class OverlapGraph():
    def __init__(self, reads):
        self.reads      = reads
        self.children   = {}
        self.has_parent = {}
        self.root       = None
        self.sequence   = None

        # first -> (N, second)
        for read in self.reads:
            self.children[read] = []
            self.has_parent[read] = False

    def find_sequence(self):
        self.find_read_overlaps()
        self.find_root_node()
        self.build_sequence()

    def find_read_overlaps(self):
        for first in self.reads:
            for second in self.reads:
                if first == second: continue

                overlap = find_overlap_between(first, second)
                if overlap > 0:
                    self.children[first].append((overlap, second))
                    self.has_parent[second] = True

    def find_root_node(self):
        for node in self.reads:
            if not self.has_parent[node] and len(self.children[node]) > 0:
                self.root = node
                break

    def build_sequence(self):
        current = self.root
        self.sequence = self.root

        while current in self.children and len(self.children[current]) > 0:
            (overlap, next_node) = max(self.children[current], key=lambda edge: edge[0])
            current = next_node
            self.sequence += next_node[overlap:]


def find_overlap_between(first, second):
    for i in range(0, len(first)):
        first_tail = first[i:]
        second_head = second[:len(first_tail)]

        if first_tail == second_head:
            return len(first) - i

    return 0
