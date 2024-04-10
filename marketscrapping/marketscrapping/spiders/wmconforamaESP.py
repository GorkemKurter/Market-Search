import time

import scrapy
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

class WmconforamaespSpider(scrapy.Spider):
    name = "wmconforamaESP"
    start_urls = ["https://www.conforama.es/electrodomesticos/lavadoras/lavadoras-de-carga-frontal"]

    def parse(self, response):
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument("--ignore-certificate-error")
        chrome_options.add_argument("--ignore-ssl-errors")
        driver = webdriver.Chrome(options=chrome_options)
        driver.get("https://www.conforama.es/electrodomesticos/lavadoras/lavadoras-de-carga-frontal")
        time.sleep(120)

        #TEST PY 'YE BAK
