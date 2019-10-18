from bs4 import BeautifulSoup
from selenium import webdriver
import re
from millionsSites import filter_element
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()
url = "https://www.vk.com"
driver.get(url)
timeout = 2
try:
    element_present = EC.presence_of_element_located((By.XPATH, '//input'))
    WebDriverWait(driver, timeout).until(element_present)
except TimeoutException:
    print ("Timed out waiting for page to load")
# driver.maximize_window()
# driver.implicitly_wait(10)

soup = BeautifulSoup(driver.page_source, 'lxml')
driver.quit()
filter_element(soup)
raw_data = soup.findAll("input")
if not raw_data:
    print('Error')
else:
    print(raw_data)

# print(soup.prettify())
