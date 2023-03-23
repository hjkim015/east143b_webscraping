from pathlib import Path
import scrapy

class ArticlesSpider(scrapy.Spider):
    name = "articles"

    def start_requests(self):
        urls = [f'https://www.japantimes.co.jp/news/world/page/{page_num}/' 
                for page_num in range(12, 46)]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
    
    def parse_article(self, url):
        

    def parse(self, response):
        for article in response.css('article'):
            url = article.css('header p a::attr(href)').get()
            yield {
                'title': article.css('header p a::text').get(),
                'author': article.css('header h5 a::text').get(),
                'date': article.css('header span::text').getall(),
                'content': response.follow(url, callback=self.parse_article)
            }
        


        #Gets all the source code of the urls 
        # page = response.url.split("/")[-2]
        # filename = f'articles-{page}.html'
        # Path(filename).write_bytes(response.body)
        # self.log(f'Saved file {filename}')