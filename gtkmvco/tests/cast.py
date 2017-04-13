import unittest

import _importer
import gtkmvc

TYPES = [int, float, str, unicode]
VALUES = [t(1) for t in TYPES]

class AdaptTypes(unittest.TestCase):
    def testEmpty(self):
        self.assertEqual(0, gtkmvc.support.utils.cast_value('', int))

    def testCast(self):
        for t in TYPES:
            for v in VALUES:
                r = gtkmvc.support.utils.cast_value(v, t)
                self.assertEqual(t, type(r))
                if t == type(v):
                    self.assertEqual(v, r)
        return

if __name__ == "__main__":
    unittest.main()
