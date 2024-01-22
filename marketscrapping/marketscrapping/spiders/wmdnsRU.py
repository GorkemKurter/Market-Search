import scrapy


class WmdnsruSpider(scrapy.Spider):
    name = "wmdnsRU"
    start_urls = [r"https://www.dns-shop.ru/catalog/c01df46f39137fd7/stiralnye-mashiny/?stock=now-today-tomorrow-later"]
    custom_settings = {
        'USER_AGENT' : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    }
    def parse(self, response):

        product_link = response.css("body > div.container.category-child > div > div.products-page__content > div.products-page__list > div.products-list > div > div:nth-child(2) > div > a::attr(href)").getall()

        print(product_link)