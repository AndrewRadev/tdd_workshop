import unittest

from snps import categorize_snps
from tests.database_test import DatabaseTest

class TestCategorizeSnps(DatabaseTest):
    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()

    def test_snps_present_in_normal_samples_are_categorized_correctly(self):
        self.create_snp('normal1')
        self.create_snp_call('normal1', sample='TLE66_N', genotype_simple=2)

        categorize_snps(self.db)

        self.assertEqual(self.fetch_snp_category('normal1'), 'Normal')

    def test_snps_present_in_tumor_samples_are_categorized_correctly(self):
        self.create_snp('tumor1')
        self.create_snp_call('tumor1', sample='TLE66_T', genotype_simple=2)

        categorize_snps(self.db)

        self.assertEqual(self.fetch_snp_category('tumor1'), 'Tumor')

    def test_snps_with_no_genotype_are_not_counted(self):
        self.create_snp('normal1')
        self.create_snp('normal2')
        self.create_snp('normal3')
        self.create_snp_call('normal1', sample='TLE66_N', genotype_simple=0)
        self.create_snp_call('normal2', sample='TLE66_N', genotype_simple=1)
        self.create_snp_call('normal3', sample='TLE66_N', genotype_simple=2)

        categorize_snps(self.db)

        self.assertEqual(self.fetch_snp_category('normal1'), None)
        self.assertEqual(self.fetch_snp_category('normal2'), 'Normal')
        self.assertEqual(self.fetch_snp_category('normal3'), 'Normal')

    def test_snps_present_in_different_samples_are_categorized_correctly(self):
        self.create_snp('normal1')
        self.create_snp_call('normal1', sample='TLE66_N', genotype_simple=2)

        self.create_snp('tumor1')
        self.create_snp_call('tumor1', sample='TLE66_T', genotype_simple=2)

        self.create_snp('mixed1')
        self.create_snp_call('mixed1', sample='TLE66_N', genotype_simple=2)
        self.create_snp_call('mixed1', sample='TLE66_T', genotype_simple=2)

        self.create_snp('unknown1')
        self.create_snp_call('unknown1', sample='???', genotype_simple=2)

        categorize_snps(self.db)

        self.assertEqual(self.fetch_snp_category('normal1'), 'Normal')
        self.assertEqual(self.fetch_snp_category('tumor1'), 'Tumor')
        self.assertEqual(self.fetch_snp_category('mixed1'), 'Mixed')
        self.assertEqual(self.fetch_snp_category('unknown1'), None)

if __name__ == '__main__':
    unittest.main()
