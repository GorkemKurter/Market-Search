import scrapy


class WmwortenespSpider(scrapy.Spider):
    name = "wmwortenesp"
    start_urls = ["https://www.worten.es/productos/electrodomesticos/lavado-y-cuidado-de-la-ropa/lavadoras/carga-frontal"]
    custom_settings = {
        'USER AGENT' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    def parse(self, response):

        print(response.css("div.product-card__details::text").getall())
