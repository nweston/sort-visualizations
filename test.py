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
        sort.run(sort.selection_sort, xs)
        assert correct == xs


class MergeSort(unittest.TestCase):
    @given(st.lists(st.integers()))
    @settings(max_examples=200)
    @example([])
    def test_sort_works(self, xs):
        correct = list(sorted(xs))
        sort.run(sort.merge_sort, xs)
        assert correct == xs


class QuickSort(unittest.TestCase):
    @given(st.lists(st.integers()))
    @settings(max_examples=200)
    @example([0, 1, 0, 1])
    @example([])
    def test_sort_works(self, xs):
        correct = list(sorted(xs))
        sort.run(sort.quicksort, xs)
        self.assertEqual(correct, xs)


class CountSteps(unittest.TestCase):
    def test_count(self):

        def fake_sort(data):
            for _ in range(10):
                yield ('cmp', 0, 0)

        self.assertEqual(sort.count_steps(fake_sort, []), 10)
