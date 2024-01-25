import scrapy
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import sqlite3

class WmottodeSpider(scrapy.Spider):
    name = "wmottoDE"
    allowed_domains = ["www.otto.de"]
    start_urls = ["https://www.otto.de/haushalt/waschmaschinen/frontlader/"]

    def parse(self, response):
        product_links = response.css("#reptile-tilelist > article > ul > li > a::attr(href)").getall()
        for i in product_links:
            yield scrapy.Request(f"https://www.otto.de{i}",callback=self.parse_product,meta={'product_link':f"https://www.otto.de{i}"})
        next_page_selector = response.css("js_pagingLink ts-link p_btn50--1st reptile_paging__btn").get()
        if next_page_selector is not None:
            next_page_link = self.selenium_clicker(start_url_selector=response.url)
            print(next_page_link)
            print("xxxxxxxxxxxxxxxxxxxxxxx")
            yield scrapy.Request(next_page_link,callback=self.parse)

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

    def selenium_clicker(self,response,start_url_selector):
        chrome_options = Options()
        #chrome_options.add_argument('--headless')
        chrome_options.add_argument("--ignore-certificate-error")
        chrome_options.add_argument("--ignore-ssl-errors")
        driver = webdriver.Chrome(options=chrome_options)

        driver.get(start_url_selector)
        next_page_clicker = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'button.js_pagingLink.ts-link p_btn50--1st.reptile_paging__btn')))
        next_page_clicker.click()
        driver.quit()
        return response.url









