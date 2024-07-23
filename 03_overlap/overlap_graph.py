import itertools

class OverlapGraph():
    def __init__(self, reads):
        self.reads = reads

        self.children   = {}
        self.has_parent = {}

        self.root         = None
        self.sorted_reads = None
        self.sequence     = None

        # first -> (N, second)
        for read in self.reads:
            self.children[read] = []
            self.has_parent[read] = False

    def find_sequence(self):
        self.find_read_overlaps()

        # self.find_root_node()
        self.sort_reads()

        self.build_sequence()

    def find_read_overlaps(self):
        for first in self.reads:
            for second in self.reads:
                if first == second: continue

                overlap = find_overlap_between(first, second)
                if overlap > 0:
                    self.children[first].append((overlap, second))
                    self.has_parent[second] = True

    def sort_reads(self):
        max_value = 0
        best_path = None

        for path in itertools.permutations(self.reads):
            value = 0

            for first, second in itertools.pairwise(path):
                overlap = next((
                    overlap
                    for (overlap, next_node) in self.children[first]
                    if next_node == second
                ), None)

                if overlap is None:
                    break
                else:
                    value += overlap

            if value > max_value:
                max_value = value
                best_path = path

        self.sorted_reads = list(best_path)

    def find_root_node(self):
        for node in self.reads:
            if not self.has_parent[node] and len(self.children[node]) > 0:
                self.root = node
                break

    def build_sequence(self):
        for first, second in itertools.pairwise(self.sorted_reads):
            if self.sequence is None:
                self.sequence = first

            overlap = next((
                overlap
                for (overlap, next_node) in self.children[first]
                if next_node == second
            ), None)

            self.sequence += second[overlap:]


def find_overlap_between(first, second):
    for i in range(0, len(first)):
        first_tail = first[i:]
        second_head = second[:len(first_tail)]

        if first_tail == second_head:
            return len(first) - i

    return 0
