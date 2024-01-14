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
    i = 0

    def parse(self, response):

        product_links = response.css(
            "div  section  div.Content-sc-2fu3f8-2.bugHkt  div  div  div article  a::attr(href)").getall()
        for i in product_links:
            yield scrapy.Request(url=("https://pricespy.co.uk" + i), callback=self.parse_product,meta={'product_link': i})

        next_url = response.css("#root > div > section > div.Content-sc-2fu3f8-2.bugHkt > div > div > div > div > section > main > div > span > ul > li:last-child > a::attr(href)").get()
        if next_url is not None:
            yield scrapy.Request(url = f"https://pricespy.co.uk{next_url}",callback=self.parse)

    def parse_product(self, response):
        brand_name = response.css('div  section  section  div div section span  a::text').get()
        product_link = response.meta.get('product_link', '')
        print(brand_name)
        chrome_options = Options()
        #chrome_options.add_argument('--headless')
        chrome_options.add_argument("--ignore-certificate-error")
        chrome_options.add_argument("--ignore-ssl-errors")
        driver = webdriver.Chrome(options=chrome_options)
        url = f"https://pricespy.co.uk{response.meta.get('product_link', '')}"
        driver.get(url)
        try:
            WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR,'#\#properties > div > section > section > div > div > div.hideInViewports-sc-0-0.iwivxM > section:nth-child(2) > div:nth-child(9) > div:nth-child(2) > span')))

            model_name = driver.find_element(By.CSS_SELECTOR, '#\#properties div section section div div div.hideInViewports-sc-0-0.iwivxM div section div:nth-child(2) div:nth-child(2) span').text.split()[1]
            print(model_name)
            capacity = driver.find_element(By.CSS_SELECTOR,'#\#properties > div > section > section > div > div > div.hideInViewports-sc-0-0.igwacS > section > div:nth-child(3) > div:nth-child(2) > span').text
            print(capacity)
            print("xxxxxxxxxxxxxxxxxxxxxxx")
            rpm = driver.find_element(By.CSS_SELECTOR,'#\#properties > div > section > section > div > div > div.hideInViewports-sc-0-0.iwivxM > section:nth-child(2) > div:nth-child(9) > div:nth-child(2) > span').text
            print(rpm)
            price = driver.find_element(By.CSS_SELECTOR,'#\#statistics > div > section > section > div > div.StyledPriceHistoryArea-sc-0-0.dBNVRg > div > div.StyledFooter-sc-0-0.kybaJZ > div:nth-child(2) > div:nth-child(2) > h3').text.replace("£","")
            print(price)
            #currency = driver.find_element(By.CSS_SELECTOR,)
            self.i = self.i + 1
            print(self.i)
            print("xxxxxxxxxxxxxxxxxxxxxxx")

        finally:
            driver.quit()


