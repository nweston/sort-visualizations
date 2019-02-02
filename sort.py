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


def run_sort(sort, data, observe=True):
    for kind, a, b in sort(data):
        if observe:
            print(kind, a, b)
        if kind == 'swap':
            data[a], data[b] = data[b], data[a]


if __name__ == '__main__':
    lst = [5, 11, 2, 3, 9]
    run_sort(selection_sort, lst, observe=True)
    print(lst)
