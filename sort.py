import hypothesis.strategies as st


def selection_sort(data):
    """Sort contents of data in place.

This is a generator which yields each algorithm step (comparison or
swap), allow for visualization or instrumentation. The caller is
responsible for performing swaps.
"""
    for dest in range(len(data) - 1):
        yield ('label', 'Find Smallest', None)
        smallest_i = dest
        yield ('focus', dest, None)
        for i in range(dest + 1, len(data)):
            yield ('cmp', smallest_i, i)
            if data[i] < data[smallest_i]:
                smallest_i = i
                yield ('focus', i, None)
        yield ('label', 'Move to Front', None)
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
    yield ('subdivide', left, mid)
    for e in merge_sort(data, left, mid):
        yield e
    yield ('subdivide', mid + 1, right)
    for e in merge_sort(data, mid, right):
        yield e

    for e in merge(data, left, mid, right):
        yield e


def quicksort(data, left=None, right=None):
    """Quick sort in place. Like selection_sort, this is a generator."""
    if left is None:
        left = 0
    if right is None:
        right = len(data) - 1
    if right <= left:
        return

    mid = None
    def partition(data, left, right):
        pi = (left + right) // 2
        pivot = data[pi]
        yield ('label', 'Partition, pivot=%s' % pivot, None)
        i = left
        j = right
        while True:
            yield('focus', pi, None)
            while True:
                yield ('cmp', i, pi)
                if data[i] >= pivot:
                    yield ('focus', i, pi)
                    break
                i += 1
            while True:
                yield ('cmp', j, pi)
                if data[j] <= pivot:
                    yield ('focus', i, j)
                    break
                j -= 1

            nonlocal mid
            if i >= j:
                mid = j
                return
            elif data[i] == pivot and data[j] == pivot:
                mid = i
                return

            yield ('swap', i, j)
            if i == pi:
                pi = j
            elif j == pi:
                pi = i

    for e in partition(data, left, right):
        yield e
    assert(mid is not None)

    yield ('label', 'Sort Left Side', None)
    yield ('subdivide', left, mid + 1)
    for e in quicksort(data, left, mid):
        yield e
    yield ('label', 'Sort Right Side', None)
    yield ('subdivide', mid + 1, right + 1)
    for e in quicksort(data, mid + 1, right):
        yield e
    yield ('subdivide', left, right + 1)
    yield ('label', 'Sorted from %d to %d' % (left, right), None)


def perform_effect(effect, data):
    """Apply an effect to a list, modifying the data argument."""
    kind, a, b = effect
    if kind == 'swap':
        data[a], data[b] = data[b], data[a]
    if kind == 'set':
        data[a] = b


def run(sort, data, callback=None):
    """Run a sorting algorithm, passing all effects to optional callback."""
    for effect in sort(data):
        if callback:
            callback(*effect)
        perform_effect(effect, data)


def print_effects(sort, data):
    """Run a sorting algorithm, printing all steps."""
    run(sort, data, lambda *e: print(*e))


def count_steps(sort, data):
    """Run a sorting algorithm, returning the number of effects performed."""

    def inc_count(effect, a, b):
        nonlocal count
        if effect in ['cmp', 'swap', 'set']:
            count = count + 1
    count = 0

    run(sort, data, inc_count)
    return count


def random_list(length, max_value=None):
    return st.lists(st.integers(min_value=1, max_value=max_value),
                    min_size=length, max_size=length).example()


if __name__ == '__main__':
    lst = [-2, -2]
    mysort = quicksort

    print_effects(mysort, lst)
    print(lst)
    print(count_steps(mysort, lst), 'steps')
