def selection_sort(data):
    """Sort contents of data in place.

This is a generator which yields each algorithm step (comparison or
swap), allow for visualization or instrumentation. The caller is
responsible for performing swaps.
"""
    for dest in range(len(data) - 1):
        smallest_i = dest
        for i in range(dest+1, len(data)):
            yield ('cmp', smallest_i, i)
            if data[i] < data[smallest_i]:
                smallest_i = i
        yield ('swap', dest, smallest_i)


def merge(data, left, mid, right):
    # Copy each sub-list, reverse them so we can pop from the end, and
    # merge back into the main list. This isn't terribly efficient but
    # it's convenient.
    yield ('merge', (left, mid), (mid, right))
    sub_left = data[left:mid]
    sub_right = data[mid:right]
    for i in range(left, right):
        if not sub_right or (sub_left and sub_left[0] < sub_right[0]):
            yield ('set', i, sub_left[0])
            del sub_left[0]
        else:
            yield ('set', i, sub_right[0])
            del sub_right[0]
    assert len(sub_left) == 0
    assert len(sub_right) == 0


def merge_sort(data, left=None, right=None):
    """Merge sort in place. Like selection_sort, this is a generator."""
    if left is None:
        left = 0
    if right is None:
        right = len(data)
    if right <= left + 1:
        return

    mid = (left + right) // 2
    yield ('subdivide', (left, mid), (mid, right))
    for e in merge_sort(data, left, mid):
        yield e
    for e in merge_sort(data, mid, right):
        yield e

    for e in merge(data, left, mid, right):
        yield e


def run_sort(sort, data, observe=True):
    for kind, a, b in sort(data):
        if observe:
            print(kind, a, b)
        if kind == 'swap':
            data[a], data[b] = data[b], data[a]
        if kind == 'set':
            data[a] = b


if __name__ == '__main__':
    lst = [5, 11, 2, 3, 9]
    run_sort(merge_sort, lst, observe=True)
    print(lst)
