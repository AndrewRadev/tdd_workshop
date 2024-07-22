import unittest
import sqlite3
from pathlib import Path


class DatabaseTest(unittest.TestCase):
    def setUp(self):
        self.db = sqlite3.connect(':memory:')
        schema = Path('schema.sql').read_text()

        for statement in schema.split(';'):
            self.db.execute(statement)

    def tearDown(self):
        self.db.close()

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
