import scrapy


class WdidealoitaSpider(scrapy.Spider):
    name = "wdidealoITA"
    start_urls = ["https://www.idealo.it/cat/3959/lavasciuga.html"]

    def parse(self, response):

        product_urls = response.css("#productcategory > main > div.row.resultlist__content > div > div > section > div.sr-searchResult__resultPanel > div:nth-child(2) > div > div > div > div > a::attr(href)").getall()
        for i in product_urls:
            yield scrapy.Request(i,callback=self.parse_product,meta={'product_link': i})

    def parse_product(self,response):

        brand_name = response.css("#oopStage-title > span::text").get().split()[0]
        model_name = response.css("#oopStage-title > span::text").get().split()[1]
        capacity = response.css("#datasheet > div.datasheet-wrapper > table > tbody:contains('Capacità di carico') > tr:contains('kg') > td.datasheet-listItemValue.small-6.larger-8.columns::text").get().split()[0]
        capacity_dry = response.css("#datasheet > div.datasheet-wrapper > table > tbody:contains('Capacità di asciugatura') > tr:contains('kg') > td.datasheet-listItemValue.small-6.larger-8.columns::text").get().split()[0]
        rpm = response.css("#datasheet > div.datasheet-wrapper > table > tbody:contains('Velocità di centrifuga') > tr:nth-child(2) > td.datasheet-listItemValue.small-6.larger-8.columns::text").get().split()[0].replace(".", "")
        price = response.css("#oopStage-conditionButton-new > div > div.oopStage-conditionButton-wrapper-text > div.oopStage-conditionButton-wrapper-text-price > strong::text").get().split()[1].replace(",", ".")
        currency = response.css("#oopStage-conditionButton-new > div > div.oopStage-conditionButton-wrapper-text > div.oopStage-conditionButton-wrapper-text-price > strong::text").get().split()[0]
        product_link = response.meta.get('Product_url', '')

        print("**********************************")
        print(brand_name)
        print(model_name)
        print(capacity)
        print(capacity_dry)
        print(rpm)
        print(price)
        print(currency)
        print(product_link)
        print("**********************************")
