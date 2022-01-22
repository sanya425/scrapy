import unittest
from unittest.mock import MagicMock, patch, Mock
import report
from GridBlog.pipelines import GridBlogPipeline
import sqlite3
from GridBlog.spiders.authors_spider import AuthorsSpider
from GridBlog.items import GridBlogItem
from sqlite3 import Error


class TestReport(unittest.TestCase):

    def test_report_connection(self):
        self.assertEqual(type(report.create_connection('GDblog.db')), sqlite3.Connection)

    def test_pipelines_connection(self):
        pipeline = GridBlogPipeline()
        self.assertEqual(type(pipeline.create_connection()), sqlite3.Connection)

    def test_add_items(self):
        items = {}
        report.add_items(items, '1', '2', '3', 4)
        self.assertEqual(items['linked_in_url'], '1')
        self.assertEqual(items['job_title'], '2')
        self.assertEqual(items['author'], '3')
        self.assertEqual(items['count_article'], 4)

    def test_number_of_tables(self):
        mock = MagicMock()
        mock.execute.return_value.fetchone.return_value = [1]
        res = report.number_of_tables(mock)
        mock.execute.assert_called_once_with("SELECT count(*) FROM sqlite_master WHERE type='table'")
        mock.execute().fetchone.assert_called_once()
        self.assertEqual(res, 1)

    @patch('GridBlog.spiders.authors_spider.GD_items')
    def test_parse_author(self, mock_blog):
        test_data = {
            'linked_in_url': 'https://www.linkedin.com/in/ivanpetrushin/',
            'job_title': 'Senior Big Data Engineer in Delivery',
            'author': 'Ivan Petrushin',
            'count_article': ['q', 'w', 'e']
        }

        mock_blog.GridBlogItem.return_value = {}
        mock_response = MagicMock()
        mock_response.css.return_value.get.side_effect = [test_data['author'], test_data['linked_in_url'],
                                                          test_data['job_title']]
        mock_response.css.return_value.getall.return_value = test_data['count_article']
        parse_a = AuthorsSpider()
        res = list(parse_a.parse_author(mock_response))[0]
        test_data['count_article'] = len(test_data['count_article'])
        mock_response.css().getall.assert_called_once()
        self.assertEqual(res, test_data)


if __name__ == '__main__':
    unittest.main()

# python -m unittest discover
# python -m unittest filename.py
# type hints; mock; git
