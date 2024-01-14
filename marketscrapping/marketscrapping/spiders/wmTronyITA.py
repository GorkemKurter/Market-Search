import scrapy
import sqlite3
class WmtronyitaSpider(scrapy.Spider):
    name = "wmTronyITA"
    start_urls = ["https://www.trony.it/online/grandi-elettrodomestici/elettrodomestici/lavatrici_ct-VHJvbnktQjJDLVRyb255fHx8Mzg"]
    page_counter = 0

    def parse(self, response):

        product_urls = response.css("div.vai-alla-scheda a::attr(href)").getall()
        for i in product_urls:
            yield scrapy.Request(url=i,callback=self.parse_product,meta = {'product_link': i})

        self.page_counter = self.page_counter + 1
        print(self.page_counter)

        next_urls = response.css(f"#maincontent > div:nth-child(3) > div.col-xxs-12.col-sm-9.no-padding-mobile > div > div:nth-child(3) > div > div::attr(data-url)").getall()
        for next_url in next_urls:
            if next_url is not None:
                yield scrapy.Request(next_url,callback=self.parse)

    def parse_product(self, response):

        brand_name = response.css("#maincontent > div > div > div.schedaprodotto_presentazione_container.row > div > div.schedaprodotto_presentazione_voci_header_titolo > h1 > div.schedaprodotto_presentazione_marca::text").get()
        model_name = response.css("#maincontent > div > div > div.schedaprodotto_presentazione_container.row > div > div.schedaprodotto_presentazione_voci_header_titolo > h1 > div.schedaprodotto_presentazione_modello::text").get()
        capacity = response.css("tr:contains('Capacità max di carico in Kg:') > td.schedaprodotto_schedatecnica_testo.barra_grigia_bottom::text").get().replace(",",".")
        rpm = response.css("tr:contains('Velocità max di centrifuga (giri/min):') > td.schedaprodotto_schedatecnica_testo.barra_grigia_bottom::text").get().replace(".","").split(",")[0]
        price = response.css("#maincontent > div > div > div:nth-child(4) > div.schedaprodotto_presentazione_table_colonna3.col-xxs-12.col-sm-8 > div.schedaprodotto_presentazione_box1.row > div:nth-child(1) > div.schedaprodotto_presentazione_box1_contenuto > klarna-placement::attr(data-purchase-amount)").get()
        price = float(price)
        price = price/100
        price = str(price)
        product_link = response.meta.get('product_link', '')
        currency = response.css("#maincontent > div > div > div:nth-child(4) > div.schedaprodotto_presentazione_table_colonna3.col-xxs-12.col-sm-8 > div.schedaprodotto_presentazione_box1.row > div:nth-child(1) > div.schedaprodotto_presentazione_box1_contenuto > div.ish-priceContainer > div.ish-priceContainer-salePrice > span > span::text").get().split()[1]

        print(brand_name)
        print(model_name)
        print(capacity)
        print(rpm)
        print(price)

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
            ''', ("Washing Machine", brand_name, model_name, capacity, rpm, price,currency,product_link))

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
