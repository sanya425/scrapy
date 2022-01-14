import subprocess
import logging
import os
import pandas as pd
import sqlite3
from sqlite3 import Error

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
logger = logging.getLogger('root')

conn = None
try:
    conn = sqlite3.connect('GDblog.db')
except Error as e:
    logger.error(e)
cur = conn.cursor()
'''
if cur.execute("""SELECT count(*) FROM sqlite_master WHERE type='table' AND name='table_name'""").fetchone():
    cnt = cur.execute("""SELECT MAX(id) FROM articles""").fetchone()
    logger.debug('Update articles')
    os.system("scrapy crawl articles")
    if cnt == cur.execute("""SELECT MAX(id) FROM articles""").fetchone():
        logger.debug("There are no new blog posts since the last date")
    else:
        logger.debug('There is a new article in the blog')
        logger.debug('Update authors')
        os.system("scrapy crawl authors")
        logger.debug('Authors successfully updated')

else:
    logger.debug('First start crawler')
    process_articles = subprocess.Popen(['scrapy', 'crawl', 'articles'])
    process_authors = subprocess.Popen(['scrapy', 'crawl', 'authors'])
    process_authors.wait()
    process_articles.wait()
'''
sql_articles = """SELECT title, publication_date, tags FROM articles"""
sql_authors = """SELECT author, count_article FROM authors"""
df_articles = pd.read_sql_query(sql_articles, conn)
df_authors = pd.read_sql_query(sql_authors, conn)
pd.set_option('display.max_colwidth', None)

sorted_df_authors = df_authors.sort_values(by='count_article', ascending=False)
temp_dict_authors = {k: v for k, v in zip(sorted_df_authors['author'], sorted_df_authors['count_article'])}
names = []
cnt = {}
for k, v in temp_dict_authors.items():
    if v not in cnt:
        cnt[v] = 'v'
        names.append(f"\nTOP-{len(cnt)} AUTHORS:\n")
        names.append(k + f": {v}\n")
    else:
        names.append(k + f": {v}\n")
    if len(cnt) == 5:
        break
print(*names)
print('-' * 80)

df_articles['publication_date'] = pd.to_datetime(df_articles['publication_date'])
sorted_df_articles = df_articles.sort_values(by='publication_date', ascending=False)
print('TOP-5 ARTICLES:')
print(*[x + '\n' for x in sorted_df_articles['title'].head(5)])
print('-' * 80)
print("test")

