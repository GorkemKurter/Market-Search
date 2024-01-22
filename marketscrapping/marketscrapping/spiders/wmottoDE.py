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
        print(product_links)
        for i in product_links:
            yield scrapy.Request(f"https://www.otto.de{i}",callback=self.parse_product,meta={'product_link':f"https://www.otto.de{i}"})

    def parse_product(self,response):

        chrome_options = Options()
        #chrome_options.add_argument('--headless')
        chrome_options.add_argument("--ignore-certificate-error")
        chrome_options.add_argument("--ignore-ssl-errors")
        driver = webdriver.Chrome(options=chrome_options)

        url = response.meta.get('product_link', '')
        driver.get(url)
        cookie_popup_button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'#onetrust-accept-btn-handler')))
        cookie_popup_button.click()

        try:

            brand_name = driver.find_element(By.CSS_SELECTOR,'div.pl_grid-col-12 h1').text.split()[0]
            print(brand_name)
            print("xxxxxxxxxxxxxxxxxxxxxxx")
            show_details_button = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR,'div.js_pdp_details.pl_block.pdp_details div.pl_text-expander.pl_copy100.pdp_details__text-expander.js_pdp_details__text-expander.pl_text-expander--has-more a')))
            show_details_button.click()
            model_name = driver.find_element(By.CSS_SELECTOR, 'div.pl_text-expander.pl_copy100.pdp_details__text-expander.js_pdp_details__text-expander.pl_text-expander--has-more.pl_text-expander--expanded table.dv_characteristicsTable:contains('') tbody tr:contains("Modellbezeichnung") td:nth-child(2)').text
            print(model_name)
            print("xxxxxxxxxxxxxxxxxxxxxxx")
            capacity = driver.find_element(By.CSS_SELECTOR,'body > div.gridAndInfoContainer.pdp-milestone-4 > div.gridContainer.mo-frame.wrapper > div > div > div:nth-child(6) > div.js_pdp_details.pl_block.pdp_details > div > div.pdp_details__characteristics-html > table:nth-child(3) > tbody > tr:nth-child(5) > td:nth-child(2)').text.split()[0]
            rpm = driver.find_element(By.CSS_SELECTOR,'body > div.gridAndInfoContainer.pdp-milestone-4 > div.gridContainer.mo-frame.wrapper > div > div > div:nth-child(6) > div.js_pdp_details.pl_block.pdp_details > div > div.pdp_details__characteristics-html > table:nth-child(3) > tbody > tr:nth-child(4) > td:nth-child(2)').text.split()[0]
            price = driver.find_element(By.CSS_SELECTOR,'body > div.gridAndInfoContainer.pdp-milestone-4 > div.gridContainer.mo-frame.wrapper > div > div > div:nth-child(4) > div.pdp_price.js_pdp_price.pl_block.pl_copy100 > div.pdp_price__inner > div.pdp_price__price.pl_mt100.js_pdp_price__price > div > div > span').text

            print("xxxxxxxxxxxxxxxxxxxxxxx")
            print(brand_name)
            print(model_name)
            print(capacity)
            print(rpm)
            print(price)
            print("xxxxxxxxxxxxxxxxxxxxxxx")

        finally:
            driver.quit()


