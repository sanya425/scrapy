import scrapy
from ..items import GridBlogItem


class ArticlesSpider(scrapy.Spider):
    name = "test_articles"
    start_urls = [
        'https://blog.griddynamics.com/',
    ]

    def parse(self, response):
        sub_pages = response.css('.domainblock .row.regular .card:nth-child(4n)::attr(href)').getall()
        for href in sub_pages:
            yield response.follow(href, callback=self.parse_articles)

    def parse_articles(self, response):
        items = GridBlogItem()
        title = response.css('h1::text').get()
        items['title'] = title
        all_articles = list(map(lambda x: x.replace('\n', ''), response.css('.domainblock .card.featured .cardbody h4.ellip2::text').getall())) +\
                       response.css('.domainblock .card .img img::attr(alt)').getall()
        z = zip(all_articles, response.css('body .author img::attr(alt)').getall()[1:])
        for article, author in z:
            items['article'] = article
            items['author'] = author
            yield items

