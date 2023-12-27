import scrapy


class WmpricespyukSpider(scrapy.Spider):
    name = "wmpricespyUK"
    start_urls = ["https://pricespy.co.uk/c/washing-machines?1247=2342"]

    def parse(self, response):
        
        product_links = response.css("div  section  div.Content-sc-2fu3f8-2.bugHkt  div  div  div article  a::attr(href)").getall()
        '''for i in range(len(product_links)):
            if i == "/":
                product_links.pop(i)'''
        print(product_links)
        print("******************************")
        for i in product_links:
            yield scrapy.Request(url=("https://pricespy.co.uk/" + i + "#properties") ,callback = self.parse_product)

#\#properties > div > section > section > div > div > div.hideInViewports-sc-0-0.iwivxM > div > section > div:nth-child(2) > div:nth-child(2) > span
        
    def parse_product(self, response):
        
        brand_name =  response.css('div  section  section  div div section span  a::text').get()
        model_name = response.css("div  section  section  div  div.hideInViewports-sc-0-0.iwivxM").get()      
        #model_name = response.css("div div section div div.SectionWrapper-sc-ia0zhw-0.bqrwQK section div.StyledList--1mpttw7.czBGBu.StyledPanel--lryowj.llXyJQ div div:nth-child(2) div.Column-sc-0-2.kMCFmk span.Text--o69vef.gLKIHP.bodysmalltext.PropertyValue-sc-0-6.guNUSr::text").getall()
#\#properties > div > section > section > div > div > div.hideInViewports-sc-0-0.iwivxM > div > section > div:nth-child(2) > div:nth-child(2) > span        
        print(brand_name)
        print(model_name)
        
