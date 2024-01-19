import scrapy
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import sqlite3
import re

class WdpricespyukSpider(scrapy.Spider):
    name = "wdpricespyUK"
    start_urls = ["https://pricespy.co.uk/c/washing-machines?103048=34544"]

    def parse(self, response):

        product_link = response.css("div  section  div.Content-sc-2fu3f8-2.bugHkt  div  div  div article  a::attr(href)").getall()

        for i in product_link:
            yield scrapy.Request(f"https://pricespy.co.uk{i}",callback=self.parse_product,meta ={'product_link': i})

    def parse_product(self,response):

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

            WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.CSS_SELECTOR,'#\#properties > div > section > section > div > div > div.hideInViewports-sc-0-0.iwivxM > section:nth-child(2) > div:nth-child(9) > div:nth-child(2) > span')))
            model_name = driver.find_element(By.CSS_SELECTOR, '#\#properties div section section div div div.hideInViewports-sc-0-0.iwivxM div section div:nth-child(2) div:nth-child(2) span').text.split()[1]
            capacity = driver.find_element(By.CSS_SELECTOR,'#\#properties > div > section > section > div > div > div.hideInViewports-sc-0-0.iwivxM > section:nth-child(2) > div:nth-child(2) > div:nth-child(2) > span').text.split()[0]
            capacity_dry = driver.find_element(By.CSS_SELECTOR,'#\#properties > div > section > section > div > div > div.hideInViewports-sc-0-0.iwivxM > section:nth-child(2) > div:nth-child(16) > div.Row-sc-0-3.zIQlG > div:nth-child(2) > span').text.split()[0]
            if capacity_dry == "" or capacity_dry == None:
                capacity_dry = driver.find_element(By.CSS_SELECTOR,'').text
                match = re.search(r'(\d+)\s*(?:\s*kg)?', capacity_dry)
                capacity_dry = match.group(1)
            print("xxxxxxxxxxxxxxxxxxxxxxx")
            rpm = driver.find_element(By.CSS_SELECTOR,'#\#properties > div > section > section > div > div > div.hideInViewports-sc-0-0.iwivxM > section:nth-child(2) > div:nth-child(9) > div:nth-child(2) > span').text
            print(brand_name)
            print(model_name)
            print(capacity)
            print(capacity_dry)
            print(rpm)
            print(price)

        finally:
            driver.quit()



