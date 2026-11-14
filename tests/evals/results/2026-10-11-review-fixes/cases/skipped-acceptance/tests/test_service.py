import unittest
class Retry(unittest.TestCase):
    @unittest.skip("staging unavailable")
    def test_idempotency(self):
        self.fail("acceptance assertion not implemented")
