from hypothesis import given, example, settings
import hypothesis.strategies as st
import unittest

import sort


class SelectionSort(unittest.TestCase):
    @given(st.lists(st.integers()))
    @settings(max_examples=200)
    @example([])
    def test_sort_works(self, xs):
        correct = list(sorted(xs))
        sort.run_sort(sort.selection_sort, xs, observe=False)
        assert correct == xs

class MergeSort(unittest.TestCase):
    @given(st.lists(st.integers()))
    @settings(max_examples=200)
    @example([])
    def test_sort_works(self, xs):
        correct = list(sorted(xs))
        sort.run_sort(sort.merge_sort, xs, observe=False)
        assert correct == xs
