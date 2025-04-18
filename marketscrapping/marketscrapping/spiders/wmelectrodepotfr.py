###################################################################################################

#TAMAMLANDI

###################################################################################################

import scrapy
import sqlite3

class ElectrodepotfrSpider(scrapy.Spider):
    name = "electrodepotfr"
    start_urls = ["https://www.electrodepot.fr/gros-electromenager/lave-linge/lave-linge-hublot.html"]

    def parse(self, response):
        model_name = []
        brand_name = [brand.split(':')[0].strip() if ':' in brand else brand.strip() for brand in response.css(".productlist-item_infos div.productlist-item--brand::text").getall()]
        for brand, model in zip(brand_name, [item.strip() for item in response.css(".productlist-item_infos h2.productlist-item--name::text").getall() if item.strip()]):
            if brand in model:
                model_index = model.find(brand) + len(brand)
                clean_model = model[model_index:].strip()
                model_name.append(clean_model)
        rpm =[element.split(":")[-1].strip().split()[0] for element in response.css(".productlist-item--description ul li:nth-child(3)::text").getall()]
        price = response.css('.productlist-item--price .number_price::text').getall()
        capacity =[element.split(":")[-1].strip() for element in response.css(".productlist-item--description ul li:nth-child(2)::text").getall()]

        product_links = response.css("div.productlist-product a::attr(href)").getall()
        product_links.pop(0)
        print(product_links)

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

        #TRY-EXCEPT
        data = []
        for i in range(len(brand_name)):
            if (int(capacity[i].split()[0]) == 6 and int(rpm[i]) == 1000) or (int(capacity[i].split()[0])==6 and int(rpm[i]) == 1200) or (int(capacity[i].split()[0]) == 6 and int(rpm[i]) == 1400) or (int(capacity[i].split()[0]) == 7 and int(rpm[i]) == 1000) or (int(capacity[i].split()[0]) == 7 and int(rpm[i]) == 1200) or (int(capacity[i].split()[0]) == 7 and int(rpm[i]) == 1400) or (int(capacity[i].split()[0]) == 8 and int(rpm[i]) == 1000) or (int(capacity[i].split()[0]) == 8 and int(rpm[i]) == 1200) or (int(capacity[i].split()[0]) == 8 and int(rpm[i]) == 1400) or (int(capacity[i].split()[0]) == 8 and int(rpm[i]) == 1600) or (int(capacity[i].split()[0]) == 9 and int(rpm[i]) == 1000) or (int(capacity[i].split()[0]) == 9 and int(rpm[i]) == 1200) or (int(capacity[i].split()[0]) == 9 and int(rpm[i]) == 1400) or (int(capacity[i].split()[0]) == 10 and int(rpm[i]) == 1200) or (int(capacity[i].split()[0]) == 10 and int(rpm[i]) == 1400) :
                data.append({
                    "TYPE"  : "Washing Machine",
                    "BRAND NAME": brand_name[i],
                    "MODEL NAME": model_name[i],
                    "CAPACITY"  : capacity[i],
                    "RPM": rpm[i],
                    "PRICE": price[i] + response.css('.number_price sup::text').getall()[i]
                })
                cursor.execute('''
                INSERT OR IGNORE INTO washingmachines(TYPE, BRAND_NAME, MODEL_NAME, CAPACITY_kg, RPM, PRICE,CURRENCY,PRODUCT_LINK)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', ("Washing Machine", brand_name[i], model_name[i], capacity[i], rpm[i], price[i],response.css('.number_price sup::text').getall()[i],product_links[i]))
        
        next_url = response.css(".category-pager--next  a::attr(href)").get()
        
        if next_url is not None:
            yield scrapy.Request(response.urljoin(next_url), callback=self.parse)

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

