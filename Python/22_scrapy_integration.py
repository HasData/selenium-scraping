# Example of Scrapy spider using scrapy-selenium
import scrapy
from scrapy_selenium import SeleniumRequest

class MySpider(scrapy.Spider):
    name = "selenium_spider"
    
    def start_requests(self):
        yield SeleniumRequest(
            url="https://example.com",
            callback=self.parse
        )

    def parse(self, response):
        title = response.css("h1::text").get()
        yield {"title": title}
