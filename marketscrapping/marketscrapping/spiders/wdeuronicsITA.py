import scrapy
import sqlite3

class WdeuronicsitaSpider(scrapy.Spider):
    name = "wdeuronicsITA"
    start_urls = ["https://www.euronics.it/elettrodomestici/grandi-elettrodomestici/lavasciuga/"]
    i = 0
    
    def parse(self, response):

        product_urls = response.css("#maincontent div.container.search-results.px-0 div:nth-child(4) div:nth-child(4) div div.col-sm-12.col-md-9 div.row.product-grid div:contains('product') div div.product-tile div.tile-body div.tile-hover-hidden div.pdp-link a::attr(href)").getall()
        print(product_urls)

        for i in product_urls:
            yield scrapy.Request(url="https://www.euronics.it/" + i, callback=self.parse_product)

        next_url = response.css('button.metanext::attr(data-url-full)').get()
        print("**************")
        print(next_url)
        print("**************")
        if next_url is not None:
            yield scrapy.Request(url=next_url, callback=self.parse)
            
    def parse_product(self, response):
        brand_name = response.css("div.product-details-js h1::text").get().split("-")[0]
        model_name = response.css("div.product-details-js h1::text").get().split("-")[1].replace("Lavasciuga", '').replace(" ","",2)
        capacity = response.css("#body-technicalSpecifications > div > div > div > ul:nth-child(2) > li:nth-child(2) > span.keyMapRight::text").get().replace("\n", "").replace(",", ".")
        capacity_dry = response.css("#body-technicalSpecifications > div > div > div > ul:nth-child(2) > li:nth-child(2) > span.keyMapRight::text").get().replace("\n", "").replace(",", ".")
        rpm = response.css("#body-technicalSpecifications > div > div > div > ul:nth-child(2) > li:nth-child(1) > span.keyMapRight::text").get().replace("\n", "")
        price = response.css("div.product-cart-settings div.sticky-container div.d-flex.align-items-center p::text").get().split()[1].replace(",", ".")
        currency = response.css("div.product-cart-settings div.sticky-container div.d-flex.align-items-center p::text").get().split()[0]

        #Database Operations    
        conn = sqlite3.connect('C:\\Users\\gorke\\OneDrive\\Masaüstü\\gorkem\\marketproject\\Market-Search\\marketscrapping\\Italian Market\\washerdryers_euronics_ITA.db')
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
                CURRENCY TEXT 
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
            INSERT OR IGNORE INTO washerdryers(TYPE, BRAND_NAME, MODEL_NAME, CAPACITY_WASH,CAPACITY_DRY,RPM,PRICE, CURRENCY)
            VALUES (?, ?, ?, ?, ?, ?, ?,?)
            ''', ("Washer Dryer", brand_name, model_name, capacity, capacity_dry,rpm, price,currency))

        except Exception as e:
            print(brand_name)
            print(model_name)
            cursor.execute('''
            INSERT OR IGNORE INTO washerdryers(TYPE, BRAND_NAME, MODEL_NAME, CAPACITY_WASH,CAPACITY_DRY ,RPM, PRICE, CURRENCY)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', ("Washer Dryer", brand_name, model_name, capacity, capacity_dry,rpm ,price,currency))
            print(f"An error occurred: {e}")
            
        conn.commit()
        conn.close()
        
        # Control block
        print("**************")
        print(self.i)
        print("**************")
        self.i = self.i + 1     
            
        self.remove_duplicates()

    def remove_duplicates(self):
        conn = sqlite3.connect('C:\\Users\\gorke\\OneDrive\\Masaüstü\\gorkem\\marketproject\\Market-Search\\marketscrapping\\Italian Market\\washerdryers_euronics_ITA.db')
        cursor = conn.cursor()

        try:
            cursor.execute('''
                DELETE FROM washerdryers
                WHERE user_id NOT IN (
                    SELECT MIN(user_id)
                    FROM washerdryers
                    GROUP BY BRAND_NAME, MODEL_NAME
                )
            ''')
        except Exception as e:
            print(f"An error occurred while removing duplicates: {e}")



        conn.commit()
        conn.close()








