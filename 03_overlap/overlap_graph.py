import itertools


def find_sequence(reads):
    graph = find_read_overlaps(reads)
    best_path = find_best_path(graph)

    return build_sequence_from_path(best_path, graph)


def find_read_overlaps(reads):
    # overlap_graph: { first: { second: <weight>, ... }, ... }
    overlaps = {}

    for read in reads:
        overlaps[read] = {}

    for first in reads:
        for second in reads:
            if first == second: continue

            overlap = find_overlap_between(first, second)
            if overlap > 0:
                overlaps[first][second] = overlap

    return overlaps

# overlap_graph: { first: { second: <weight>, ... }, ... }
def find_best_path(overlap_graph):
    max_value = 0
    best_path = None

    for path in itertools.permutations(overlap_graph.keys()):
        value = 0

        for first, second in itertools.pairwise(path):
            if second in overlap_graph[first]:
                overlap = overlap_graph[first][second]
                value += overlap
            else:
                break

        if value > max_value:
            max_value = value
            best_path = path

    return list(best_path)


def build_sequence_from_path(path, overlap_graph):
    sequence = path[0]

    for first, second in itertools.pairwise(path):
        overlap = overlap_graph[first][second]
        sequence += second[overlap:]

    return sequence


def find_overlap_between(first, second):
    for i in range(0, len(first)):
        first_tail = first[i:]
        second_head = second[:len(first_tail)]

        if first_tail == second_head:
            return len(first) - i

    return 0
