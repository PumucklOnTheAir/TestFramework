import unittest
import shelve
from server.dbtestresult import DBTestResult
from server.server import Server
import os


class MyTestCase(unittest.TestCase):
    path_cli = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'cli.py')

    def test_dbm(self):
        with shelve.open('test_results') as db:
            t = DBTestResult()
            print(len(db))
            db.clear()
            print(len(db))
            db['t1'] = t
            print(len(db))
            dbt = db['t1']
            t1 = unittest.TestResult()
            t1.failures = dbt.failures
            t1.errors = dbt.errors
            db.clear()
            print(len(db))
        self.assertTrue(True, True)

    def test_shelve(self):
        Server.start()
        Server.get_test_results(-1)
        Server.stop()
        self.assertTrue(True, True)
