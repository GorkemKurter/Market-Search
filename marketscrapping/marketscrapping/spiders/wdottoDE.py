import scrapy
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import sqlite3

class WdottodeSpider(scrapy.Spider):
    name = "wdottoDE"
    start_urls = ["https://www.otto.de/haushalt/waschtrockner/"]

    def parse(self, response):
        product_links = response.css("#reptile-tilelist > article > ul > li > a::attr(href)").getall()
        for i in range(len(product_links)):
            try:
                if i < 11:
                    brand_name = response.css(f'#reptile-tilelist > article:nth-child({i}) > ul > li > div > div.find_tile__content > header > a::attr(title)').get().split()[0]
                    model_name = " ".join(response.css(f'#reptile-tilelist > article:nth-child({i}) > ul > li > div > div.find_tile__content > header > a::attr(title)').get().split(",")[0].split()[2::])
                    capacity = response.css(f'#reptile-tilelist > article:nth-child({i}) > ul > li > div > div.find_tile__content > header > a::attr(title)').get().split(",")[1].split()[0]
                    capacity_dry = response.css(f'#reptile-tilelist > article:nth-child({i}) > ul > li > div > div.find_tile__content > header > a::attr(title)').get().split(",")[2].split()[0]
                    rpm = response.css(f'#reptile-tilelist > article:nth-child({i}) > ul > li > div > div.find_tile__content > header > a::attr(title)').get().split(",")[3].split()[0]
                    product_link = f"https://www.otto.de{product_links[i]}"
                    currency = "€"
                    chrome_options = Options()
                    chrome_options.add_argument('--headless')
                    chrome_options.add_argument("--ignore-certificate-error")
                    chrome_options.add_argument("--ignore-ssl-errors")
                    driver = webdriver.Chrome(options=chrome_options)
                    driver.get(product_link)
                    try:
                        cookie_popup_button = WebDriverWait(driver, 5).until(
                            EC.element_to_be_clickable((By.CSS_SELECTOR, '#onetrust-accept-btn-handler')))
                        cookie_popup_button.click()
                    except:
                        pass
                    try:
                        price = WebDriverWait(driver, 20).until(EC.presence_of_element_located(
                            (By.CSS_SELECTOR, 'span.js_pdp_price__retail-price__value.pl_headline300'))).text.split()[
                            0].replace(",", ".")
                    finally:
                        driver.quit()
                else:
                    brand_name = response.css(f'#reptile-tilelist > article:nth-child({i}) > ul > li > a::text').get().split()[0]
                    model_name = " ".join(response.css(f'#reptile-tilelist > article:nth-child({i}) > ul > li > a::text').get().split(",")[0].split()[2::])
                    capacity = response.css(f'#reptile-tilelist > article:nth-child({i}) > ul > li > a::text').get().split(",")[1].split()[0]
                    capacity_dry = response.css(f'#reptile-tilelist > article:nth-child({i}) > ul > li > a::text').get().split(",")[2].split()[0]
                    rpm = response.css(f'#reptile-tilelist > article:nth-child({i}) > ul > li > a::text').get().split(",")[3].split()[0]
                    product_link = f"https://www.otto.de{product_links[i]}"
                    currency = "€"
                    chrome_options = Options()
                    chrome_options.add_argument('--headless')
                    chrome_options.add_argument("--ignore-certificate-error")
                    chrome_options.add_argument("--ignore-ssl-errors")
                    driver = webdriver.Chrome(options=chrome_options)
                    driver.get(product_link)
                    try:
                        cookie_popup_button = WebDriverWait(driver, 5).until(
                            EC.element_to_be_clickable((By.CSS_SELECTOR, '#onetrust-accept-btn-handler')))
                        cookie_popup_button.click()
                    except:
                        pass
                    try:
                        price = WebDriverWait(driver, 20).until(EC.presence_of_element_located(
                            (By.CSS_SELECTOR, 'span.js_pdp_price__retail-price__value.pl_headline300'))).text.split()[
                            0].replace(",", ".")
                    finally:
                        driver.quit()
                    #database operations

                print("******************")
                print(brand_name)
                print(model_name)
                print(capacity)
                print(capacity_dry)
                print(rpm)
                print(price)
                print(currency)
                print(product_link)
                print("******************")



            except Exception as e:
                print(e)