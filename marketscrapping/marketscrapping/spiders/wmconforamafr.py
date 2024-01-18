from typing import Iterable

import scrapy
from scrapy import Request


class WmconforamafrSpider(scrapy.Spider):
    name = "wmconforamafr"
    start_urls = ["https://www.conforama.fr/special/gros-electromenager/lavage/lave-linge/c/070101/NW-6426-type-ouverture~hublot?p=1"]


    def parse(self, response):
        
        product_links = response.css('div.awk-detail-product div.typo-paragraphe.c-r_product_name a.extendLink::attr(href)').getall()
        print(product_links)
        for i in product_links:
            yield scrapy.Request(url = i ,callback = self.parse_product)

        #Next URL will come

    def start_requests(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        for url in self.start_urls:
            yield scrapy.Request(url,headers=headers,callback=self.parse)


    def parse_product(self,response):
        pass
    