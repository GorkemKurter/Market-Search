import scrapy


class WmceneoplSpider(scrapy.Spider):
    name = "wmceneoPL"
    allowed_domains = ["www.ceneo.pl"]
    start_urls = ["https://www.ceneo.pl/Pralki/Ladowanie:Od_frontu.htm"]
    custom_settings = {
        'DOWNLOAD_DELAY': 3,
        'USER_AGENT': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    def parse(self, response):

        product_link = response.css("#body > div > div > div.grid-cat__main > div > section > div.category-list-body.js_category-list-body.js_search-results.js_products-list-main.js_async-container > div > div > div.cat-prod-row__content > div.cat-prod-row__desc > div:nth-child(1) > div:nth-child(1) > strong > a::attr(href)").getall()
        for i in product_link:
            yield scrapy.Request(f"https://www.ceneo.pl{i}",callback=self.parse_product,meta={'product_link' : i})

    def parse_product(self,response):

        if response.css("div.product-top__title > h1::text").get().split()[0] == "Pralka":
            brand_name = response.css("div.product-top__title > h1::text").get().split()[1]
        else:
            brand_name = response.css("div.product-top__title > h1::text").get().split()[0]
        model_name = response.css("div.product-top__title > h1::text").get().split()[-1]
        capacity = response.css("#productTechSpecs > div:nth-child(1) > table > tbody > tr:contains('Ładowność') > td > ul > li::text").get().split()[0]
        rpm = response.css("#productTechSpecs > div:nth-child(1) > table > tbody > tr:contains('Prędkość ') > td > ul > li > a::text").get().split()[0]
        try:
            price = response.css("span.value::text").get().replace(" ","")
        except:
            price = response.css("#body > div.no-banner > div > div > article > div > div.product-top__price-column.js_column_product_offer.pointer > div > div > div.product-offer-summary__price-box.product-offer-summary__price-box--with-icon > span > span > span.value::text").get().replace(" ","")
        try:
            price_penny = response.css("span.penny::text").get().replace(",",".")
            delimeter = ""
            price = delimeter.join([price, price_penny])
        except:
            pass
        price = float(price) * 0.23
        price = str(price)
        currency = "€"
        product_link = f"https://www.ceneo.pl{response.meta.get('product_link','')}"

        print("**************************")
        print(brand_name)
        print(model_name)
        print(capacity)
        print(rpm)
        print(price)
        print(currency)
        print(product_link)
        print("**************************")