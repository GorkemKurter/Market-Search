import scrapy


class WmweissgauffruSpider(scrapy.Spider):
    name = "wmweissgauffru"
    allowed_domains = ["www.weissgauff.ru"]
    start_urls = ["https://www.weissgauff.ru/catalog_815/stiral_nye_mashiny_bez_sushki.html"]

    def parse(self, response):
        
        brand_name = response.css("div.desc-list span.font-regular::text")
        print(brand_name)
        
        
