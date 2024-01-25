import time

import scrapy
import sqlite3
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
class WmceneoplSpider(scrapy.Spider):
    name = "wmceneoPL"
    start_urls = ["https://www.ceneo.pl/Pralki/Ladowanie:Od_frontu.htm"]
    custom_settings = {
        'DOWNLOAD_DELAY': 3,
        'USER_AGENT': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    counter = 0
    def parse(self, response):

        brand_names = response.css("#body > div > div > div.grid-cat__main > div > section > div.category-list-body.js_category-list-body.js_search-results.js_products-list-main.js_async-container > div > div > div.cat-prod-row__content > div.cat-prod-row__desc > div:nth-child(1) > div:nth-child(1) > strong > a > span::text").getall()
        print(brand_names)
        for i in range(len(brand_names)):
            try:

                brand_name = response.css(f"#body > div > div > div.grid-cat__main > div > section > div.category-list-body.js_category-list-body.js_search-results.js_products-list-main.js_async-container > div:nth-child({i}) > div > div.cat-prod-row__content > div.cat-prod-row__desc > div:nth-child(1) > div:nth-child(1) > strong > a > span::text").get().split()[1]
                model_name = " ".join(response.css(f"#body > div > div > div.grid-cat__main > div > section > div.category-list-body.js_category-list-body.js_search-results.js_products-list-main.js_async-container > div:nth-child({i}) > div > div.cat-prod-row__content > div.cat-prod-row__desc > div:nth-child(1) > div:nth-child(1) > strong > a > span::text").get().split()[-1:1:-1])
                capacity = response.css(f"#body > div > div > div.grid-cat__main > div > section > div.category-list-body.js_category-list-body.js_search-results.js_products-list-main.js_async-container > div:nth-child({i}) > div > div.cat-prod-row__content > div.cat-prod-row__desc > div.cat-prod-row__desc-row.cat-prod-row__desc-row--main > div > ul > li:contains('Ładowność') > strong::text").get().split()[0]
                rpm = response.css(f"#body > div > div > div.grid-cat__main > div > section > div.category-list-body.js_category-list-body.js_search-results.js_products-list-main.js_async-container > div:nth-child({i}) > div > div.cat-prod-row__content > div.cat-prod-row__desc > div.cat-prod-row__desc-row.cat-prod-row__desc-row--main > div > ul > li:contains('Prędkość:') > strong::text").get().split()[0]
                price = response.css(f"#body > div > div > div.grid-cat__main > div > section > div.category-list-body.js_category-list-body.js_search-results.js_products-list-main.js_async-container > div:nth-child({i}) > div > div.cat-prod-row__content > div.cat-prod-row__price > a:nth-child(1) > span.price-format.nowrap > span > span.value::text").get().replace(" ","")
                price_decimal = response.css(f"#body > div > div > div.grid-cat__main > div > section > div.category-list-body.js_category-list-body.js_search-results.js_products-list-main.js_async-container > div:nth-child({i}) > div > div.cat-prod-row__content > div.cat-prod-row__price > a:nth-child(1) > span.price-format.nowrap > span > span.penny::text").get().replace(",",".")
                price = "".join([price,price_decimal])
                currency = "zł"
                product_link = response.css(f"#body > div > div > div.grid-cat__main > div > section > div.category-list-body.js_category-list-body.js_search-results.js_products-list-main.js_async-container > div:nth-child({i}) > div > div.cat-prod-row__content > div.cat-prod-row__desc > div:nth-child(1) > div:nth-child(1) > strong > a::attr(href)").get()
                product_link = f"https://www.ceneo.pl/{product_link}"
                print(brand_name)
                print(model_name)
                print(capacity)
                print(rpm)
                print(price)
                print(currency)
                print(product_link)
                self.counter = self.counter + 1
                print(self.counter)

            except Exception as e:
                print(e)
                continue

            try:
                database_adress = r'Poland Market\washingmachines_PL.db'
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

            except Exception as e:
                print(e)

        current_url = response.url
        print("**************************")
        chrome_options = Options()
        #chrome_options.add_argument('--headless')
        chrome_options.add_argument("--ignore-certificate-error")
        chrome_options.add_argument("--ignore-ssl-errors")
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(current_url)
        try:
            cookie_popup_button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'#js_cookie-consent-general > div > div.cookie-consent__buttons > button.cookie-consent__buttons__action.js_cookie-consent-agree.primary')))
            cookie_popup_button.click()
        except Exception as e:
            print(e)
        next_page_clicker = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'a.pagination__item.pagination__next')))
        next_page_clicker.click()
        time.sleep(20)
        next_url = driver.current_url
        driver.close()
        if next_url is not None:
            yield scrapy.Request(next_url,callback=self.parse)
    def remove_duplicates(self, adress):
        conn = sqlite3.connect(adress)
        cursor = conn.cursor()

        try:
            cursor.execute('''
                    DELETE FROM washingmachines
                    WHERE user_id NOT IN (
                        SELECT MIN(user_id)
                        FROM washingmachines
                        GROUP BY BRAND_NAME, MODEL_NAME , PRICE
                    )
                ''')
        except Exception as e:
            print(f"An error occurred while removing duplicates: {e}")

        conn.commit()
        conn.close()
        #product_link = response.css("#body > div > div > div.grid-cat__main > div > section > div.category-list-body.js_category-list-body.js_search-results.js_products-list-main.js_async-container > div > div > div.cat-prod-row__content > div.cat-prod-row__desc > div:nth-child(1) > div:nth-child(1) > strong > a::attr(href)").getall()
        #for i in product_link:
        #    yield scrapy.Request(f"https://www.ceneo.pl{i}",callback=self.parse_product,meta={'product_link' : i})

        #next_url = response.css("#body > div > div > div.grid-cat__main > div > section > footer > div > a.pagination__item.pagination__next::attr(href)").get()
        #if next_url is not None:
        #    yield scrapy.Request(f"https://www.ceneo.pl{next_url}",callback=self.parse)

    #def parse_product(self,response):

    #    if response.css("div.product-top__title > h1::text").get().split()[0] == "Pralka":
    #        brand_name = response.css("div.product-top__title > h1::text").get().split()[1]
    '''    else:
            brand_name = response.css("div.product-top__title > h1::text").get().split()[0]
        model_name = response.css("div.product-top__title > h1::text").get().split()[-1]
        capacity = response.css("#productTechSpecs > div:nth-child(1) > table > tbody > tr:contains('Ładowność') > td > ul > li::text").get().split()[0]
        rpm = response.css("#productTechSpecs > div:nth-child(1) > table > tbody > tr:contains('Prędkość ') > td > ul > li > a::text").get().split()[0]
        try:
            price = response.css("span.value::text").get().replace(" ","")
        except:
            price = response.css("#body > div.no-banner > div > div > article > div > div.product-top__price-column.js_column_product_offer.pointer > div > div > div.product-offer-summary__price-box.product-offer-summary__price-box--with-icon > span > span > span.value::text").get().replace(" ","")
        try:
            price_penny = response.css("span.penny::text").get().replace(",",".")
            delimeter = ""
            price = delimeter.join([price, price_penny])
        except:
            pass
        price = float(price) * 0.23
        price = str(price)
        currency = "€"
        product_link = f"https://www.ceneo.pl{response.meta.get('product_link','')}"

        print("**************************")
        print(brand_name)
        print(model_name)
        print(capacity)
        print(rpm)
        print(price)
        print(currency)
        print(product_link)
        print("**************************")'''