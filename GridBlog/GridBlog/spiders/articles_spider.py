import scrapy
from ..items import GridBlogItem


class ArticlesSpider(scrapy.Spider):
    name = "articles"
    start_urls = [
        'https://blog.griddynamics.com/',
    ]

    def parse(self, response):
        """
        Go to all links 'view more'
        :return: callback parse_link
        """
        sub_pages = response.css('.domainblock .row.regular .card:nth-child(4n)::attr(href)').getall()
        for href in sub_pages:
            yield response.follow(href, callback=self.parse_link)

    def parse_link(self, response):
        """
        Go to all articles pages
        :return: callback parse_article
        """
        all_articles_links = response.css(
            '.domainblock.cardleft .row.first a.card::attr(href)').getall() + response.css(
            '.domainblock .row.regular .card::attr(href)').getall()
        for href in all_articles_links:
            yield response.follow(href, callback=self.parse_article)

    def parse_article(self, response):
        """
        Parse the page with article
        :return: class scrapy.Item
        """
        items = GridBlogItem()
        title = response.css('h1::text').get()
        article_url = response.url
        text = response.css('p::text').get()
        if len(text) <= 160:
            text += response.css('p::text').getall()[1]
            text = text[:160]
        else:
            text = text[:160]

        publication_date = response.css('div.sdate::text').get().replace('\n', '').replace('\t', '')\
            .replace('•', '').replace(',', '')
        temp_date = publication_date.split()
        dict_month = {'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04', 'May': '05', 'Jun': '06',
                      'Jul': '07', 'Aug': '08', 'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dec': '12'}
        temp_date[0] = dict_month[f"{temp_date[0]}"]
        temp_date[0], temp_date[1] = temp_date[1], temp_date[0]
        temp_date.reverse()
        publication_date = '-'.join(temp_date)

        temp_authors = list(map(lambda x: x.strip(), response.css('body .author .sauthor .name::text').getall()))
        author = ';'.join([x for x in temp_authors if x != ''])

        meta = [x for x in response.css('meta').getall() if x.find('article:tag') != -1]
        tags = ';'.join(list(map(lambda x: x[x.find('"', x.find('content')) + 1:x.rfind('"')], meta)))
        items['title'] = title
        items['article_url'] = article_url
        items['text'] = text
        items['publication_date'] = publication_date
        items['author'] = author
        items['tags'] = tags
        yield items


