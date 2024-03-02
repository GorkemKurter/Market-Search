import scrapy
import sqlite3

class WmmediamarktdeSpider(scrapy.Spider):
    name = "wmmediamarktde"
    start_urls = ["file:///C:/Users/gorkemk/PycharmProjects/Market-Search/marketscrapping/HTML%20Files/wmmediamarktDE/page1.html"]
    page_counter = 1
    def parse(self, response):

        product_urls = response.css("#main-content > div.sc-89725820-0.fqRTWa > div.sc-f9f83eec-0.dkSVao > div.sc-835d3f28-0.kTdeVZ > div > div.sc-572c0887-0.oLQeQ > div > div > div > div > a::attr(href)").getall()

        for i in range(len(product_urls)):
            try:
                product_link = response.css(f"#main-content > div.sc-89725820-0.fqRTWa > div.sc-f9f83eec-0.dkSVao > div.sc-835d3f28-0.kTdeVZ > div > div.sc-572c0887-0.oLQeQ > div:nth-child({i}) > div > div > div > a::attr(href)").get()
                product_link = f"https://www.mediamarkt.de{product_link}"
                print(product_link)
                brand_name = response.css(f"#main-content > div.sc-89725820-0.fqRTWa > div.sc-f9f83eec-0.dkSVao > div.sc-835d3f28-0.kTdeVZ > div > div.sc-572c0887-0.oLQeQ > div:nth-child({i}) > div > div > div > a > div > p::text").get().split()[0]
                print(brand_name)
                model_name = response.css(f"#main-content > div.sc-89725820-0.fqRTWa > div.sc-f9f83eec-0.dkSVao > div.sc-835d3f28-0.kTdeVZ > div > div.sc-572c0887-0.oLQeQ > div:nth-child({i}) > div > div > div > a > div > p::text").get().split()[1]
                print(model_name)
                capacity = response.css(f"#main-content > div.sc-89725820-0.fqRTWa > div.sc-f9f83eec-0.dkSVao > div.sc-835d3f28-0.kTdeVZ > div > div.sc-572c0887-0.oLQeQ > div:nth-child({i}) > div > div > div > a > div > p::text").get().split("(")[-1].replace(")","").split(",")[0].replace(" kg","")
                print(capacity)
                rpm = response.css(f"#main-content > div.sc-89725820-0.fqRTWa > div.sc-f9f83eec-0.dkSVao > div.sc-835d3f28-0.kTdeVZ > div > div.sc-572c0887-0.oLQeQ > div:nth-child({i}) > div > div > div > a > div > p::text").get().split("(")[-1].replace(")","").split(",")[1].replace(" U/Min.","").replace(" ","")
                print(rpm)
                try:
                    price = response.css(f"#main-content > div.sc-89725820-0.fqRTWa > div.sc-f9f83eec-0.dkSVao > div.sc-835d3f28-0.kTdeVZ > div > div.sc-572c0887-0.oLQeQ > div:nth-child({i}) > div > div > div > div.sc-b038b935-0.gWqOnR > div > div > div.sc-c5b05e03-0.qDWjW > span.sc-f1f881c4-0.iuwhod.sc-fd36c0ef-2.ccimAO::text").get().split()[0].replace(",",".").replace("–","")
                    print(price)
                except Exception as e:
                    price = response.css(f"#main-content > div.sc-89725820-0.fqRTWa > div.sc-f9f83eec-0.dkSVao > div.sc-835d3f28-0.kTdeVZ > div > div.sc-572c0887-0.oLQeQ > div:nth-child({i}) > div > div > div > div.sc-b038b935-0.gWqOnR > div > div > div.sc-c5b05e03-0.qDWjW > span.sc-f1f881c4-0.eDRAfL.sc-fd36c0ef-2.ccimAO::text").get().split()[0].replace(",",".").replace("–","")
                    print(e)
                currency = response.css(f"#main-content > div.sc-89725820-0.fqRTWa > div.sc-f9f83eec-0.dkSVao > div.sc-835d3f28-0.kTdeVZ > div > div.sc-572c0887-0.oLQeQ > div:nth-child({i}) > div > div > div > div.sc-b038b935-0.gWqOnR > div > div > div.sc-c5b05e03-0.qDWjW > span.sc-f1f881c4-0.iuwhod.sc-fd36c0ef-2.ccimAO::text").get().split()[1]
                print(currency)

                #Database Ops.

                database_adress = r'German Market\washingmachines_DE.db'
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
        next_url = fr"file:///C:/Users/gorkemk/PycharmProjects/Market-Search/marketscrapping/HTML%20Files/wmmediamarktDE/page{self.page_counter}.html"
        if next_url is not None:
            yield scrapy.Request(url=next_url,callback=self.parse)


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

