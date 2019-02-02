from hypothesis import given, example, settings
import hypothesis.strategies as st
import unittest

from sort import *

class SelectionSort(unittest.TestCase):
#    @settings(max_examples=1000)
    @given(st.lists(st.integers()))
    @example([])
    def test_sort_works(self, xs):
        correct = list(sorted(xs))
        run_sort(selection_sort, xs, observe=False)
        assert correct == xs
