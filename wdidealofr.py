import scrapy
import sqlite3
import re


class WdidealofrSpider(scrapy.Spider):
    name = "wdidealofr"
    start_urls = ["https://www.idealo.fr/cat/3959/lave-linge-sechants.html"]

    def parse(self, response):

        products_links = response.css('div.sr-resultItemLink a::attr(href)').getall()
        for i in products_links:
            yield scrapy.Request(url = i ,callback = self.parse_product)



        next_url = response.css('div.sr-pagination a.sr-pageArrow::attr(href)').get()
        if next_url is not None:
            yield scrapy.Request(response.urljoin(next_url), callback=self.parse)

        

    def parse_product(self,response):
        
        try :
            brand_name_temp = response.css("h1.oopStage-title span::text").get()
            brand_name = brand_name_temp.split()[0]
            model_name = brand_name_temp.split()[-1]
            capacity = response.css('tr.datasheet-listItem--properties td.datasheet-listItemKey:contains("Capacité de lavage") + td.datasheet-listItemValue::text').get().strip().replace('\n', '').replace('\xa0','').replace('kg','').replace(',','.')
            capacity_dry = response.css('tr.datasheet-listItem--properties td.datasheet-listItemKey:contains("Capacité de séchage") + td.datasheet-listItemValue::text').get().strip().replace('\n', '').replace('\xa0','').replace('kg','').replace(',','.')
            if response.css('tr.datasheet-listItem--group + tr.datasheet-listItem--properties td.datasheet-listItemKey:contains("Vitesse d\'essorage") + td.datasheet-listItemValue::text').get() == None:
                rpm = '-'
            else:    
                rpm = response.css('tr.datasheet-listItem--group + tr.datasheet-listItem--properties td.datasheet-listItemKey:contains("Vitesse d\'essorage") + td.datasheet-listItemValue::text').get().strip().replace('\n', '').replace('\u202f','').replace('\xa0','').replace('tours/min','')
            price = response.css("div.oopStage-conditionButton-wrapper-text-price strong::text").get().replace("\xa0",'')[:-1].replace('\u202f','')
            currency = response.css("div.oopStage-conditionButton-wrapper-text-price strong::text").get().replace("\xa0",'')[-1] 

            

        except Exception as e:
            print(brand_name)
            print(model_name)
            print(f"An error occurred: {e}")
        
        #Database Operations    
        conn = sqlite3.connect('C:\\Users\\gorke\\OneDrive\\Masaüstü\\gorkem\\marketproject\\Market-Search\\marketscrapping\\French Market\\washerdryers_idealo_fr.db')
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
            INSERT OR IGNORE INTO washerdryers(TYPE, BRAND_NAME, MODEL_NAME, CAPACITY_WASH,CAPACITY_DRY , PRICE, CURRENCY)
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
