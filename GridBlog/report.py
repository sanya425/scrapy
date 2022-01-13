import subprocess
import logging
import os
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

'''
if tables exists:
    cnt = max(id_articles)
    last_date = ...
    os.system("scrapy crawl articles")
    if cnt == max(id_articles):
        print("There are no new blog posts since the last date")
    else:
        os.system("scrapy crawl authors")

else:
    process_authors = subprocess.Popen(['scrapy', 'crawl', 'authors'])
    process_articles = subprocess.Popen(['scrapy', 'crawl', 'articles'])
'''

logger.debug('start spiders')
process_authors = subprocess.Popen(['scrapy', 'crawl', 'authors'])
process_articles = subprocess.Popen(['scrapy', 'crawl', 'articles'])

process_authors.wait()
process_articles.wait()