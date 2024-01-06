import scrapy
import sqlite3
import re


class WdidealofrSpider(scrapy.Spider):
    name = "wdidealofr"
    start_urls = ["https://www.idealo.fr/cat/3959/lave-linge-sechants.html"]

    def parse(self, response):

        products_links = response.css('div.sr-resultItemLink a::attr(href)').getall()
        for i in products_links:
            yield scrapy.Request(url = i ,callback = self.parse_product,meta={'product_link': i})



        next_url = response.css('div.sr-pagination a.sr-pageArrow::attr(href)').get()
        if next_url is not None:
            yield scrapy.Request(response.urljoin(next_url), callback=self.parse)

        

    def parse_product(self,response):
        
        try :
            brand_name_temp = response.css("h1.oopStage-title span::text").get()
            brand_name = brand_name_temp.split()[0]
            model_name = brand_name_temp.split()[-1]
            product_link = response.meta.get('product_link', '')
            capacity = response.css('tr.datasheet-listItem--properties td.datasheet-listItemKey:contains("Capacité de lavage") + td.datasheet-listItemValue::text').get().strip().replace('\n', '').replace('\xa0','').replace('kg','').replace(',','.')
            capacity_dry = response.css('tr.datasheet-listItem--properties td.datasheet-listItemKey:contains("Capacité de séchage") + td.datasheet-listItemValue::text').get().strip().replace('\n', '').replace('\xa0','').replace('kg','').replace(',','.')
            if  response.css("#datasheet > div.datasheet-wrapper > table > tbody:nth-child(3) > tr.datasheet-listItem.datasheet-listItem--properties.datasheet-listItem--collapsible > td.datasheet-listItemValue.small-6.larger-8.columns").get() == None:
                rpm = 0
            else:    
                rpm = response.css("#datasheet > div.datasheet-wrapper > table > tbody:nth-child(3) > tr.datasheet-listItem.datasheet-listItem--properties.datasheet-listItem--collapsible > td.datasheet-listItemValue.small-6.larger-8.columns::text").get().strip().replace('\n', '').replace('\u202f','').replace('\xa0','').replace('tours/min','')
            price = response.css("div.oopStage-conditionButton-wrapper-text-price strong::text").get().replace("\xa0",'')[:-1].replace('\u202f','')
            currency = response.css("div.oopStage-conditionButton-wrapper-text-price strong::text").get().replace("\xa0",'')[-1]

        except Exception as e:
            print(brand_name)
            print(model_name)
            print(f"An error occurred: {e}")
        
        #Database Operations
        database_adress = r"C:\Users\gorkemk\PycharmProjects\Market-Search\marketscrapping\French Market\\washerdryers_fr.db"
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
            INSERT OR IGNORE INTO washerdryers(TYPE, BRAND_NAME, MODEL_NAME, CAPACITY_WASH,CAPACITY_DRY , PRICE, CURRENCY,PRODUCT_LINK)
            VALUES (?, ?, ?, ?, ?, ?, ?,?, ?)
            ''', ("Washer Dryer", brand_name, model_name, capacity, capacity_dry,rpm, price,currency,product_link))

        except Exception as e:
            print(brand_name)
            print(model_name)
            cursor.execute('''
            INSERT OR IGNORE INTO washerdryers(TYPE, BRAND_NAME, MODEL_NAME, CAPACITY_WASH,CAPACITY_DRY ,RPM, PRICE, CURRENCY,PRODUCT_LINK)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', ("Washer Dryer", brand_name, model_name, capacity, capacity_dry,rpm ,price,currency,product_link))
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

