# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class GridBlogItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    article_url = scrapy.Field()
    text = scrapy.Field()
    publication_date = scrapy.Field()
    tags = scrapy.Field()

    author = scrapy.Field()

    job_title = scrapy.Field()
    linked_in_url = scrapy.Field()
    count_article = scrapy.Field()


    article = scrapy.Field()