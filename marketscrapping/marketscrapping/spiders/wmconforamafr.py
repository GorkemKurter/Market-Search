import scrapy





class WmconforamafrSpider(scrapy.Spider):
    name = "wmconforamafr"
    start_urls = ["https://www.conforama.fr/special/gros-electromenager/lavage/lave-linge/c/070101/NW-6426-type-ouverture~hublot?p=1"]


    def parse(self, response):
        
        product_links = response.css('div.awk-detail-product div.typo-paragraphe.c-r_product_name a.extendLink::attr(href)').getall()
        print(product_links)
        for i in product_links:
            yield scrapy.Request(url = i ,callback = self.parse_product)

        #Next URL will come
        
    def parse_product(self,response):
        pass
    