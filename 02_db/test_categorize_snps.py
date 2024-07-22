import unittest
import sqlite3
from pathlib import Path

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

    def test_example(self):
        self.assertEqual(1 + 1, 2)


if __name__ == '__main__':
    unittest.main()
