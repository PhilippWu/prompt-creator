import unittest
from src import main

class TestMain(unittest.TestCase):
    def test_dummy(self):
        # Ein einfacher Test, der immer erfolgreich ist.
        self.assertTrue(True)

if __name__ == '__main__':
    unittest.main()
