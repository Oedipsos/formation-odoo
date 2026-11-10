from datetime import date
from operator import itemgetter

Interval = tuple[date, date]


def overlaps(a: Interval, b: Interval) -> bool:
    """
    Returns True if time interval 'a' overlaps with time interval 'b', else otherwise.
    """
    return max(a[0], b[0]) < min(a[1], b[1])


def find_overlapping_pairs_naive(intervals: list[Interval]) -> list[tuple[int, int]]:
    """
    Find overlapping pairs of given intervals. Naive inplementation
    with quadratic time complexity.
    """
    overlapping_pairs = []
    n = len(intervals)
    for i in range(n):
        for j in range(i + 1, n):
            if overlaps(intervals[i], intervals[j]):
                overlapping_pairs.append((i, j))

    return overlapping_pairs


def find_overlapping_pairs(intervals: list[Interval]) -> list[tuple[int, int]]:
    """
    Find overlapping pairs of given intervals. Faster implementation by sorting first
    (N log N complexity) plus a best case linear scan.
    """
    overlapping_pairs = []
    active = []
    # We use enumerate to assign an id to each interval, since they will be shuffled.
    for i, interval in sorted(enumerate(intervals), key=itemgetter(1)):
        # iterate on copy since it will be mutated
        for j, active_interval in active.copy():
            if overlaps(interval, active_interval):
                # Asserting that i < j
                overlapping_pairs.append((min(i, j), max(i, j)))
            else:
                active.remove((j, active_interval))
        active.append((i, interval))

    return sorted(overlapping_pairs)
