import scrapy


class WmconforamafrSpider(scrapy.Spider):
    name = "wmconforamafr"
    allowed_domains = ["www.conforama.fr"]
    start_urls = ["https://www.conforama.fr/special/gros-electromenager/lavage/lave-linge/c/070101/NW-6426-type-ouverture~hublot?p=1"]

    def parse(self, response):
        pass
