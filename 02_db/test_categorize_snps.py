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
        pass

    def create_snp_call(self, snp_id, **params):
        pass

    def get_snp_category(self, snp_id):
        pass

    def test_categorizing_normal_snps(self):
        # Setup
        self.create_snp('normal1')
        self.create_snp_call('normal1', sample='TLE66_N', genotype='1/1')

        # Execution
        categorize_snps()

        # Verification
        category = self.get_snp_category('normal1')
        self.assertEqual(category, 'Normal')


if __name__ == '__main__':
    unittest.main()
