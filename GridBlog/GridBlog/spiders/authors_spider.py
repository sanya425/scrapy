import scrapy
from ..items import GridBlogItem


class AuthorsSpider(scrapy.Spider):
    name = "authors"
    start_urls = [
        'https://blog.griddynamics.com/all-authors/',
    ]

    def parse(self, response):
        view_more = response.css('.authorcard .postsrow .row.viewmore a::attr(href)').getall()
        for href in view_more:
            yield response.follow(href, callback=self.parse_author)

    def parse_author(self, response):
        items = GridBlogItem()
        author = response.css('body.authors.author .modalbg .authorcard.popup h3::text').get()
        linked_in_url = response.css('body.authors.author .modalbg .authorcard.popup li.socicon a::attr(href)').get()
        job_title = response.css('body.authors.author .modalbg .authorcard.popup p.jobtitle::text').get()
        count_article = len(response.css('body.authors.author .modalbg .authorcard .postsrow .row a::text').getall())
        baned_words = ['Kharkiv', 'Ukrain', 'Lviv', 'Belgrade', 'Serbia', 'Petersburg', 'Saratov', 'Russia', 'Atlanta',
                       'Belgrade', 'Moscow', 'Krakow', 'California']

        if sum(map(lambda x: str(job_title).find(x), baned_words.copy())) != -len(baned_words):
            job_title = None

        items['linked_in_url'] = linked_in_url
        items['job_title'] = job_title
        items['author'] = author
        items['count_article'] = count_article
        yield items


