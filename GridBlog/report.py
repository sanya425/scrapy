import subprocess
import logging
import os
import sqlite3
from sqlite3 import Error
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
logger = logging.getLogger('root')
'''
if tables exists:
    last_date = ...
    os.system("scrapy crawl articles")
    if last_date is max:
        print("There are no new blog posts since the last date")
    else:
        os.system("scrapy crawl authors")
    
else:
    process_authors = subprocess.Popen(['scrapy', 'crawl', 'authors'])
    process_articles = subprocess.Popen(['scrapy', 'crawl', 'articles'])
'''
conn = None
try:
    conn = sqlite3.connect('GDblog.db')
except Error as e:
    print(e)
cur = conn.cursor()

if cur.execute("""SELECT count(*) FROM sqlite_master WHERE type='table' AND name='table_name'"""):
    cnt = ...
    last_date = ...
    os.system("scrapy crawl articles")
    if cnt == ...:
        print("There are no new blog posts since the last date")
    else:
        os.system("scrapy crawl authors")

else:
    logger.debug('start spiders')
    process_authors = subprocess.Popen(['scrapy', 'crawl', 'authors'])
    process_articles = subprocess.Popen(['scrapy', 'crawl', 'articles'])
    process_authors.wait()
    process_articles.wait()




