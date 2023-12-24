import scrapy


class WmmediamarktespSpider(scrapy.Spider):
    name = "wmmediamarktesp"
    allowed_domains = ["www.mediamarkt.es"]
    start_urls = ["https://www.mediamarkt.es/es/category/lavadoras-carga-frontal-672.html?enforcedReload=true"]

    def parse(self, response):
        product_urls = response.css(".div")
        #product_urls = response.css("div.sc-a5f84192-0.iBjTMh a.sc-db43135e-1.gpEOUZ.sc-748831be-0.jkrRKq::attr(href)").get(all)
        print(product_urls)
        
        