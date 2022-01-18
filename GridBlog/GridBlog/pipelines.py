# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import sqlite3
from sqlite3 import Error


class GridBlogPipeline(object):
    """
    Pipeline to sqlite3
    """

    def __init__(self):
        self.conn = self.create_connection()
        self.cur = self.conn.cursor()
        self.create_tables()

    def create_connection(self):
        self.conn = None
        try:
            self.conn = sqlite3.connect('GDblog.db')
        except Error as e:
            print(e)
        return self.conn

    def create_tables(self):
        self.cur.execute("""CREATE TABLE IF NOT EXISTS articles(
        id INTEGER PRIMARY KEY,
        title TEXT UNIQUE,
        article_url TEXT,
        text TEXT,
        publication_date TEXT,
        author TEXT,
        tags TEXT
        )""")

        self.cur.execute("""CREATE TABLE IF NOT EXISTS authors(
        id INTEGER PRIMARY KEY,
        author TEXT UNIQUE,
        job_title TEXT,
        linked_in_url TEXT,
        count_article INTEGER
        )""")

    def process_item(self, item, spider):
        """
        Choice table to insert data
        :param item: class scrapy.Item
        :param spider: class scrapy.Spider
        :return: class scrapy.Item
        """
        if spider.name == 'authors':
            self.insert_authors(item)
        elif spider.name == 'articles':
            self.insert_articles(item)
        else:
            raise NameError
        return item

    def insert_authors(self, item):
        """
        INSERT OR UPDATE data in the table 'authors'
        :param item: class scrapy.Item
        :return: None
        """
        data = (item['author'], item['job_title'], item['linked_in_url'], item['count_article'])
        self.cur.execute(
            f"""INSERT OR IGNORE INTO authors (author, job_title, linked_in_url, count_article) 
            VALUES(?, ?, ?, ?)""", data)
        self.cur.execute(
            f"""UPDATE authors SET author='{item['author']}', job_title='{item['job_title']}',
            linked_in_url='{item['linked_in_url']}', count_article='{item['count_article']}'
             WHERE author='{item['author']}'"""
        )
        self.conn.commit()

    def insert_articles(self, item):
        """
        INSERT OR UPDATE data in the table 'articles'
        :param item: class scrapy.Item
        :return: None
        """
        item['author'] = ';'.join(item['author'])
        item['tags'] = ';'.join(item['tags'])
        data = (
            item['title'], item['article_url'], item['text'],
            item['publication_date'], item['author'], item['tags'])
        data_up = (
            item['title'], item['article_url'], item['text'],
            item['publication_date'], item['author'], item['tags'], item['title'])
        self.cur.execute(
            """INSERT OR IGNORE INTO articles (title, article_url, text, publication_date, author, tags) 
            VALUES(?, ?, ?, ?, ?, ?)""", data)
        self.cur.execute(
            f"""UPDATE articles SET title=?, article_url=?,
            text=?, publication_date=?, author=?, tags=? WHERE title=?""", data_up)
        self.conn.commit()
