###################################################################################################

#TAMAMLANDI
#NOT:RPM Filtre, Yıkayıcı kurutucu kapasite filtre veritabanı işlemlerinden ayarlanacak

###################################################################################################
import scrapy
import sqlite3
import re

def get_dry_capacity(liste):
    dry_kilograms = []
    for item in liste:
        match = re.search(r'/ (\d+)', item)
        if match:
            dry_kilograms.append(match.group(1))
    return dry_kilograms       

class WdelectrodepotfrSpider(scrapy.Spider):
    name = "wdelectrodepotfr"
    allowed_domains = ["www.electrodepot.fr"]
    start_urls = ["https://www.electrodepot.fr/gros-electromenager/lave-linge/lave-linge-sechant.html"]

    def parse(self, response):
        model_name = []
        brand_name = [brand.split(':')[0].strip() if ':' in brand else brand.strip() for brand in response.css(".productlist-item_infos div.productlist-item--brand::text").getall()]
        for brand, model in zip(brand_name, [item.strip() for item in response.css(".productlist-item_infos h2.productlist-item--name::text").getall()if item.strip()]):
            if brand in model:
                model_index = model.find(brand) + len(brand)
                clean_model = model[model_index:].strip()
                model_name.append(clean_model)
        rpm =[element.split(":")[-1].strip().split()[0] for element in response.css(".productlist-item--description ul li:nth-child(3)::text").getall()]
        price = response.css('.productlist-item--price .number_price::text').getall()
        capacity =[element.split(":")[-1].strip() for element in response.css(".productlist-item--description ul li:nth-child(2)::text").getall()] 
        capacity_dry_temp = response.css("div.productlist-item_infos h2.productlist-item--name::text").getall()
        capacity_dry = get_dry_capacity(capacity_dry_temp)

        conn = sqlite3.connect('C:\\Users\\gorkemk\\Desktop\\Genel\\Market_Search\\marketscrapping\\French Market\\washerdryers_electrodepot_fr.db')
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
            CURRENCY TEXT 
            )
            ''')

        #TRY-EXCEPT
        for i in range(len(brand_name)):
            if (int(capacity[i].split()[0]) == 6 and int(rpm[i]) == 1000) or (int(capacity[i].split()[0])==6 and int(rpm[i]) == 1200) or (int(capacity[i].split()[0]) == 6 and int(rpm[i]) == 1400) or (int(capacity[i].split()[0]) == 7 and int(rpm[i]) == 1000) or (int(capacity[i].split()[0]) == 7 and int(rpm[i]) == 1200) or (int(capacity[i].split()[0]) == 7 and int(rpm[i]) == 1400) or (int(capacity[i].split()[0]) == 8 and int(rpm[i]) == 1000) or (int(capacity[i].split()[0]) == 8 and int(rpm[i]) == 1200) or (int(capacity[i].split()[0]) == 8 and int(rpm[i]) == 1400) or (int(capacity[i].split()[0]) == 8 and int(rpm[i]) == 1600) or (int(capacity[i].split()[0]) == 9 and int(rpm[i]) == 1000) or (int(capacity[i].split()[0]) == 9 and int(rpm[i]) == 1200) or (int(capacity[i].split()[0]) == 9 and int(rpm[i]) == 1400) or (int(capacity[i].split()[0]) == 10 and int(rpm[i]) == 1200) or (int(capacity[i].split()[0]) == 10 and int(rpm[i]) == 1400) :
                cursor.execute('''
                INSERT OR IGNORE INTO washerdryers(TYPE, BRAND_NAME, MODEL_NAME, CAPACITY_WASH,CAPACITY_DRY,RPM, PRICE,CURRENCY)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', ("Washer_Dryer", brand_name[i], model_name[i], capacity[i],capacity_dry[i],rpm[i], price[i],response.css('.number_price sup::text').getall()[i]))
        
        next_url = response.css(".category-pager--next  a::attr(href)").get()
        
        if next_url is not None:
            yield scrapy.Request(response.urljoin(next_url), callback=self.parse)

        conn.commit()
        conn.close()        
