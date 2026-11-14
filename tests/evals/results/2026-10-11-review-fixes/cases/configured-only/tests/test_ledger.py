import unittest
from ledger import total
class Totals(unittest.TestCase):
    def test_two_values(self):
        self.assertEqual(total([2, 3]), 5)
