from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import re
import time

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
driver = webdriver.Chrome(options=chrome_options)
driver.get("https://www.conforama.fr/special/gros-electromenager/lavage/lave-linge/c/070101/NW-6426-type-ouverture~hublot/NW-4169-sechant~non?p=1")
try:
        cookie_popup_button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'#onetrust-accept-btn-handler')))
        cookie_popup_button.click()
except Exception as e:
        print(e)

product_links = []
brand_names = []
capacities = []

WebDriverWait(driver,20).until(EC.presence_of_element_located((By.CSS_SELECTOR,'#addToCartForm > div.column-product.column-product_middle > div.awk-detail-product > div.typo-paragraphe.c-r_product_name > a')))
product_links_temp = driver.find_elements(By.CSS_SELECTOR,'#addToCartForm > div.column-product.column-product_middle > div.awk-detail-product > div.typo-paragraphe.c-r_product_name > a')
for i in product_links_temp:
        product_links.append(i.get_attribute("href"))
brand_names_temp = driver.find_elements(By.CSS_SELECTOR,'#addToCartForm > div.column-product.column-product_middle > div.awk-detail-product > div.typo-paragraphe.c-r_product_name > a > div.c-r_refFournisseur-grp')
for i in brand_names_temp:
        brand_names.append(i.text)
print(brand_names)
capacities_temp = driver.find_elements(By.CSS_SELECTOR,'#addToCartForm > div.column-product.column-product_middle > div.awk-detail-product > div.awk-desc-product.product-pointfort > ul > li:nth-child(1) > span')
for i in capacities_temp:
        capacities.append(i.text.split()[1])
print(capacities)
print(len(capacities))