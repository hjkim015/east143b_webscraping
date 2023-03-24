from pathlib import Path
import scrapy
import datetime

class ArticlesSpider(scrapy.Spider):
    name = "articles"
    start_url = 'https://www.japantimes.co.jp/news/world/page/1/'

    def start_requests(self):
        urls = [f'https://www.japantimes.co.jp/news/world/page/{page_num}/' 
                for page_num in range(13, 45)]
        # urls = ['https://www.japantimes.co.jp/news/world/page/12/']

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    
    def parse(self, response):
        #Calls the parse_article function for each article link 
        for article_link in response.css('article header p a[href]'):
            yield response.follow(article_link, callback=self.parse_article)
        

    def parse_article(self, response):
        yield {
            'title': response.xpath("//title/text()").get(),
            'author': response.xpath("//meta[@name='author']/@content").get(),
            'date': response.xpath("//time/text()").get().strip(),
            'content': response.css('.entry p::text').get()
        }
    

        #Gets all the source code of the urls 
        # page = response.url.split("/")[-2]
        # filename = f'articles-{page}.html'
        # Path(filename).write_bytes(response.body)
        # self.log(f'Saved file {filename}')