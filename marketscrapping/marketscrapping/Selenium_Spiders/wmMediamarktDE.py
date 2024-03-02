import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

#https://www.mediamarkt.es/es/category/lavadoras-671.html
chrome_options = Options()
#chrome_options.add_argument('--headless')
chrome_options.add_argument("--ignore-certificate-error")
chrome_options.add_argument("--ignore-ssl-errors")
driver = webdriver.Chrome(options=chrome_options)
#driver.get("https://www.conforama.es/electrodomesticos/lavadoras/lavadoras-de-carga-frontal")
driver.get("https://www.mediamarkt.es/es/category/lavadoras-671.html")

try:
    pop_up_button2 = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'#pwa-consent-layer-accept-all-button')))
    pop_up_button2.click()
except Exception as e:
    print(e)

for i in range(1, 13):
    time.sleep(1)
    product_link = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR,f'#main-content > div.sc-89725820-0.fqRTWa > div.sc-f9f83eec-0.dkSVao > div.sc-835d3f28-0.kTdeVZ > div > div.sc-572c0887-0.oLQeQ > div:nth-child({i}) > div > div > div > div.sc-b038b935-0.iVqexX > a'))).text
