import scrapy


class WmmediamarktdeSpider(scrapy.Spider):
    name = "wmmediamarktde"
    allowed_domains = ["www.mediamarkt.de"]
    start_urls = ["https://www.mediamarkt.de/de/category/w%C3%A4sche-2.html?enforcedReload=true"]

    def parse(self, response):
        pass
