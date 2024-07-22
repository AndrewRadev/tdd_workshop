import unittest

from overlap_graph import OverlapGraph

class TestOverlapGraph(unittest.TestCase):
    def test_overlap_graph_produces_correct_sequence(self):
        graph = OverlapGraph(['ABCD', 'CDEF'])
        graph.find_sequence()

        self.assertEqual(graph.sequence, 'ABCDEF')

        graph = OverlapGraph(['CDEFG', 'ABCD', 'EFG', 'BC'])
        graph.find_sequence()

        self.assertEqual(graph.sequence, 'ABCDEFG')
