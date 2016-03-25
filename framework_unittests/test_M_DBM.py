import unittest
import shelve
from server.dbtestresult import DBTestResult


class MyTestCase(unittest.TestCase):

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
