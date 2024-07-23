import unittest

from overlap_graph import OverlapGraph, find_overlap_between

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
        graph = OverlapGraph(['ABCD', 'CDEF'])
        graph.find_read_overlaps()

        self.assertEqual(graph.overlaps, {
            'ABCD': {'CDEF': 2},
            'CDEF': {},
        })

        graph = OverlapGraph(['ABCDEF', 'EF', 'FGHA'])
        graph.find_read_overlaps()

        self.assertEqual(graph.overlaps, {
            'ABCDEF': { 'EF': 2, 'FGHA': 1 },
            'EF': { 'FGHA': 1 },
            'FGHA': { 'ABCDEF': 1 },
        })

    def test_overlap_graph_produces_correct_sequence(self):
        graph = OverlapGraph(['ABCD', 'CDEF'])
        graph.find_sequence()

        self.assertEqual(graph.sequence, 'ABCDEF')

        graph = OverlapGraph(['CDEFG', 'ABCD', 'EFG'])
        graph.find_sequence()

        self.assertEqual(graph.sequence, 'ABCDEFG')

    def test_reads_are_sorted_by_graph_weight(self):
        graph = OverlapGraph([
            'CCTTTGA',
            'ATTGCA',
            'GGATATCC',
            'CATCGG',
            'TCGGGAT',
        ])
        graph.find_read_overlaps()
        graph.sort_reads()

        self.assertEqual(graph.sorted_reads, [
            'ATTGCA',
            'CATCGG',
            'TCGGGAT',
            'GGATATCC',
            'CCTTTGA'
        ])

    def test_overlap_graph_produces_big_sequence(self):
        graph = OverlapGraph([
            'CCTTTGA',
            'ATTGCA',
            'GGATATCC',
            'CATCGG',
            'TCGGGAT',
        ])
        graph.find_sequence()

        self.assertEqual(graph.sequence, 'ATTGCATCGGGATATCCTTTGA')
