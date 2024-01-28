import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import undetected_chromedriver as uc
from seleniumbase import BaseCase
import sqlite3

'''url = "https://www.worten.es/productos/electrodomesticos/lavado-y-cuidado-de-la-ropa/lavadoras/carga-frontal"
chrome_options = Options()'''
#chrome_options.add_argument('--headless')
'''chrome_options.add_argument('--guest')
chrome_options.add_argument("--ignore-certificate-error")
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option('useAutomationExtension', False)
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_argument("--ignore-ssl-errors")
chrome_options.add_argument("--auto-open-devtools-for-tabs")'''
'''open("https://www.worten.es/productos/electrodomesticos/lavado-y-cuidado-de-la-ropa/lavadoras/carga-frontal")
WebDriverWait(driver, 20).until(EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR,"iframe[title='Cloudflare güvenlik görevi içeren pencere öğeleri']")))
WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#challenge-stage > div > label"))).click()
brand_name = WebDriverWait(driver,30).until(EC.presence_of_element_located((By.CSS_SELECTOR,"#filtered-grid > div > div > section > div > div.listing-content__list-container > ul > li:nth-child(2) > div > a > div > div.product-card__text-container > div.product-card__details > div.product-card__name-and-features > h3 > span")))
print(brand_name)
#challenge-stage > div > label > input[type=checkbox]'''


from seleniumbase import SB


def verify_success(sb):
    pass
    #sb.assert_element('img[alt="Logo Assembly"]', timeout=8)
    #sb.sleep(4)

with SB(uc_cdp=True, guest_mode=True) as sb:
    sb.open("https://www.worten.es/productos/electrodomesticos/lavado-y-cuidado-de-la-ropa/lavadoras/carga-frontal")
    try:
        verify_success(sb)
    except Exception:
        if sb.is_element_visible('input[type=checkbox]'):
            sb.click('#challenge-stage > div > label')
        elif sb.is_element_visible("iframe[title='Cloudflare güvenlik görevi içeren pencere öğeleri']"):
            sb.switch_to_frame("iframe[title='Cloudflare güvenlik görevi içeren pencere öğeleri']")
            sb.click("#challenge-stage > div > label")
        else:
            raise Exception("Detected!")
        try:
            verify_success(sb)
        except Exception:
            raise Exception("Detected!")

brand_name = WebDriverWait(sb, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR,"#filtered-grid > div > div > section > div > div.listing-content__list-container > ul > li:nth-child(2) > div > a > div > div.product-card__text-container > div.product-card__details > div.product-card__name-and-features > h3 > span")))
print(brand_name)




'''url = "https://www.worten.es/productos/electrodomesticos/lavado-y-cuidado-de-la-ropa/lavadoras/carga-frontal"
chrome_options = Options()

driver = webdriver.Chrome(options=chrome_options)

WebDriverWait(sb, 20).until(EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR,"iframe[title='Cloudflare güvenlik görevi içeren pencere öğeleri']")))
WebDriverWait(sb, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#challenge-stage > div > label"))).click()
brand_name = WebDriverWait(sb,30).until(EC.presence_of_element_located((By.CSS_SELECTOR,"#filtered-grid > div > div > section > div > div.listing-content__list-container > ul > li:nth-child(2) > div > a > div > div.product-card__text-container > div.product-card__details > div.product-card__name-and-features > h3 > span")))
print(brand_name)'''
