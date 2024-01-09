import scrapy
import sqlite3

class WdargosukSpider(scrapy.Spider):
    name = "wdargosUK"
    start_urls = ["https://www.argos.co.uk/browse/appliances/laundry/washer-dryers/c:29613/type:freestanding-washer-dryers,integrated-washer-dryers/"]

    def parse(self, response):
        
        product_links = response.css("div.SpecCardstyles__ContentBlock-lugbee-4.hTXZJd.xs-row.xs-8--none.sm-10--none.md-8--none div.xs-12--none.sm-6--none a::attr(href)").getall()
        for i in product_links:
            yield scrapy.Request(url=response.urljoin('https://www.argos.co.uk/' + i) , callback=self.parse_product,meta = {"product_link": i})
            
        next_url = response.css("a.Paginationstyles__PageLink-sc-1temk9l-1.ifyeGc[data-test^='component-pagination-arrow-right']::attr(href)").get()
        if next_url is not None:
            yield scrapy.Request(response.urljoin(next_url), callback=self.parse)
    def parse_product(self, response):
        
        try:
            #Price operations
            price_currency = response.css("div:nth-child(2) div.xs-block div:nth-child(1) section.xs-12--none.md-5--none.xl-4--none.pdp-right  section  ul  li  h2::text").getall()
            price = price_currency[1]
            
            #Currency operations
            currency = price_currency[0]

            
            #Brand/Model Name operations
            brand_name = response.css("div.Namestyles__ProductName-sc-269llv-0.kEQsqD.bolt-v2  h1 span::text").get().split()[0]
            model_name = response.css("div.Namestyles__ProductName-sc-269llv-0.kEQsqD.bolt-v2  h1 span::text").get().split()[1]

            #Capacity operations
            capacity = response.css("div section div:nth-child(1) table tbody tr:contains('Washing Cycle Capacity (kg)') td::text").get()

            #Dry capacity operations
            capacity_dry = response.css("div  div  div:nth-child(1)  table  tbody  tr:contains('Wash and Dry Cycle Capacity (kg)') td::text").get()
        
            #RPM operations
            rpm = response.css("div section div:nth-child(1)  table  tbody  tr:contains('spin speed (rpm)') td::text").get()

            product_link = f"https://www.argos.co.uk{response.meta.get('product_link', '')}"
        except:
            print(Exception)
           
        conn = sqlite3.connect(r"C:\Users\gorkemk\PycharmProjects\Market-Search\marketscrapping\England Market\washerdryers_en.db")
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
                CAPACITY_DRY TEXT,
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
            INSERT OR IGNORE INTO washerdryers(TYPE, BRAND_NAME, MODEL_NAME, CAPACITY_WASH,CAPACITY_DRY ,RPM, PRICE, CURRENCY,PRODUCT_LINK)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', ("Washer Dryer",brand_name, model_name, capacity,capacity_dry,rpm,price,currency,product_link))

        except Exception as e:
            #print(brand_name)
            #print(model_name)
            print(f"An error occurred: {e}")
            
        conn.commit()
        conn.close()

        self.remove_duplicates(r"C:\Users\gorkemk\PycharmProjects\Market-Search\marketscrapping\England Market\washerdryers_en.db")

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
