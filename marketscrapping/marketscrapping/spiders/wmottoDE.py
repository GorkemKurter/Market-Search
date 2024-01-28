import scrapy
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import sqlite3
import json

class WmottodeSpider(scrapy.Spider):
    name = "wmottoDE"
    allowed_domains = ["www.otto.de"]
    start_urls = ["https://www.otto.de/haushalt/waschmaschinen/frontlader/"]

    def parse(self, response):
        product_links = response.css("#reptile-tilelist > article > ul > li > a::attr(href)").getall()

        for i in product_links:
            yield scrapy.Request(f"https://www.otto.de{i}",callback=self.parse_product,meta={'product_link':f"https://www.otto.de{i}"})
        try :
            data_page = response.css("li[id='reptile-paging-bottom-next'] button::attr(data-page)").get()
            data_page_json = json.loads(data_page)
            next_page_url = data_page_json.get('o', '')
            print(next_page_url)
            print("xxxxxxxxxxxxxxxxxxxxxxx")
        except:
            pass

        if next_page_url is not None :
            yield scrapy.Request(f'https://www.otto.de/haushalt/waschmaschinen/frontlader/?l=gq&o={next_page_url}&c=Waschmaschinen',callback=self.parse)

    def parse_product(self,response):

        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument("--ignore-certificate-error")
        chrome_options.add_argument("--ignore-ssl-errors")
        driver = webdriver.Chrome(options=chrome_options)

        url = response.meta.get('product_link', '')
        driver.get(url)
        try :
            cookie_popup_button = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'#onetrust-accept-btn-handler')))
            cookie_popup_button.click()
        except :
            pass

        try:

            brand_name = driver.find_element(By.CSS_SELECTOR,'div.pl_grid-col-12 h1').text.split()[0]
            show_details_button = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR,'div.js_pdp_details.pl_block.pdp_details div.pl_text-expander.pl_copy100.pdp_details__text-expander.js_pdp_details__text-expander.pl_text-expander--has-more a')))
            show_details_button.click()
            WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR,'div.pdp_details__characteristics-html table:nth-child(3) tbody tr:nth-child(1) td:nth-child(2)')))
            model_name = driver.find_element(By.CSS_SELECTOR, 'div.pdp_details__characteristics-html table:nth-child(3) tbody tr:nth-child(1) td:nth-child(2)').text
            capacity = driver.find_element(By.CSS_SELECTOR,'div.pdp_details__characteristics-html table:nth-child(3) tr:nth-child(5) td:nth-child(2)').text.split()[0]
            rpm = driver.find_element(By.CSS_SELECTOR,'div.pdp_details__characteristics-html table:nth-child(3) tr:nth-child(4) td:nth-child(2)').text.split()[0]
            WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR,'span.js_pdp_price__retail-price__value.pl_headline300')))
            price = driver.find_element(By.CSS_SELECTOR,'span.js_pdp_price__retail-price__value.pl_headline300').text.split()[0].replace(",",".")
            product_link = response.meta.get('product_link','')
            currency = "€"
        finally:
            print("xxxxxxxxxxxxxxxxxxxxxxx")
            print(brand_name)
            print(model_name)
            print(capacity)
            print(rpm)
            print(price)
            print("xxxxxxxxxxxxxxxxxxxxxxx")
            driver.quit()
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








