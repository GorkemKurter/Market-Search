from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import sqlite3
import time

chrome_options = Options()
#chrome_options.add_argument('--headless')
chrome_options.add_argument("--ignore-certificate-error")
chrome_options.add_argument("--ignore-ssl-errors")
driver = webdriver.Chrome(options=chrome_options)

url = 'https://www.eldorado.ru/c/stiralnye-mashiny/f/s-frontalnoy-zagruzkoy/?f_1629037=708115806'
driver.get(url)
time.sleep(30)
driver.quit()
