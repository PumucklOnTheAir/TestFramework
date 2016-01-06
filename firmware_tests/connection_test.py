from server.test import AbstractTest


class ConnectionTest(AbstractTest):
    def runTest(self):
        self.test_noting()

    def test_noting(self):
        lol = True
        assert lol
