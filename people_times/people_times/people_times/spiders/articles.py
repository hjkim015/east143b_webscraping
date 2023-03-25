from pathlib import Path
import scrapy
import datetime

class ArticlesSpider(scrapy.Spider):
    name = "articles"
    base = 'http://en.people.cn'

    def start_requests(self):
        urls = [f'http://en.people.cn/90777/index{page_num}.html' 
                for page_num in range(21, 63)]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    
    def parse(self, response):
        #Gets the specific link for an article, which is just a class
        for article_link in response.css('div.foreign_d2list ul.foreign_list8 li a::attr(href)').getall(): 
            yield response.follow(self.base + article_link, callback=self.parse_article)
        

    def parse_article(self, response):
        yield {
            'title': response.css('h1::text').get(),
            'author': response.css('div.origin a::text').get(),
            'date': response.css('div.origin span::text').get(),
            'content': ' '.join(response.css('p::text').getall()).replace('\n','').replace('\t', '')
        }
