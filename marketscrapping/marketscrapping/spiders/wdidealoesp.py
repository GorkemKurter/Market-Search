import scrapy
import sqlite3

class WdidealoespSpider(scrapy.Spider):
    name = "wdidealoesp"
    allowed_domains = ["www.idealo.es"]
    start_urls = ["https://www.idealo.es/cat/3959/lavadoras-secadoras.html"]

    def parse(self, response):

        prodcut_link = response.css('#productcategory > main > div.row.resultlist__content > div > div > section > div.sr-searchResult__resultPanel > div:nth-child(2) > div > div > div > div > a::attr(href)').getall()

        for i in prodcut_link:
            yield scrapy.Request(i,callback=self.parse_product,meta={'product_link': i})

        next_url = response.css('#productcategory > main > div.row.resultlist__content > div > div > section > div.sr-searchResult__resultPanel > div.sr-pagination > a.sr-pageArrow::attr(href)').get()
        if next_url is not None:
            yield scrapy.Request(next_url,callback=self.parse)

    def parse_product(self,response):

        brand_name = response.css('#oopStage-title > span::text').get().split()[0]
        model_name = response.css('#oopStage-title > span::text').get().split()[1]
        capacity = response.css("#datasheet > div.datasheet-wrapper > table > tbody:contains('Capacidad de lavado') > tr:contains('Capacidad de lavado') > td.datasheet-listItemValue.small-6.larger-8.columns::text").get().split()[0]
        capacity_dry = response.css("#datasheet > div.datasheet-wrapper > table > tbody:contains('Capacidad de secado') > tr:contains('Capacidad de secado') > td.datasheet-listItemValue.small-6.larger-8.columns::text").get().split()[0]
        rpm = response.css("#datasheet > div.datasheet-wrapper > table > tbody:contains('Velocidad de centrifugado') > tr:contains('Velocidad de centrifugado') > td.datasheet-listItemValue.small-6.larger-8.columns::text").get()
        if rpm is None or rpm == "":
            rpm = response.css("#datasheet > div.datasheet-wrapper > table > tbody:contains('Velocidad de centrifugado') > tr:contains('Velocidad de centrifugado') > td.datasheet-listItemValue.small-6.larger-8.columns::text").get().split()[0].replace(".","")
        else:
            rpm = response.css("#datasheet > div.datasheet-wrapper > table > tbody:contains('Velocidad de centrifugado') > tr:contains('Velocidad de centrifugado') > td.datasheet-listItemValue.small-6.larger-8.columns::text").get().split()[0].replace(".","")
        price = response.css("#oopStage-conditionButton-new > div > div.oopStage-conditionButton-wrapper-text > div.oopStage-conditionButton-wrapper-text-price > strong::text").get().split()[0].replace(",",".")
        currency = response.css("#oopStage-conditionButton-new > div > div.oopStage-conditionButton-wrapper-text > div.oopStage-conditionButton-wrapper-text-price > strong::text").get().split()[1]
        product_link = response.meta.get('product_link','')

        database_adress = r"Spanish Market\washerdryers_ESP.db"
        conn = sqlite3.connect(database_adress)
        cursor = conn.cursor()
        cursor.execute('SELECT name FROM sqlite_master WHERE type="table" AND name="washerdryers"')
        table_exists = cursor.fetchone()

        if not table_exists:
            cursor.execute('''
                    CREATE TABLE washerdryers(
                    user_id integer primary key not null on conflict ignore,               
                    TYPE TEXT ,
                    BRAND_NAME TEXT,
                    MODEL_NAME TEXT,
                    CAPACITY_WASH TEXT,
                    CAPACITY_DRY TEXT ,
                    RPM TEXT,
                    PRICE TEXT,
                    CURRENCY TEXT ,
                    PRODUCT_LINK
                    )  
                    ''')

        valid_combinations = [
            (6, 1000), (6, 1200), (6, 1400),
            (7, 1000), (7, 1200), (7, 1400),
            (8, 1000), (8, 1200), (8, 1400), (8, 1600),
            (9, 1000), (9, 1200), (9, 1400),
            (10, 1200), (10, 1400)
        ]

        try:
            current_combination = (float(capacity), float(rpm))
            if current_combination in valid_combinations:
                cursor.execute('''
                INSERT OR IGNORE INTO washerdryers(TYPE, BRAND_NAME, MODEL_NAME, CAPACITY_WASH,CAPACITY_DRY , RPM, PRICE, CURRENCY,PRODUCT_LINK)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                "Washer Dryer", brand_name, model_name, capacity, capacity_dry, rpm, price, currency, product_link))

        except Exception as e:
            print(f"An error occurred: {e}")

        conn.commit()
        conn.close()

        self.remove_duplicates(database_adress)

    def remove_duplicates(self, adress):
        conn = sqlite3.connect(adress)
        cursor = conn.cursor()

        try:
            cursor.execute('''
                    DELETE FROM washerdryers
                    WHERE user_id NOT IN (
                        SELECT MIN(user_id)
                        FROM washerdryers
                        GROUP BY BRAND_NAME, MODEL_NAME , PRODUCT_LINK
                    )
                ''')
        except Exception as e:
            print(f"An error occurred while removing duplicates: {e}")

        conn.commit()
        conn.close()




