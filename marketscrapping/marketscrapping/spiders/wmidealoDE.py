import scrapy


class WmidealodeSpider(scrapy.Spider):
    name = "wmidealoDE"
    allowed_domains = ["www.idealo.de"]
    start_urls = ["https://www.idealo.de/preisvergleich/ProductCategory/1941F1201412.html"]

    def parse(self, response):

        product_links = response.css("#productcategory > main > div.row.resultlist__content > div > div > section > div.sr-searchResult__resultPanel > div:nth-child(2) > div > div > div > div > a::attr(href)").getall()
        for i in product_links:
            yield scrapy.Request(i,callback=self.parse_product,meta={'product_link': i})

    def parse_product(self,response):

        capacity = response.css("#datasheet > div.datasheet-wrapper > table > tbody:contains('Füllmenge') > tr:contains('kg') > td.datasheet-listItemValue.small-6.larger-8.columns::text").get().split()[0]
        rpm = response.css("#datasheet > div.datasheet-wrapper > table > tbody:contains('Schleuderdrehzahl') > tr:contains('U/min') > td.datasheet-listItemKey.small-6.larger-8.columns::text").get()
#datasheet > div.datasheet-wrapper > table > tbody:nth-child(3) > tr:nth-child(2) > td.datasheet-listItemValue.small-6.larger-8.columns