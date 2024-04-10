import scrapy


class WmaoukSpider(scrapy.Spider):
    name = "wmAOUK"
    start_urls = ["file:///C:/Users/gorkemk/PycharmProjects/Market-Search/marketscrapping/HTML%20Files/wmAOUK/page1.html"]

    def parse(self, response):
        product_urls = response.css("").getall()