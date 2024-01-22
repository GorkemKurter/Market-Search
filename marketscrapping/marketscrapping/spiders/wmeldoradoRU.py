import scrapy


class WmeldoradoruSpider(scrapy.Spider):
    name = "wmeldoradoRU"
    start_urls = ["https://www.eldorado.ru/c/stiralnye-mashiny/f/s-frontalnoy-zagruzkoy/?f_1629037=708115806"]

    def parse(self, response):

        product_link = response.css("#listing-container > ul > li:nth-child(1) > div.wD.yD > a::attr(href)").getall()

        for i in product_link:
            yield scrapy.Request(f"https://www.eldorado.ru{i}",callback=self.parse_product,meta={'product_link' : f"https://www.eldorado.ru{i}"})

    def parse_product(self,response):

        capacity = response.css("#cont_description > div > div.innerContainer.q-item-main-specs.no-mobile > div.aboutGoodText > div.q-specs-body > div:contains('Максимальная загрузка') > p:nth-child(2)::text").get()
        rpm = response.css("#cont_description > div > div.innerContainer.q-item-main-specs.no-mobile > div.aboutGoodText > div.q-specs-body > div:contains('Максимальная скорость отжима') > p:nth-child(2)::text").get()

        print(capacity)
        print(rpm)