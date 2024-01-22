import scrapy
import sqlite3

class WmweissgauffruSpider(scrapy.Spider):
    name = "wmweissgauffru"
    start_urls = ["https://www.weissgauff.ru/catalog_815/stiral_nye_mashiny_bez_sushki.html"]

    def parse(self, response):

        product_link = response.css("#products > div > div.wrapper-products > div > div.col-md-9.col-sm-8.col-xs-12 > div.desc-list > a::attr(href)").getall()

        for i in product_link:
            yield scrapy.Request(f"https://www.weissgauff.ru/{i}",callback=self.parse_product,meta = {'product_link' : f"https://www.weissgauff.ru/{i}"})

        next_url = response.css("#page-content > div.container.clearfix > div > a.next.glyphicon.glyphicon-chevron-right::attr(href)").get()
        if next_url is not None:
            yield scrapy.Request(f"https://www.weissgauff.ru/{next_url}",callback=self.parse)

    def parse_product(self,response):

        brand_name = response.css("#page-content > div:nth-child(8) > p > span > span::text").get().split()[0]
        model_name = response.css("#page-content > div:nth-child(8) > p > span > span::text").get().split()
        model_name.pop(0)
        delimeter = " "
        model_name = delimeter.join(model_name)
        capacity = response.css("div:contains('Технические характеристики') div.product-desc.spoiler table.table.table-striped.table-hover tr:contains('Максимальная загрузка, кг:') td:nth-child(2)::text").get()
        rpm = response.css("div:contains('Технические характеристики') div.product-desc.spoiler table.table.table-striped.table-hover tr:contains('Отжим, об./мин:') td:nth-child(2)::text").get()
        price = response.css("#block-product > div:nth-child(2) > div > div.col-md-6.col-sm-12.col-xs-12.visible-xs-block.visible-sm-block > div.sm-buttons > div:nth-child(1) > div:nth-child(3) > div.font-cost::text").get().split()
        delimeter = ""
        price = delimeter.join(price)
        price = float(price) * 0.010
        price = str(price)
        currency = "€"
        product_link = response.meta.get('product_link', '')

        database_adress = r'Russian Market\washingmachines_RU.db'
        conn = sqlite3.connect(database_adress)
        cursor = conn.cursor()
        cursor.execute('SELECT name FROM sqlite_master WHERE type="table" AND name="washingmachines"')
        table_exists = cursor.fetchone()

        if not table_exists:
            cursor.execute('''
                        CREATE TABLE washingmachines(
                        user_id integer primary key not null on conflict ignore,               
                        TYPE TEXT ,
                        BRAND_NAME TEXT,
                        MODEL_NAME TEXT,
                        CAPACITY_kg TEXT,
                        RPM TEXT,
                        PRICE TEXT,
                        CURRENCY TEXT,
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
                    INSERT OR IGNORE INTO washingmachines(TYPE, BRAND_NAME, MODEL_NAME, CAPACITY_kg, RPM, PRICE, CURRENCY,PRODUCT_LINK)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    ''', ("Washing Machine", brand_name, model_name, capacity, rpm, price, currency, product_link))

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
                        DELETE FROM washingmachines
                        WHERE user_id NOT IN (
                            SELECT MIN(user_id)
                            FROM washingmachines
                            GROUP BY BRAND_NAME, MODEL_NAME , PRODUCT_LINK
                        )
                    ''')
        except Exception as e:
            print(f"An error occurred while removing duplicates: {e}")

        conn.commit()
        conn.close()
