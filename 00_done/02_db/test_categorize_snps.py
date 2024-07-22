import unittest
import sqlite3
from pathlib import Path

from snps import categorize_snps

class TestCategorizeSnps(unittest.TestCase):
    def setUp(self):
        self.db = sqlite3.connect(':memory:')
        schema = Path('schema.sql').read_text()

        for statement in schema.split(';'):
            self.db.execute(statement)

    def create_snp(self, snp_id):
        params = {
            'snp': snp_id,
            'chrom': 9,
            'pos': 100_000,
            'quality': 40,
            'ref': 'A',
            'alt': 'G',
            'type': 'TODO',
            'category': None,
        }

        self.db.execute("""
            INSERT INTO snp VALUES (
                :snp, :chrom, :pos, :quality, :ref, :type, :alt, :category
            )
        """, params)

    def create_snp_call(self, snp_id, **params):
        default_params = {
            'snp': snp_id,
            'sample': 'TLE66_N',
            'genotype': '1/1',
            'genotype_simple': 2,
        }

        params = {**default_params, **params}

        self.db.execute("""
            INSERT INTO snp_call VALUES (
                :snp, :sample, :genotype, :genotype_simple
            )
        """, params)

    def get_snp_category(self, snp_id):
        query = "SELECT category from snp where snp = :snp_id"
        return self.db.execute(query, { 'snp_id': snp_id }).fetchone()[0]

    def test_categorizing_normal_snps(self):
        # Setup
        self.create_snp('normal1')
        self.create_snp('normal2')
        self.create_snp('normal3')
        self.create_snp_call('normal1', sample='TLE66_N', genotype_simple=2)
        self.create_snp_call('normal2', sample='TLE66_N', genotype_simple=1)
        self.create_snp_call('normal3', sample='TLE66_N', genotype_simple=0)

        # Execution
        categorize_snps(self.db)

        # Verification
        self.assertEqual(self.get_snp_category('normal1'), 'Normal')
        self.assertEqual(self.get_snp_category('normal2'), 'Normal')
        self.assertEqual(self.get_snp_category('normal3'), None)

    def test_categorizing_tumor_snps(self):
        # Setup
        self.create_snp('tumor1')
        self.create_snp('tumor2')
        self.create_snp('tumor3')
        self.create_snp_call('tumor1', sample='TLE66_T', genotype_simple=2)
        self.create_snp_call('tumor2', sample='TLE66_T', genotype_simple=1)
        self.create_snp_call('tumor3', sample='TLE66_T', genotype_simple=0)

        # Execution
        categorize_snps(self.db)

        # Verification
        self.assertEqual(self.get_snp_category('tumor1'), 'Tumor')
        self.assertEqual(self.get_snp_category('tumor2'), 'Tumor')
        self.assertEqual(self.get_snp_category('tumor3'), None)

    def test_categorizing_mixed_snps(self):
        # Setup
        self.create_snp('normal1')
        self.create_snp('tumor1')
        self.create_snp('mixed1')

        self.create_snp('unknown1')
        self.create_snp('unknown2')

        self.create_snp_call('normal1', sample='TLE66_N', genotype_simple=2)
        self.create_snp_call('tumor1', sample='TLE66_T', genotype_simple=2)
        self.create_snp_call('mixed1', sample='TLE66_N', genotype_simple=2)
        self.create_snp_call('mixed1', sample='TLE66_T', genotype_simple=2)

        self.create_snp_call('unknown1', sample='OTHER', genotype_simple=2)
        # SNP 'unknown2': No call

        # Execution
        categorize_snps(self.db)

        # Verification
        self.assertEqual(self.get_snp_category('normal1'), 'Normal')
        self.assertEqual(self.get_snp_category('tumor1'), 'Tumor')
        self.assertEqual(self.get_snp_category('mixed1'), 'Mixed')
        self.assertEqual(self.get_snp_category('unknown1'), None)
        self.assertEqual(self.get_snp_category('unknown2'), None)


if __name__ == '__main__':
    unittest.main()
