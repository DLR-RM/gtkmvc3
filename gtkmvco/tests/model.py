"""
Real unit tests for functions in gtkmvc/model.py
"""

import unittest

import _importer

from gtkmvc.model import count_leaves

class CountLeaves(unittest.TestCase):
    def testList(self):
        self.assertEqual(count_leaves([]), 0)
        self.assertEqual(count_leaves([1, 2]), 2)
        self.assertEqual(count_leaves([[1], [2]]), 2)

    def testMap(self):
        self.assertEqual(count_leaves({}), 0)
        self.assertEqual(count_leaves({1: 2}), 1)
        self.assertEqual(count_leaves({1: {2: 3}}), 1)

    def testMixed(self):
        self.assertEqual(count_leaves([{1: ()}, {2: ()}]), 0)

def has_item(x):  # Faster than count_leaves as it aborts early
    """
    Return whether any non-sequence occurs in a given recursive sequence.
    """
    if hasattr(x, 'keys'):
        x = x.values()
    if hasattr(x, '__getitem__'):
        for i in x:
            if has_item(i):
                return True
        return False
    return True

class HasItem(unittest.TestCase):
    def testList(self):
        self.assertFalse(has_item([]))
        self.assertTrue(has_item([1, 2]))
        self.assertTrue(has_item([[1], [2]]))

    def testMap(self):
        self.assertFalse(has_item({}))
        self.assertTrue(has_item({1: 2}))
        self.assertTrue(has_item({1: {2: 3}}))

    def testMixed(self):
        self.assertFalse(has_item([{1: ()}, {2: ()}]))

if __name__ == "__main__":
    unittest.main()
