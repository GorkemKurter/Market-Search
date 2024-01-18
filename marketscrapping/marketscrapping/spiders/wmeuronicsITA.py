import scrapy
import sqlite3

class WmeuronicsitaSpider(scrapy.Spider):
    name = "wmeuronicsITA"
    start_urls = ["https://www.euronics.it/elettrodomestici/grandi-elettrodomestici/lavatrici/?prefn1=tipoCarica&prefv1=Frontale"]
    i = 0

    def parse(self, response):
        product_urls = response.css("#maincontent div.container.search-results.px-0 div:nth-child(4) div:nth-child(4) div div.col-sm-12.col-md-9 div.row.product-grid div:contains('product') div div.product-tile div.tile-body div.tile-hover-hidden div.pdp-link a::attr(href)").getall()
        print(product_urls)

        for i in product_urls:
            yield scrapy.Request(url="https://www.euronics.it/" + i, callback=self.parse_product,meta = {'product_link': i})

        next_url = response.css('button.metanext::attr(data-url-full)').get()
        print("**************")
        print(next_url)
        print("**************")
        if next_url is not None:
            yield scrapy.Request(url=next_url, callback=self.parse)

    def parse_product(self, response):
        brand_name = response.css("div.product-details-js h1::text").get().split("-")[0]
        model_name = response.css("div.product-details-js h1::text").get().split("-")[1].replace("Lavatrice", '').replace(" ","",2)
        capacity = response.css("#body-technicalSpecifications > div > div > div > ul:nth-child(2) > li:nth-child(2) > span.keyMapRight::text").get().replace("\n", "").replace(",", ".")
        rpm = response.css("#body-technicalSpecifications > div > div > div > ul:nth-child(2) > li:nth-child(1) > span.keyMapRight::text").get().replace("\n", "")
        price = response.css("div.product-cart-settings div.sticky-container div.d-flex.align-items-center p::text").get().split()[1].replace(",", ".")
        currency = response.css("div.product-cart-settings div.sticky-container div.d-flex.align-items-center p::text").get().split()[0]
        product_link = response.meta.get('product_link', '')

        database_adress = r'Italian Market\washingmachines_ITA.db'
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
