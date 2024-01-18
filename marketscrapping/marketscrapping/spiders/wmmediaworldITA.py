import scrapy


class WmmediaworlditaSpider(scrapy.Spider):
    name = "wmmediaworldITA"
    start_urls = ["https://www.mediaworld.it/it/category/lavatrici-carica-frontale-600101.html"]
    custom_settings = {
        'USER_AGENT' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

    def parse(self, response):

        product_urls = response.css("#main-content > div.sc-89725820-0.fqRTWa > div.sc-f9f83eec-0.dkSVao > div.sc-835d3f28-0.kTdeVZ > div > div.sc-2469269c-0.hxVJgr > div > div > div > div > a::attr(href)").getall()
        for i in product_urls:
            yield scrapy.Request(f"https://www.mediaworld.it{i}",callback=self.parse_product)

    def parse_product(self,response):

        brand_name = response.css("#description-content > div.sc-f1f881c4-0.evTnGL.sc-b292c3cd-0.eXcgpL > b:nth-child(1)::text").get().split()[0]
        model_name = response.css("#description-content > div.sc-f1f881c4-0.evTnGL.sc-b292c3cd-0.eXcgpL > b:nth-child(1)::text").get().split()[1]
        capacity = response.css("#features-content > div > table:nth-child(1) > tbody > tr:nth-child(1) > td.sc-27ebc524-0.ca-dqbf.sc-c0c3f7bd-1.bMxfiq > p::text").get()
        rpm = response.css("#features-content > div > table:nth-child(6) > tbody > tr:nth-child(6) > td.sc-27ebc524-0.ca-dqbf.sc-c0c3f7bd-1.bMxfiq > p::text").get()

        print(brand_name)
        print(model_name)
        print(capacity)
        print(rpm)