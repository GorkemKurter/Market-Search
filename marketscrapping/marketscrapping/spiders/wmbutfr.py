###################################################################################################

#Try-except yazılacak

###################################################################################################
import scrapy
import sqlite3
import re

def extract_kilograms(product):
    match = re.search(r'(\d+(\.\d+)?)\s*kg', product, re.IGNORECASE)
    if match:
        return match.group(1)
    return None

def rpm_purification(input):
    pattern = r'(\d+)'
    match = re.search(pattern,input)
    if match:
        return match.group(1)
    
k = 0

class WmbutfrSpider(scrapy.Spider):

    name = "wmbutfr"
    start_urls = ["https://www.but.fr/electromenager/lavage/lave-linge-hublot/index-c11197/NW-3479-type-de-lave_linge~lave-linge-hublot/NW-3479-type-de-lave_linge~lave-linge-encastrable?PageSize=60"]
    
    def parse(self, response):
        
        brand_name = response.css(".infos-title strong::text").getall()
        model_name = response.css(".infos-title span::text").getall()


        #Capacity operations
        #capacity_temp = response.css('ul.infos-features li:contains("Capacité de chargement (en kg)")::text').getall()
        capacity = []
        capacity_temp = response.css(".infos ul li:nth-child(1)::text").getall()
        capacity_values = [capacity_temp[i] for i in range(2,len(capacity_temp),3)]
        capacity_header = [capacity_temp[i] for i in range (0,len(capacity_temp),3)]

        for i in range(len(brand_name)):
            if capacity_header[i] == "Capacité de chargement (en kg)":
                capacity.append(capacity_values[i])
            else:
                capacity.append(extract_kilograms(model_name[i]))

        #RPM operations
        rpm = []
        rpm_temp = response.css(".infos ul li:nth-child(2)::text").getall()
        rpm_values =  [rpm_temp[i] for i in range(2,len(rpm_temp),3)]
        rpm_header =  [rpm_temp[i] for i in range(0,len(rpm_temp),3)]
        for i in range(len(brand_name)):
            if rpm_header[i] == "Classe d'efficacité énergétique":
                rpm.append(rpm_purification(capacity_values[i]))
            else:
                rpm.append(rpm_purification(rpm_values[i]))

        product_links_temp = response.css("div.product a::attr(href)").getall()
        product_links = []
        for i in range(len(product_links_temp)):
            product_links.append('https://www.but.fr' + product_links_temp[i])

        #Price Operations
        price = response.css("div.pricesActions p.pricesActions__prices span.pricesActions__prices-price::text").getall()

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


        #TRY-EXCEPT
        for i in range(len(brand_name)):
            try:
                if model_name[i].lower().find("séchant") != -1:
                    continue
                    
                current_combination = (float(capacity[i]), float(rpm[i]))
                if current_combination in valid_combinations:
                    cursor.execute('''
            INSERT OR IGNORE INTO washingmachines(TYPE, BRAND_NAME, MODEL_NAME, CAPACITY_kg, RPM, PRICE, CURRENCY, PRODUCT_LINK)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', ("Washing Machine", brand_name[i], model_name[i], capacity[i], rpm[i], price[i], response.css("span.pricesActions__prices-price sup::text").getall()[i],product_links[i]))

            except Exception as e:
                pass


        next_url = response.css("ul.pagination li.page-item:nth-last-child(2) a::attr(href)").get()
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
