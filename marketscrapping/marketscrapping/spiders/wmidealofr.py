import scrapy
import sqlite3
import json

class WmidealofrSpider(scrapy.Spider):
    name = "wmidealofr"
    start_urls = ["https://www.idealo.fr/cat/1941F1203607/lave-linge.html"]
    page_number = 1
    item_number = 1

    def parse(self, response):
        products_links = []
        a_links = response.css("div.sr-resultItemLink a::attr(href)").getall()
        buttons = response.css("button.resultItemLink__button")

        temp_button_list = [button.css('::attr(data-gtm-payload)').get() for button in buttons]
        products_links_dict_list = []
        for json_string in temp_button_list:
            dict_value = json.loads(json_string)
            products_links_dict_list.append(dict_value)
        product_links_button = []
        for product_id in products_links_dict_list:
            product_links_button.append(f"https://www.idealo.fr/prix/{product_id.get('productId')}")


        products_links = a_links + product_links_button
        for i in products_links:
            self.item_number = self.item_number + 1
            print("////////////////////////////////////////////////////////////")
            print(self.item_number)
            print("////////////////////////////////////////////////////////////")
            yield scrapy.Request(url = i ,callback = self.parse_product,meta={'product_link': i})



        next_url = response.css('#productcategory > main > div.row.resultlist__content > div > div > section > div.sr-searchResult__resultPanel > div.sr-pagination > a.sr-pageArrow::attr(href)').get()
        if next_url is not None:
            self.page_number = self.page_number + 1
            print("############################################################")
            print(self.page_number)
            print("############################################################")
            yield scrapy.Request(response.urljoin(next_url), callback=self.parse)

        

    def parse_product(self,response):
        print(response.meta.get('product_link', ''))
        print("***********************")

        try :
            brand_name_temp = response.css("h1.oopStage-title span::text").get()
            brand_name = brand_name_temp.split()[0]
            model_name = brand_name_temp.split()[-1]
            capacity = response.css('tr.datasheet-listItem--properties td.datasheet-listItemKey:contains("Capacité") + td.datasheet-listItemValue::text').get().strip().replace('\n', '').replace('\xa0','').replace('kg','').replace(',','.')
            rpm = response.css('tr.datasheet-listItem--group:contains("Caractéristiques techniques") + tr.datasheet-listItem--properties td.datasheet-listItemKey:contains("Vitesse d\'essorage") + td.datasheet-listItemValue::text').get().strip().replace('\n', '').replace('\u202f','').replace('\xa0','').replace('tours/min','')
            price = response.css("div.oopStage-conditionButton-wrapper-text-price strong::text").get().replace("\xa0",'')[:-1]
            currency = response.css("div.oopStage-conditionButton-wrapper-text-price strong::text").get().replace("\xa0",'')[-1]
            product_link = response.meta.get('product_link', '')

        except Exception as e:
            print(brand_name)
            print(model_name)
            print(f"An error occurred: {e}")
        
        #Database Operations
        database_adress = r'C:\Users\gorkemk\PycharmProjects\Market-Search\marketscrapping\French Market\washingmachines_fr.db'
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

