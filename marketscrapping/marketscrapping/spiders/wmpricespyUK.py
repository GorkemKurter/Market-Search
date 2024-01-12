import scrapy
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options


class WmpricespyukSpider(scrapy.Spider):
    name = "wmpricespyUK"
    start_urls = ["https://pricespy.co.uk/c/washing-machines?1247=2342"]
    i = 0

    def parse(self, response):

        product_links = response.css("div  section  div.Content-sc-2fu3f8-2.bugHkt  div  div  div article  a::attr(href)").getall()
        for i in product_links:
            yield scrapy.Request(url=("https://pricespy.co.uk" + i + "#properties") ,callback = self.parse_product,meta={'product_link': i})
    def parse_product(self, response):
    
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        driver = webdriver.Chrome(options=chrome_options)
        url = f"https://pricespy.co.uk{response.meta.get('product_link', '')}#properties"
        driver.get(url)
        try:
            element = WebDriverWait(driver,5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR,'#\#properties > div > section > section > div > div > div.hideInViewports-sc-0-0.iwivxM > div > section > div:nth-child(2) > div:nth-child(2) > span')))

            
            product_name = element.text
            print(product_name)
            print("xxxxxxxxxxxxxxxxxxxxxxx")
            self.i = self.i + 1
            print(self.i)
            print("xxxxxxxxxxxxxxxxxxxxxxx")

        finally:
            driver.quit()

        brand_name = response.css('div  section  section  div div section span  a::text').get()
        print(brand_name)
