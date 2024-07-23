import itertools

class OverlapGraph():
    def __init__(self, reads):
        self.reads    = reads
        self.overlaps = {}

        self.sorted_reads = None
        self.sequence     = None

        # first -> { second: N, ...}
        for read in self.reads:
            self.overlaps[read] = {}

    def find_sequence(self):
        self.find_read_overlaps()
        self.sort_reads()
        self.build_sequence()

    def find_read_overlaps(self):
        for first in self.reads:
            for second in self.reads:
                if first == second: continue

                overlap = find_overlap_between(first, second)
                if overlap > 0:
                    self.overlaps[first][second] = overlap

    def sort_reads(self):
        max_value = 0
        best_path = None

        for path in itertools.permutations(self.reads):
            value = 0

            for first, second in itertools.pairwise(path):
                if second in self.overlaps[first]:
                    overlap = self.overlaps[first][second]
                    value += overlap
                else:
                    break

            if value > max_value:
                max_value = value
                best_path = path

        self.sorted_reads = list(best_path)

    def build_sequence(self):
        for first, second in itertools.pairwise(self.sorted_reads):
            if self.sequence is None:
                self.sequence = first

            overlap = self.overlaps[first][second]
            self.sequence += second[overlap:]


def find_overlap_between(first, second):
    for i in range(0, len(first)):
        first_tail = first[i:]
        second_head = second[:len(first_tail)]

        if first_tail == second_head:
            return len(first) - i

    return 0
