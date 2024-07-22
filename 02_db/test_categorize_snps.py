import unittest
import sqlite3
from pathlib import Path

from snps import categorize_snps

# Add "category" to snps:
#
# 1. If snp is normal-specific, category = "Normal"
# 2. If snp is tumor-specific,  category = "Tumor"
# 3. If snp is both,            category = "Mixed"
# 4. If snp is neither,         category = NULL
#
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
            'pos': 10_000,
            'quality': 40,
            'ref': 'A',
            'alt': 'G',
            'type': '???',
            'category': None,
        }

        self.db.execute("""
            INSERT INTO snp
            VALUES (:snp, :chrom, :pos, :quality, :ref, :alt, :type, :category)
        """, params)

    def create_snp_call(self, snp_id, **params):
        default_params = {
            'snp': snp_id,
            'sample': 'Unknown',
            'genotype': './.',
            'genotype_simple': 0,
        }

        params = {**default_params, **params}

        self.db.execute("""
            INSERT INTO snp_call
            VALUES (:snp, :sample, :genotype, :genotype_simple)
        """, params)

    def fetch_snp_category(self, snp_id):
        query = 'SELECT category FROM snp where snp = ?'
        bindings = (snp_id,)

        return self.db.execute(query, bindings).fetchone()[0]

    def test_snps_present_in_normal_samples_are_categorized_correctly(self):
        self.create_snp('normal1')
        self.create_snp_call('normal1', sample='TLE66_N')

        category = self.fetch_snp_category('normal1')
        self.assertEqual(category, None)

        categorize_snps(self.db)

        category = self.fetch_snp_category('normal1')
        self.assertEqual(category, 'Normal')


if __name__ == '__main__':
    unittest.main()
