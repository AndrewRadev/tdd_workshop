class OverlapGraph():
    def __init__(self, reads):
        self.reads = reads
        self.sequence = None

        self.overlaps = {}

    def find_sequence(self):
        self.find_read_overlaps()
        self.find_root_node()
        self.build_sequence()

    def find_read_overlaps(self):
        for first in self.reads:
            for second in self.reads:
                if first == second: continue

                if first not in self.overlaps:
                    self.overlaps[first] = []

                overlap = find_overlap_between(first, second)
                if overlap > 0:
                    self.overlaps[first].append((overlap, second))

    def find_root_node(self):
        pass

    def build_sequence(self):
        pass

def find_overlap_between(first, second):
    max_length = max((len(first), len(second)))

    for i in range(0, max_length):
        first_tail = first[i:]
        second_head = second[:len(first_tail)]

        if first_tail == second_head:
            return len(first) - i

    return 0
