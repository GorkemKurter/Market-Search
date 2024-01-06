###################################################################################################

#TAMAMLANDI
#NOT:RPM Filtre, Yıkayıcı kurutucu kapasite filtre veritabanı işlemlerinden ayarlanacak

###################################################################################################

import scrapy
import sqlite3
import re


def extract_kilograms(product):
    match = re.search(r'(\d+)\s*kg', product,re.IGNORECASE)
    if match:
        return match.group(1)
    return None

def rpm_purification(input):
    pattern = r'(\d+)'
    match = re.search(pattern,input)
    if match:
        return match.group(1)



class WdbutfrSpider(scrapy.Spider):
    name = "wdbutfr"
    allowed_domains = ["www.but.fr"]
    start_urls = ["https://www.but.fr/electromenager/lavage/lave-linge-hublot/index-c11197/NW-3479-type-de-lave_linge~lave-linge-hublot-sechant?PageSize=60"]

    def parse(self, response):
        brand_name = response.css(".infos-title strong::text").getall()
        model_name = response.css(".infos-title span::text").getall()

        #Capacity operations
        capacity = []
        capacity_temp = response.css(".infos ul li:nth-child(1)::text").getall()
        capacity_values = [capacity_temp[i] for i in range(2,len(capacity_temp),3)]
        capacity_header = [capacity_temp[i] for i in range (0,len(capacity_temp),3)]
        for i in range(len(brand_name)):
            if capacity_header[i] == "Capacité de chargement (en kg)":
                capacity.append(capacity_values[i])
            else:
                capacity.append(extract_kilograms(model_name[i]))

        #Dryer Capacity operations
        dryer_capacity = []
        dryer_capacity_temp = response.css(".infos ul li:nth-child(2)::text").getall()
        dryer_capacity_values = [dryer_capacity_temp[i] for i in range(2,len(dryer_capacity_temp),3)]
        dryer_capacity_header = [dryer_capacity_temp[i] for i in range (0,len(dryer_capacity_temp),3)]
        for i in range(len(brand_name)):
            if dryer_capacity_header[i] == "Capacité de séchage (en kg)":
                dryer_capacity.append(dryer_capacity_values[i])
            else:
                dryer_capacity.append(rpm_purification(capacity_values[i]))       
        
        #RPM operations
        rpm = []
        rpm_temp = response.css(".infos ul li:nth-child(3)::text").getall()
        rpm_values =  [rpm_temp[i] for i in range(2,len(rpm_temp),3)]
        rpm_header =  [rpm_temp[i] for i in range(0,len(rpm_temp),3)]
        for i in range(len(brand_name)):
            if rpm_header[i] == "Classe d'efficacité énergétique":
                rpm.append(rpm_purification(dryer_capacity_values[i]))
            else:
                rpm.append(rpm_purification(rpm_values[i]))

        print(rpm)        

        #Price Operations
        price = response.css("div.pricesActions p.pricesActions__prices span.pricesActions__prices-price::text").getall()

        product_links_temp = response.css("div.product a::attr(href)").getall()
        product_links = []
        for i in range(len(product_links_temp)):
            product_links.append('https://www.but.fr' + product_links_temp[i])


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
            CAPACITY_DRY TEXT,
            RPM TEXT,
            PRICE TEXT,
            CURRENCY TEXT ,
            PRODUCT_LINK
            )
            ''')
            
        #TRY-EXCEPT
        try:
            for i in range(len(brand_name)):
                if (float(capacity[i]) == 6 and float(rpm[i]) == 1000) or (float(capacity[i])==6 and float(rpm[i]) == 1200) or (float(capacity[i]) == 6 and float(rpm[i]) == 1400) or (float(capacity[i]) == 7 and float(rpm[i]) == 1000) or (float(capacity[i]) == 7 and float(rpm[i]) == 1200) or (float(capacity[i]) == 7 and float(rpm[i]) == 1400) or (float(capacity[i]) == 8 and float(rpm[i]) == 1000) or (float(capacity[i]) == 8 and float(rpm[i]) == 1200) or (float(capacity[i]) == 8 and float(rpm[i]) == 1400) or (float(capacity[i]) == 8 and float(rpm[i]) == 1600) or (float(capacity[i]) == 9 and float(rpm[i]) == 1000) or (float(capacity[i]) == 9 and float(rpm[i]) == 1200) or (float(capacity[i]) == 9 and float(rpm[i]) == 1400) or (float(capacity[i]) == 10 and float(rpm[i]) == 1200) or (float(capacity[i]) == 10 and float(rpm[i]) == 1400) or (float(capacity[i])==11 and float(rpm[i]) == 1400) or (float(capacity[i])==12 and float(rpm[i]) == 1400) :
                    cursor.execute('''
                    INSERT OR IGNORE INTO washerdryers(TYPE, BRAND_NAME, MODEL_NAME, CAPACITY_WASH,CAPACITY_DRY,RPM, PRICE,CURRENCY,PRODUCT_LINK)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', ("Washer_Dryer", brand_name[i], model_name[i], capacity[i],dryer_capacity[i],rpm[i], price[i],response.css('span.pricesActions__prices-price sup::text').getall()[i],product_links[i]))

            next_url = response.css(".category-pager--next  a::attr(href)").get()
            if next_url is not None:
                yield scrapy.Request(response.urljoin(next_url), callback=self.parse)
        except:
            pass

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
                    FROM washingmachines
                    GROUP BY BRAND_NAME, MODEL_NAME , PRODUCT_LINK
                )
            ''')
        except Exception as e:
            print(f"An error occurred while removing duplicates: {e}")

        conn.commit()
        conn.close()

