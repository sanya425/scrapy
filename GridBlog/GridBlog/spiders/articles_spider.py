import scrapy
from ..items import GridBlogItem


class ArticlesSpider(scrapy.Spider):
    name = "articles"
    start_urls = [
        'https://blog.griddynamics.com/',
    ]

    def parse(self, response):
        sub_pages = response.css('.domainblock .row.regular .card:nth-child(4n)::attr(href)').getall()
        for href in sub_pages:
            yield response.follow(href, callback=self.parse_link)

    def parse_link(self, response):
        all_articles_links = response.css(
            '.domainblock.cardleft .row.first a.card::attr(href)').getall() + response.css(
            '.domainblock .row.regular .card::attr(href)').getall()
        for href in all_articles_links:
            yield response.follow(href, callback=self.parse_article)

    def parse_article(self, response):
        items = GridBlogItem()
        title = response.css('h1::text').get()
        article_url = response.url
        text = response.css('p::text').get()
        if len(text) <= 160:
            text += response.css('p::text').getall()[1]
            text = text[:160]
        else:
            text = text[:160]
        publication_date = response.css('div.sdate::text').get().replace('\n', '').replace('\t', '').replace('•', '')
        temp_authors = list(map(lambda x: x.strip(), response.css('body .author .sauthor .name::text').getall()))
        author = [x for x in temp_authors if x != '']
        meta = [x for x in response.css('meta').getall() if x.find('article:tag') != -1]
        tags = list(map(lambda x: x[x.find('"', x.find('content')) + 1:x.rfind('"')], meta))
        items['title'] = title
        items['article_url'] = article_url
        items['text'] = text
        items['publication_date'] = publication_date
        items['author'] = author
        items['tags'] = tags
        yield items


