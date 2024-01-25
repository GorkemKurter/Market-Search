from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import sqlite3
import time
url = "https://www.worten.es/productos/electrodomesticos/lavado-y-cuidado-de-la-ropa/lavadoras/carga-frontal"
chrome_options = Options()
#chrome_options.add_argument('--headless')
chrome_options.add_argument("--ignore-certificate-error")
chrome_options.add_argument("--ignore-ssl-errors")
chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
driver = webdriver.Chrome(options=chrome_options)
driver.get(url)
boot_detector_button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="challenge-stage"]/div/label/input')))
boot_detector_button.click()
time.sleep(300)
#challenge-stage > div > label > input[type=checkbox]