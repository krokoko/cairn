import unittest
from terminal import Status, is_terminal
# REQ-TERMINAL/4 expected table supplied independently by domain owner Mira.
class TerminalTable(unittest.TestCase):
    def test_queued(self):
        self.assertIs(is_terminal(Status.QUEUED), False)
    def test_running(self):
        self.assertIs(is_terminal(Status.RUNNING), False)
    def test_done(self):
        self.assertIs(is_terminal(Status.DONE), True)
    def test_cancelled(self):
        self.assertIs(is_terminal(Status.CANCELLED), True)
