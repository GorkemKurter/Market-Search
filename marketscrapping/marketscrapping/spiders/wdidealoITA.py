import scrapy
import sqlite3

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

        # Database Operations
        database_adress = r"Italian Market\washerdryers_ITA.db"
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
            print(brand_name)
            print(model_name)
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

