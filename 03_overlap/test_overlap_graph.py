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

        self.assertEqual(graph.children, {
            'ABCD': [(2, 'CDEF')],
            'CDEF': []
        })

        graph = OverlapGraph(['ABCDEF', 'EF', 'FGHA'])
        graph.find_read_overlaps()

        self.assertEqual(graph.children, {
            'ABCDEF': [(2, 'EF'), (1, 'FGHA')],
            'EF': [(1, 'FGHA')],
            'FGHA': [(1, 'ABCDEF')]
        })

    def test_finding_the_root_of_the_overlap_graph(self):
        graph = OverlapGraph(['ABCD', 'CDEF'])
        graph.find_read_overlaps()
        graph.find_root_node()

        self.assertEqual(graph.root, 'ABCD')

        graph = OverlapGraph(['BCD', 'AB', 'CDEF'])
        graph.find_read_overlaps()
        graph.find_root_node()

        self.assertEqual(graph.root, 'AB')

        graph = OverlapGraph(['A', 'B', 'BC'])
        graph.find_read_overlaps()
        graph.find_root_node()

        self.assertEqual(graph.root, 'B')

    def test_overlap_graph_produces_correct_sequence(self):
        graph = OverlapGraph(['ABCD', 'CDEF'])
        graph.find_sequence()

        self.assertEqual(graph.sequence, 'ABCDEF')

        graph = OverlapGraph(['CDEFG', 'ABCD', 'EFG', 'BC'])
        graph.find_sequence()

        self.assertEqual(graph.sequence, 'ABCDEFG')

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
