import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

class WmtronyitaSpider(scrapy.Spider):
    name = "wmTronyITA"
    start_urls = ["https://www.trony.it/online/grandi-elettrodomestici/elettrodomestici/lavatrici_ct-VHJvbnktQjJDLVRyb255fHx8Mzg"]
    page_counter = 0

    def parse(self, response):

        product_urls = response.css("div.vai-alla-scheda a::attr(href)").getall()
        for i in product_urls:
            yield scrapy.Request(url=i,callback=self.parse_product,meta = {'Product link':i})

        self.page_counter = self.page_counter + 1

        next_urls = response.css("#maincontent > div:nth-child(3) > div.col-xxs-12.col-sm-9.no-padding-mobile > div > div:nth-child(3) > div > div:nth-child(1)::attr(data-url)").get()
        #url_counter = response.css("#maincontent > div:nth-child(3) > div.col-xxs-12.col-sm-9.no-padding-mobile > div > div:nth-child(3) > div > div::attr(data-url)").getall()
        try:
                yield scrapy.Request(url = next_urls[self.page_counter],callback=self.parse)
        except:
            print("finished")

    def parse_product(self, response):

        brand_name = response.css("#maincontent > div > div > div.schedaprodotto_presentazione_container.row > div > div.schedaprodotto_presentazione_voci_header_titolo > h1 > div.schedaprodotto_presentazione_marca::text").get()
        model_name = response.css("#maincontent > div > div > div.schedaprodotto_presentazione_container.row > div > div.schedaprodotto_presentazione_voci_header_titolo > h1 > div.schedaprodotto_presentazione_modello::text").get()
        capacity = response.css("tr:nth-child(2) > td.schedaprodotto_schedatecnica_testo.barra_grigia_bottom::text").get().replace(",",".")
        rpm = response.css("tr:nth-child(3) > td.schedaprodotto_schedatecnica_testo.barra_grigia_bottom::text").get().replace(".","").split(",")[0]
