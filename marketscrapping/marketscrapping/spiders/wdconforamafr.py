import scrapy
import sqlite3
import re

class WdconforamafrSpider(scrapy.Spider):
    name = "wdconforamafr"
    allowed_domains = ["www.conforama.fr"]
    start_urls = ["file:///C:/Users/gorkemk/PycharmProjects/Market-Search/marketscrapping/HTML%20Files/wdconforama/page1.html"]
    page_counter = 0
    counter = 0

    def parse(self, response):

        product_urls = response.css(
            "#addToCartForm > div.column-product.column-product_middle > div.awk-detail-product > div.typo-paragraphe.c-r_product_name > a::attr(href)").getall()

        for i in range(len(product_urls)):
            try:
                if response.css(f"#contentSegment > div.c-r_descent-container > div > article:nth-child({i}) div.awk-desc-product.product-pointfort li:nth-child(1) span::text").get() == None:
                    brand_name = response.css(f"#contentSegment > div.c-r_descent-container > div > article:nth-child({i}) a.extendLink div.c-r_refProductName-grp span::text").get().split()[0]
                    template_string = response.css(f"#contentSegment > div.c-r_descent-container > div > article:nth-child({i}) a.extendLink div.c-r_refProductName-grp span::text").get()
                    model_name = self.parse_product_info_details(template_string)[2]
                    capacity = self.parse_product_info_details(template_string)[0]
                    drying_capacity_match = re.search(r'séchage\s*(\d+)\s*kg', template_string)
                    capacity_dry = drying_capacity_match.group(1) if drying_capacity_match else None
                    rpm = self.parse_product_info_details(template_string)[1]
                    price = ".".join([response.css(f"#contentSegment > div.c-r_descent-container > div > article:nth-child({i}) div.wrapper-price div.wrapper-price_int::text").get().replace(" ", ""), response.css(f"#contentSegment > div.c-r_descent-container > div > article:nth-child({i}) div.wrapper-price span.wrapper-price_cent::text").get().replace(" ", "").replace("€", "")])
                    currency = "€"
                    product_link = response.css(f"#contentSegment > div.c-r_descent-container > div > article:nth-child({i}) a.extendLink::attr(href)").get()
                else:
                    brand_name = response.css(f"#contentSegment > div.c-r_descent-container > div > article:nth-child({i}) a.extendLink div:nth-child(2) span::text").get().split()[0]
                    model_name = response.css(f"#contentSegment > div.c-r_descent-container > div > article:nth-child({i}) a.extendLink div:nth-child(2) span::text").get().split()[1]
                    capacity_temp = response.css(f"#contentSegment > div.c-r_descent-container > div > article:nth-child(8) div.awk-desc-product.product-pointfort li:nth-child(1) span::text").get()
                    capacity = self.parse_product_info(capacity_temp.split(",")[0])
                    drying_capacity_match = re.search(r'séchage\s*(\d+)\s*kg', capacity_temp)
                    capacity_dry = drying_capacity_match.group(1) if drying_capacity_match else None
                    rpm = response.css(f"#contentSegment > div.c-r_descent-container > div > article:nth-child({i}) div.awk-desc-product.product-pointfort li:nth-child(2) span::text").get()
                    rpm = self.parse_product_info(rpm)[1]
                    price = ".".join([response.css(f"#contentSegment > div.c-r_descent-container > div > article:nth-child({i}) div.wrapper-price div.wrapper-price_int::text").get().replace(" ", ""), response.css(f"#contentSegment > div.c-r_descent-container > div > article:nth-child({i}) div.wrapper-price span.wrapper-price_cent::text").get().replace(" ", "").replace("€", "")])
                    currency = "€"
                    product_link = response.css(f"#contentSegment > div.c-r_descent-container > div > article:nth-child({i}) a.extendLink::attr(href)").get()

                print("********************")
                print(product_link)
                print(brand_name)
                print(model_name)
                print(capacity)
                print(capacity_dry)
                print(rpm)
                print(price)
                self.counter += 1
                print(self.counter)
                print("********************")

                # Database Ops.

                database_adress = r'French Market\washerdryers_fr3.db'
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
                            ''', (
                        "Washing Machine", brand_name, model_name, capacity, rpm, price, currency, product_link))

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
        next_url = fr"file:///C:/Users/gorkemk/PycharmProjects/Market-Search/marketscrapping/HTML%20Files/wdconforama/page{self.page_counter}.html"
        if next_url is not None:
            yield scrapy.Request(url=next_url, callback=self.parse)

    def parse_product_info(self, product_str):
        kilogram_regex = re.compile(r'(\d+(\.\d+)?)\s*kg')
        rpm_regex = re.compile(r'(\d+(\.\d+)?)\s* trs/')
        kilogram_match = kilogram_regex.search(product_str)
        if kilogram_match:
            kilogram = float(kilogram_match.group(1))
        else:
            kilogram = None

        rpm_match = rpm_regex.search(product_str)
        if rpm_match:
            rpm = float(rpm_match.group(1))
        else:
            rpm = None
        model_match = re.search(r'\s(\S+\s*-?\w*)\s*trs/', product_str)
        if model_match:
            model_name = model_match.group(1)
        else:
            model_name = None

        return kilogram, rpm, model_name

    def parse_product_info_details(self, product_str):
        kilogram_regex = re.compile(r'(\d+(\.\d+)?)\s*kg')
        rpm_regex = re.compile(r'(\d+(\.\d+)?)\s* tours/')
        kilogram_match = kilogram_regex.search(product_str)
        if kilogram_match:
            kilogram = float(kilogram_match.group(1))
        else:
            kilogram = None

        rpm_match = rpm_regex.search(product_str)
        if rpm_match:
            rpm = float(rpm_match.group(1))
        else:
            rpm = None
        model_match = re.search(r'\s(\S+\s*-?\w*)\s*tours/', product_str)
        if model_match:
            model_name = model_match.group(1)
        else:
            model_name = None

        return kilogram, rpm, model_name

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

