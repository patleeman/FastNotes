import unittest

from tests import test_InitialSetup
from tests import test_notes

def TestSuite():
    test_suite = unittest.TestSuite()
    test_suite.addTest(unittest.makeSuite(test_notes.TestNotePy))
    return test_suite


if __name__ == '__main__':
    unittest.TextTestRunner(buffer=True).run(TestSuite())