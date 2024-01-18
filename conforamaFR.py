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

#Product name block
brand_name = []
model_name = []
product_name_text = []
product_name = driver.find_elements(By.CSS_SELECTOR,'#addToCartForm > div.column-product.column-product_middle > div.awk-detail-product > div.typo-paragraphe.c-r_product_name > a > div.c-r_refFournisseur-grp > span')

for i in product_name:
        product_name_text.append(i.text)

product_name_text = [item for item in product_name_text if item]
for i in range(len(product_name_text)):
        pass

print(product_name_text)
for i in product_name_text:
        brand_name.append(i.split()[0])
        model_name.append(i.split()[1])

capacity = []
capacity_temp_list = driver.find_elements(By.CSS_SELECTOR,"div.awk-desc-product.product-pointfort li:nth-child(1) span")
for i in capacity_temp_list:
        capacity.append(i.text)

capacity = [re.search(r'(\d+)(?:\s*kg)?', capacity).group(1) for capacity in capacity if re.search(r'(\d+)(?:\s*kg)?', capacity)]

rpm = []
rpm_temp_list = driver.find_elements(By.CSS_SELECTOR,"div.awk-desc-product.product-pointfort li:nth-child(2) span")
for i in rpm_temp_list:
        rpm.append(i.text)
print(rpm)
print(len(rpm))
rpm = [int(re.search(r'(\d+)\s*(?:trs|ters)/min', essorage).group(1)) for essorage in rpm if re.search(r'(\d+)\s*(?:trs|ters)/min', essorage)]
print(rpm)
print(len(rpm))

