import scrapy
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import sqlite3

class WmpricespyukSpider(scrapy.Spider):
    name = "wmpricespyUK"
    start_urls = ["https://pricespy.co.uk/c/washing-machines?1247=2342"]

    def parse(self, response):

        product_links = response.css("div  section  div.Content-sc-2fu3f8-2.bugHkt  div  div  div article  a::attr(href)").getall()
        for i in product_links:
            yield scrapy.Request(url=("https://pricespy.co.uk" + i), callback=self.parse_product,meta={'product_link': i})

        next_url = response.css("#root > div > section > div.Content-sc-2fu3f8-2.bugHkt > div > div > div > div > section > main > div > span > ul > li:last-child > a::attr(href)").get()
        if next_url is not None:
            yield scrapy.Request(url = f"https://pricespy.co.uk{next_url}",callback=self.parse)

    def parse_product(self, response):
        brand_name = response.css('div  section  section  div div section span  a::text').get()
        price = response.xpath('//span[@class="Text--1acwy6y lmewLo titlesmalltext"]/text()').re_first(r'£(\d+(?:\.\d{2})?)')
        currency = response.css('span.Text--1acwy6y.lmewLo.titlesmalltext::text').re_first(r'£')
        product_link = f"https://pricespy.co.uk{response.meta.get('product_link', '')}"

        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument("--ignore-certificate-error")
        chrome_options.add_argument("--ignore-ssl-errors")
        driver = webdriver.Chrome(options=chrome_options)
        url = f"https://pricespy.co.uk{response.meta.get('product_link', '')}#properties"
        driver.get(url)
        cookie_popup_button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'#root-modal > div > div > div > div > div > div.StyledFooterContent--1idxbh6.cxOYpt > div > button.BaseButton--onihrq.djcpuv.primarybutton > span')))
        cookie_popup_button.click()
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        try:

            WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR,'#\#properties > div > section > section > div > div > div.hideInViewports-sc-0-0.iwivxM > section:nth-child(2) > div:nth-child(9) > div:nth-child(2) > span')))
            model_name = driver.find_element(By.CSS_SELECTOR, '#\#properties div section section div div div.hideInViewports-sc-0-0.iwivxM div section div:nth-child(2) div:nth-child(2) span').text.split()[1]
            capacity = driver.find_element(By.CSS_SELECTOR,'#\#properties > div > section > section > div > div > div.hideInViewports-sc-0-0.iwivxM > section:nth-child(2) > div:nth-child(2) > div:nth-child(2) > span').text.split()[0]
            print("xxxxxxxxxxxxxxxxxxxxxxx")
            rpm = driver.find_element(By.CSS_SELECTOR,'#\#properties > div > section > section > div > div > div.hideInViewports-sc-0-0.iwivxM > section:nth-child(2) > div:nth-child(9) > div:nth-child(2) > span').text.split()[0]
            print(brand_name)
            print(model_name)
            print(capacity)
            print(rpm)
            print(price)

        finally:
            driver.quit()

        database_adress = r'England Market\washingmachines_en.db'
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


