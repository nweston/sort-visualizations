import matplotlib.pyplot as plt
import hypothesis.strategies as st


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

    def inc_count(*args):
        nonlocal count
        count = count + 1
    count = 0

    run(sort, data, inc_count)
    return count


def plot_sorts(sorts, input_sizes):
    """Create a plot of runtime for each sort with different input sizes.

Will graph each sort with each input size. Returns a matplotlib figure.
"""
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)

    for s in sorts:
        data = [(n, count_steps(s, st.lists(st.integers(),
                                            min_size=n, max_size=n).example()))
                for n in input_sizes]
        ax.plot(*zip(*data))
    ax.legend([s.__name__ for s in sorts])
    plt.xlabel('Input Length')
    plt.ylabel('Steps')
    fig


if __name__ == '__main__':
    lst = [5, 11, 2, 3, 9]
    mysort = merge_sort

    print_effects(mysort, lst)
    print(lst)
    print(count_steps(mysort, lst), 'steps')
