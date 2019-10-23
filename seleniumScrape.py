from bs4 import BeautifulSoup
from selenium import webdriver
import re
import requests
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from pathlib import Path

from millionsSites import filter_attribute

cookie_extention = Path("extention")/ "cookie.crx"


url = "https://imgur.com"

session = requests.Session()
adapter = requests.adapters.HTTPAdapter(max_retries=2)
session.mount('https://', adapter)
session.mount('http://', adapter)
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36"}
page = session.get(url, headers=headers, timeout=2)
response = page.text
page.close()
soup = BeautifulSoup(response, "lxml")
# sleep(1)
# filter element
filter_attribute(soup)
# Scrape raw data after filter
raw_data = soup.findAll("input")

# raw_data =[]
if not raw_data:
    # if the webpage is rendered with JavaScript making more requests to fetch additional data.
    # this case will be using Selenium to scrape the whole source page
    # adding chrome extension
    option = webdriver.ChromeOptions()
    option.add_extension(cookie_extention)
    driver = webdriver.Chrome(chrome_options=option)
    driver.get(url)
    driver.implicitly_wait(10)
    # Wait for page to load full
    timeout = 10
    try:
        element_present = EC.presence_of_element_located((By.XPATH, '//input'))
        WebDriverWait(driver, timeout).until(element_present)
    except TimeoutException:
        print("Timed out waiting for page to load")
    soup = BeautifulSoup(driver.page_source, 'lxml')        
    driver.quit()
    # filter attribute
    filter_attribute(soup)
    # scrape raw data after filter
    raw_data = soup.findAll("input")

    # convert raw_data to dictionary
    # raw_data = raw_data.attrs
    if not raw_data:
        # if not possible to scrape the data
        # write verdict = 'ERROR' 
        print('Error_1')    
         
    # convert raw data to string format
    # data_s=str(raw_data)
    # # convert raw data to dictionary 
    # data_dict={k:v.strip('"') for k,v in re.findall(r'(\S+)=(".*?"|\S+)', data_s)}

# If list has more than one element
# => filter again
attributes = ['autocomplete', 'autocapitalize', 'aria-autocomplete', 
              'spellcheck','autofocus']
print(len(raw_data))
# for k in raw_data:
#     print(k)

if len(raw_data)>1:
    for r in raw_data:      
        check_attr = {k: r.has_attr(k) for k in attributes}
        if True in check_attr.values():
            a=[]
            a.append(r)
            raw_data=a            
        else:
            print('Error_2')
print(raw_data)
 







