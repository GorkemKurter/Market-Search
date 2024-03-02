from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
#https://www.mediamarkt.es/es/category/lavadoras-671.html
chrome_options = Options()
#chrome_options.add_argument('--headless')
chrome_options.add_argument("--ignore-certificate-error")
chrome_options.add_argument("--ignore-ssl-errors")
driver = webdriver.Chrome(options=chrome_options)
driver.get("https://www.mediamarkt.es/es/category/lavadoras-671.html")
#time.sleep(3600)

try:
    pop_up_button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'#pwa-consent-layer-accept-all-button')))
    pop_up_button.click()
except Exception as e:
    print(e)
    print("There was an error during clicking cookie button")

for i in range(1, 13):
    product_title = pop_up_button = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR,f'#main-content > div.sc-89725820-0.fqRTWa > div.sc-f9f83eec-0.dkSVao > div.sc-835d3f28-0.kTdeVZ > div > div.sc-5d392fc9-0.fceyFV > div:nth-child({i}) > div > div > div > a > div > p'))).text
    print(product_title)



































































































































