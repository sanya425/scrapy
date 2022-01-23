import unittest
from unittest.mock import MagicMock, patch
import report
from GridBlog.pipelines import GridBlogPipeline
import sqlite3
from GridBlog.spiders.authors_spider import AuthorsSpider
from GridBlog.spiders.articles_spider import ArticlesSpider


class TestReport(unittest.TestCase):

    def test_report_connection(self):
        self.assertEqual(type(report.create_connection('GDblog.db')), sqlite3.Connection)

    def test_pipelines_connection(self):
        pipeline = GridBlogPipeline()
        self.assertEqual(type(pipeline.create_connection()), sqlite3.Connection)

    def test_number_of_tables(self):
        mock = MagicMock()
        mock.execute.return_value.fetchone.return_value = [1]
        res = report.number_of_tables(mock)
        mock.execute.assert_called_once_with("SELECT count(*) FROM sqlite_master WHERE type='table'")
        mock.execute().fetchone.assert_called_once()
        self.assertEqual(res, 1)

    @patch('GridBlog.spiders.authors_spider.GridBlogItem')
    def test_parse_author(self, mock_blog):
        test_data = {
            'linked_in_url': 'https://www.linkedin.com/in/ivanpetrushin/',
            'job_title': 'Senior Big Data Engineer in Delivery',
            'author': 'Ivan Petrushin',
            'names_articles': ['q', 'w', 'e']
        }
        data_res = {
            'linked_in_url': 'https://www.linkedin.com/in/ivanpetrushin/',
            'job_title': 'Senior Big Data Engineer in Delivery',
            'author': 'Ivan Petrushin',
            'count_article': 3
        }
        mock_blog.return_value = {}
        mock_response = MagicMock()
        mock_response.css.return_value.get.side_effect = [test_data['author'], test_data['linked_in_url'],
                                                          test_data['job_title']]
        mock_response.css.return_value.getall.return_value = test_data['names_articles']
        parse_a = AuthorsSpider()
        res = list(parse_a.parse_author(mock_response))[0]
        mock_response.css().getall.assert_called_once()
        mock_response.css().get.assert_called()
        self.assertEqual(res, data_res)

    @patch('GridBlog.spiders.articles_spider.GridBlogItem')
    def test_parse_article(self, mock_blog):
        test_data = {
            'title': 'Art.com helps customers find art they love with visual search',
            'article_url': 'https://blog.griddynamics.com/'
                           'art-com-improves-product-discovery-with-visual-similarity-search/',

            'text': 'The demands on IT service providers are changing because companies are embracing digital'
                    ' transformation. Traditionally most IT services were confined to packaged software'
                    ' implementation, system integration, and managed services. Companies grew to rely on'
                    ' traditional outsourcers for these kinds of IT projects. However, the advent of digital'
                    ' transformation has added a new demand for IT companies, in addition to regular IT jobs.'
                    ' Analysis shows that the digital transformation market will grow to 120 Billion in 2020,'
                    ' with 90% of companies saying they are not digital yet. Meeting this new demand cannot be'
                    ' addressed using the vendors, contracts, and sourcing strategies used for traditional IT. '
                    'These strategies work best with conventional IT projects for which they were initially designed.',

            'publication_date': '\n\t\t\t\t\t\t\tDec 30, 2019\n\t\t\t\t\t\t\t• ',#'2019-12-30'
            'author': ['\n\t\t\t\t\t\t\t\t\t\t\tMax Martynov', '\n\t\t\t\t\t\t\t\t\t\t',
                       '\n\t\t\t\t\t\t\t\t\t\t\tEzra Berger', '\n\t\t\t\t\t\t\t\t\t\t'],#'Max Martynov;Ezra Berger'
            'tags': ['<meta charset="utf-8">', '<meta http-equiv="X-UA-Compatible" content="IE=edge">',
                     '<meta name="HandheldFriendly" content="True">',
                     '<meta name="viewport" content="width=device-width, initial-scale=1.0">',
                     '<meta name="msapplication-TileImage" content="/assets/favicon.ico">',
                     '<meta name="msapplication-square70x70logo" content="/assets/ico/mstile-70x70.png">',
                     '<meta name="msapplication-square150x150logo" content="/assets/ico/mstile-150x150.png">',
                     '<meta name="msapplication-wide310x150logo" content="/assets/ico/mstile-310x150.png">',
                     '<meta name="msapplication-square310x310logo" content="/assets/ico/mstile-310x310.png">',
                     '<meta name="description" content="Agile co-creation engineering service vendors are best suited'
                     ' for the challenges of digital transformation. Outsource vendors will no longer cut it.">',
                     '<meta name="referrer" content="no-referrer-when-downgrade">',
                     '<meta property="og:site_name" content="Grid Dynamics Blog">',
                     '<meta property="og:type" content="article">',
                     '<meta property="og:title" content="Digital transformation requires partnerships'
                     ' and Agile co-innovation">',
                     '<meta property="og:description" content="A successful digital transformation benefits from'
                     ' new technology partnerships with Agile co-innovation companies. These companies bring a fresh'
                     ' perspective of co-creation through strategic partnerships, replacing the old concept of'
                     ' outsourcing or outstaffing.">',
                     '<meta property="og:url" content="https://blog.griddynamics.com/'
                     'digital-transformation-requires-new-technology-partnerships-and-agile-co-innovation/">',
                     '<meta property="og:image" content="https://blog.griddynamics.com/content/images/'
                     '2020/03/agile-coiinovation.jpg">',
                     '<meta property="article:published_time" content="2019-12-30T19:33:43.000Z">',
                     '<meta property="article:modified_time" content="2021-08-02T12:31:10.000Z">',
                     '<meta property="article:tag" content="CICD">',
                     '<meta property="article:tag" content="E-commerce">',
                     '<meta property="article:publisher" content="https://www.facebook.com/griddynamics/">',
                     '<meta name="twitter:card" content="summary_large_image">',
                     '<meta name="twitter:title" content="Digital transformation requires partnerships and'
                     ' Agile co-innovation">',
                     '<meta name="twitter:description" content="A successful digital transformation benefits from new'
                     ' technology partnerships with Agile co-innovation companies. These companies bring a fresh'
                     ' perspective of co-creation through strategic partnerships, replacing the old concept of'
                     ' outsourcing or outstaffing.">',
                     '<meta name="twitter:url" content="https://blog.griddynamics.com/'
                     'digital-transformation-requires-new-technology-partnerships-and-agile-co-innovation/">',
                     '<meta name="twitter:image" content="https://blog.griddynamics.com/content/images/2020/'
                     '03/agile-coiinovation.jpg">',
                     '<meta name="twitter:label1" content="Written by">',
                     '<meta name="twitter:data1" content="Max Martynov">',
                     '<meta name="twitter:label2" content="Filed under">',
                     '<meta name="twitter:data2" content="CICD, E-commerce">',
                     '<meta name="twitter:site" content="@GridDynamics">',
                     '<meta property="og:image:width" content="2000">',
                     '<meta property="og:image:height" content="1125">', '<meta name="generator" content="Ghost 3.42">',
                     '<meta name="cmsmagazine" content="da0738f9ba7f2c0a03878b32a7c9bfc6">',
                     '<meta name="google-site-verification" content="JMBIDXC03md2jdlPf2MpnOLpeXCDs-Ef9XAZrsp3fQw">',
                     '<meta name="google-site-verification" content="Hn6fr1M68PxxoBqtvPN8lCxENFfYE0lb1qBx4YyudN4">',
                     '<meta itemprop="inLanguage" content="en-US">',
                     '<meta itemprop="datePublished" content="Dec 30, 2019">',
                     '<meta itemprop="dateModified" content="Jan 19, 2022">',
                     '<meta itemprop="url" content="https://blog.griddynamics.com/assets/i/griddynamics.jpg">',
                     '<meta itemprop="width" content="227">', '<meta itemprop="height" content="57">',
                     '<meta itemprop="url" content="https://blog.griddynamics.com/assets/i/griddynamics.jpg">']#'CICD;E-commerce'
        }
        data_res = {
            'title': 'Art.com helps customers find art they love with visual search',
            'article_url': 'https://blog.griddynamics.com/'
                           'art-com-improves-product-discovery-with-visual-similarity-search/',

            'text': 'The demands on IT service providers are changing because companies are embracing digital'
                    ' transformation. Traditionally most IT services were confined to package',

            'publication_date': '2019-12-30',
            'author': 'Max Martynov;Ezra Berger',
            'tags': 'CICD;E-commerce'
        }
        mock_blog.return_value = {}
        mock_response = MagicMock()
        mock_response.url = test_data['article_url']
        mock_response.css.return_value.get.side_effect = [test_data['title'], test_data['text'],
                                                          test_data['publication_date']]
        mock_response.css.return_value.getall.side_effect = [test_data['author'], test_data['tags']]
        parse_a = ArticlesSpider()
        res = list(parse_a.parse_article(mock_response))[0]
        mock_response.css().get.assert_called()
        mock_response.css().getall.assert_called()
        print(mock_response.mock_calls)
        self.assertEqual(res, data_res)


if __name__ == '__main__':
    unittest.main()

# python -m unittest discover
# python -m unittest filename.py
# type hints; mock; git
