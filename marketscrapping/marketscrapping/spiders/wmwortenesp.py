import scrapy
import sqlite3

class WmwortenespSpider(scrapy.Spider):
    name = "wmwortenesp"
    start_urls = ["file:///C:/Users/gorkemk/PycharmProjects/Market-Search/marketscrapping/HTML%20Files/wmwortensesp/page1.html"]
    page_counter = 1
    product_counter = 0
    def parse(self, response):

        product_urls = response.css("#filtered-grid > div > div > section > div > div > ul > li > div > a::attr(href)").getall()
        for i in range(2, 2*len(product_urls)+1,2):
            try:
                product_link = response.css(f"#filtered-grid > div > div > section > div > div > ul > li:nth-child({i}) > div > a::attr(href)").get()
                if response.css(f"#filtered-grid > div > div > section > div > div > ul > li:nth-child({i}) > div > a > div > div.product-card__text-container > div.product-card__details > div.product-card__name-and-features > h3 > span::text").get() == None:
                    label = response.css(f"#filtered-grid > div > div > section > div > div > ul > li:nth-child({i}) > div > a > div > div.product-card__text-container--sponsored.product-card__text-container > div.product-card__details > div.product-card__name-and-features > h3 > span::text").get()
                else:
                    label = response.css(f"#filtered-grid > div > div > section > div > div > ul > li:nth-child({i}) > div > a > div > div.product-card__text-container > div.product-card__details > div.product-card__name-and-features > h3 > span::text").get()

                brand_name = label.split()[1]
                model_name = label.split("(")[0].split()[-1]
                capacity = label.split("(")[1].split("-")[0].replace("kg","").replace(" ","")
                rpm = label.split("(")[1].split("-")[1].replace("rpm","").replace(" ","")
                if response.css(f"#filtered-grid > div > div > section > div > div > ul > li:nth-child({i}) .integer::text").get() == None:
                    price_left = response.css(f"#filtered-grid > div > div > section > div > div > ul > li:nth-child({i}) > div > a > div > div.product-card__text-container > span > span > span > span::text").get()
                else:
                    price_left = response.css(f"#filtered-grid > div > div > section > div > div > ul > li:nth-child({i}) .integer::text").get()
                if response.css(f"#filtered-grid > div > div > section > div > div > ul > li:nth-child({i}) .decimal::text").get() == None:
                    price_right = response.css(f"#filtered-grid > div > div > section > div > div > ul > li:nth-child({i}) > div > a > div > div.product-card__text-container > span > span > span > sup::text").get()
                else:
                    price_right = response.css(f"#filtered-grid > div > div > section > div > div > ul > li:nth-child({i}) .decimal::text").get()
                price = ",".join([price_left,price_right])
                currency = "€"
                self.product_counter += 1
                print("****************************")
                print(self.product_counter)
                print(product_link)
                print(model_name)
                print(brand_name)
                print(capacity)
                print(rpm)
                print(price)
                print(currency)
                print("****************************")

                database_adress = r'Spanish Market\washingmachines_ESP.db'
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

            except Exception as e:
                print(e)


        self.page_counter += 1
        next_url = fr"file:///C:/Users/gorkemk/PycharmProjects/Market-Search/marketscrapping/HTML%20Files/wmwortensesp/page{self.page_counter}.html"
        if next_url is not None:
            yield scrapy.Request(next_url,callback=self.parse)

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
