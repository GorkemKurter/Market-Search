import scrapy


class WmidealoespSpider(scrapy.Spider):
    name = "wmidealoesp"
    start_urls = ["https://www.idealo.es/cat/1941F2613506/lavadoras.html"]

    def parse(self, response):
        
        brand_name = response.css("div.productSummary__title::text")
        print(brand_name)
