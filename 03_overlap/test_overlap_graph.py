import unittest

from overlap_graph import *

class TestOverlapGraph(unittest.TestCase):
    def test_finding_overlap_between_two_sequences(self):
        self.assertEqual(find_overlap_between('ABC', 'ABC'), 3)
        self.assertEqual(find_overlap_between('ABC', 'BCD'), 2)
        self.assertEqual(find_overlap_between('ABC', 'CDE'), 1)
        self.assertEqual(find_overlap_between('ABC', 'DEF'), 0)

        self.assertEqual(find_overlap_between('ABCDEF', 'EFG'), 2)
        self.assertEqual(find_overlap_between('ABC', 'CDEFG'), 1)

        self.assertEqual(find_overlap_between('', ''), 0)

    def test_finding_overlaps_between_a_group_of_sequences(self):
        overlaps = find_read_overlaps(['ABCD', 'CDEF'])

        self.assertEqual(overlaps, {
            'ABCD': {'CDEF': 2},
            'CDEF': {},
        })

        overlaps = find_read_overlaps(['ABCDEF', 'EF', 'FGHA'])

        self.assertEqual(overlaps, {
            'ABCDEF': { 'EF': 2, 'FGHA': 1 },
            'EF': { 'FGHA': 1 },
            'FGHA': { 'ABCDEF': 1 },
        })

    def test_overlap_graph_produces_correct_sequence(self):
        self.assertEqual(find_sequence(['ABCD', 'CDEF']), 'ABCDEF')
        self.assertEqual(find_sequence(['CDEFG', 'ABCD', 'EFG']), 'ABCDEFG')

    def test_reads_are_sorted_by_graph_weight(self):
        graph = find_read_overlaps([
            'CCTTTGA',
            'ATTGCA',
            'GGATATCC',
            'CATCGG',
            'TCGGGAT',
        ])
        path = find_best_path(graph)

        self.assertEqual(path, [
            'ATTGCA',
            'CATCGG',
            'TCGGGAT',
            'GGATATCC',
            'CCTTTGA'
        ])

    def test_overlap_graph_produces_big_sequence(self):
        sequence = find_sequence([
            'CCTTTGA',
            'ATTGCA',
            'GGATATCC',
            'CATCGG',
            'TCGGGAT',
        ])

        self.assertEqual(sequence, 'ATTGCATCGGGATATCCTTTGA')
