import unittest
import report
from GridBlog.pipelines import GridBlogPipeline
import sqlite3
from sqlite3 import Error

class TestReport(unittest.TestCase):
    def setUp(self) -> None:
        self.conn = None
        try:
            self.conn = sqlite3.connect('GDblog.db')
        except Error as e:
            print(e)
        self.cur = self.conn.cursor()

    def test_number_of_tables(self):
        self.assertEqual(type(report.number_of_tables(self.cur)), int)

    def test_report_connection(self):
        self.assertEqual(type(report.create_connection('GDblog.db')), sqlite3.Connection)

    def test_pipelines_connection(self):
        pipeline = GridBlogPipeline()
        self.assertEqual(type(pipeline.create_connection()), sqlite3.Connection)

if __name__ == '__main__':
    unittest.main()

# python -m unittest discover
# python -m unittest filename.py
