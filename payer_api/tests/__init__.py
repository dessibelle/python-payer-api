import unittest


class TestCase(unittest.TestCase):
    # Implement assertIsNotNone for Python runtimes < 2.7 or < 3.1
    if not hasattr(unittest.TestCase, 'assertIsNotNone'):
        def assertIsNotNone(self, value, *args):
            self.assertNotEqual(value, None, *args)
