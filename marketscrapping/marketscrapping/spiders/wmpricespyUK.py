import scrapy
import sys

class WmpricespyukSpider(scrapy.Spider):
    name = "wmpricespyUK"
    start_urls = ["https://pricespy.co.uk/c/washing-machines?1247=2342"]

    def parse(self, response):
        
        product_links = response.css("div  section  div.Content-sc-2fu3f8-2.bugHkt  div  div  div    article  a::attr(href)").getall()
        '''for i in range(len(product_links)):
            if i == "/":
                product_links.pop(i)'''
        print(product_links)
        print("******************************")
        for i in product_links:
            yield scrapy.Request(url=response.urljoin('https://pricespy.co.uk/' + i) ,callback = self.parse_product)
        
#root > div > section > div.Content-sc-2fu3f8-2.bugHkt > div > div > div > div.ProductsWrapper-sc-r7ueb4-0.iNYtxu > section > main > div > ul > li:nth-child(30) > article > a
#root > div > section > div.Content-sc-2fu3f8-2.bugHkt > div > div > div > div.ProductsWrapper-sc-r7ueb4-0.iNYtxu > section > main > div > ul > li:nth-child(4) > article > a
        
    def parse_product(self, response):
        
        brand_name =  response.css('div  section  section  div div section span  a::text ').get()
        print(brand_name)
        
        pass
