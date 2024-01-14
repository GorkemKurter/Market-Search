import scrapy
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
driver = webdriver.Chrome(options=chrome_options)
driver.get("https://pricespy.co.uk/home-interior/white-goods/laundry-care/washing-machines/haier-hwd100-b14979s-silver--p5411676#properties")
cookie_popup_button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#root-modal > div > div > div > div > div > div.StyledFooterContent--1idxbh6.cxOYpt > div > button.BaseButton--onihrq.djcpuv.primarybutton > span')))
cookie_popup_button.click()
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")


product_name = driver.find_element(By.CSS_SELECTOR,'#\#properties div section section div div div.hideInViewports-sc-0-0.iwivxM div section div:nth-child(2) div:nth-child(2) span').text.split()[1]
print(product_name)
capacity = driver.find_element(By.CSS_SELECTOR,'#\#properties > div > section > section > div > div > div.hideInViewports-sc-0-0.iwivxM > section:nth-child(2) > div:nth-child(2) > div:nth-child(2) > span').text
print(capacity)
print("xxxxxxxxxxxxxxxxxxxxxxx")
rpm = driver.find_element(By.CSS_SELECTOR,'#\#properties > div > section > section > div > div > div.hideInViewports-sc-0-0.iwivxM > section:nth-child(2) > div:nth-child(9) > div:nth-child(2) > span').text
print(rpm)

driver.get("https://pricespy.co.uk/home-interior/white-goods/laundry-care/washing-machines/haier-hwd100-b14979s-silver--p5411676#statistics")
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
time.sleep(10)
price = driver.find_element(By.CSS_SELECTOR,'#\#statistics > div > section > section > div > div.StyledPriceHistoryArea-sc-0-0.dBNVRg > div > div.StyledFooter-sc-0-0.kybaJZ > div:nth-child(2) > div:nth-child(2) > h3').text.replace("£", "")
print(price)
print("xxxxxxxxxxxxxxxxxxxxxxx")
