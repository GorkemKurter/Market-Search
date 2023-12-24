import scrapy


class WmwortenespSpider(scrapy.Spider):
    name = "wmwortenesp"
    allowed_domains = ["www.worten.es"]
    start_urls = ["https://www.worten.es/productos/electrodomesticos/lavado-y-cuidado-de-la-ropa/lavadoras"]

    def parse(self, response):
        print(response.css("div.product-card__details::text").getall())
