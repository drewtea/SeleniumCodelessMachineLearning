from bs4 import BeautifulSoup
from selenium import webdriver
import re, os
import requests
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException, ElementNotVisibleException

from pathlib import Path
from millionsSites import filter_attribute
from searchTC import LocatorElement


COOKIE_EXTENTION = Path("extention") / "cookie.crx"
UBLOCK_EXTENTION = Path("extention") / "ublock.crx"
SEARCH_TERM = "Test Automation with ML/AI"


url = "https://vk.com"


# if the webpage is rendered with JavaScript making more requests to fetch additional data.
# this case will be using Selenium to scrape the whole source page
# adding chrome extension
option = webdriver.ChromeOptions()
option.add_extension(COOKIE_EXTENTION)
option.add_extension(UBLOCK_EXTENTION)
driver = webdriver.Chrome(chrome_options=option)
driver.get(url)
driver.implicitly_wait(10)
# Wait for page to load full
# timeout = 10
# try:
#     element_present = EC.presence_of_element_located((By.XPATH, '//input'))
#     WebDriverWait(driver, timeout).until(element_present)
# except TimeoutException:
#     print("Timed out waiting for page to load")
soup = BeautifulSoup(driver.page_source, 'lxml') 
# scrape element with direct type='search'
type_search = soup.findAll("input", {"type":"search"})       
# driver.quit()
# filter attribute
filter_attribute(soup)
# scrape raw data after filter
raw_data = soup.findAll("input")
print('SCRAPED BY SELENIUM')
print(raw_data)
# if not possible to scrape the data on this website
if not raw_data:  
    """Scrape scheduled link previews."""
    session = requests.Session()
    adapter = requests.adapters.HTTPAdapter(max_retries=2)
    session.mount('https://', adapter)
    session.mount('http://', adapter)
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36"}
    page = session.get(url, headers=headers, timeout=2)
    response = page.text
    page.close()
    soup = BeautifulSoup(response, "lxml")
    type_search = soup.findAll("input", {"type":"search"})       
    # sleep(1)
    # filter element
    filter_attribute(soup)
    # Scrape raw data after filter
    raw_data = soup.findAll("input")
    print('SCRAPED BY REQUEST MODULE')
    print(raw_data)
    # collect the input element whose attribute type='search'    
    if not raw_data:
        raw_data = type_search
        if not raw_data:
            print('Error')       

####################

# convert element to dictionary type 
for r in raw_data:
    raw_data = r.attrs

''' 
    Function to locate the search element
    Input: raw_data with type is dictionary
'''
print(raw_data['class'])

# if raw_data.keys() in locator_handler
#Test Search

# adding chrome extension
# option = webdriver.ChromeOptions()
# option.add_extension(COOKIE_EXTENTION)
# option.add_extension(UBLOCK_EXTENTION)
# driver = webdriver.Chrome(chrome_options=option)
# driver.get(url)
# driver.implicitly_wait(10)
# # Wait for page to load full
# timeout = 10
# try:
#     element_present = EC.presence_of_element_located((By.XPATH, '//input'))
#     WebDriverWait(driver, timeout).until(element_present)
# except TimeoutException:
#     print("Timed out waiting for page to load")
# driver.maximize_window()
# driver.implicitly_wait(10)
###
if raw_data:
    xpaths = []

    if 'name' in raw_data:
        xpaths.append("//input[@name='" + raw_data['name'] + "']")
    if 'placeholder' in raw_data:
        xpaths.append("//input[@placeholder='" + raw_data['placeholder'] + "']")
    if 'class' in raw_data:
        xpaths.append("//input[@class='" + raw_data['class'] + "']")
    if 'id' in raw_data:
        xpaths.append("//input[@id='" + raw_data['id'] + "']")
    if 'aria-label' in raw_data:
        xpaths.append("//input[@aria-label='" + raw_data['aria-label'] + "']")
    if 'title' in raw_data:
        xpaths.append("//input[@title='" + raw_data['title'] + "']")
    if 'tabindex' in raw_data:
        xpaths.append("//input[@tabindex='" + raw_data['tabindex'] + "']")
    if 'role' in raw_data:
        xpaths.append("//input[@role='" + raw_data['role'] + "']")
    if 'accesskey' in raw_data:
        xpaths.append("//input[@accesskey='" + raw_data['accesskey'] + "']")
    if 'type' in raw_data:
        xpaths.append("//input[@title='search']")
    print(xpaths)
    # xpaths=["//input[@name='disable-autofill']","//input[@id='ts_input']"]
    # xpaths = ["//input[@name='" + raw_data['name'] + "']", 
    #               "//input[@placeholder='" + raw_data['placeholder'] + "']",
    #               "//input[@class='" + raw_data['class'] + "']",
    #               "//input[@id='" + raw_data['id'] + "']",
    #               "//input[@aria-label='" + raw_data['aria-label'] + "']",
    #               "//input[@title='" + raw_data['title'] + "']",
    #               "//input[@tabindex='" + raw_data['tabindex'] + "']",
    #               "//input[@role='" + raw_data['role'] + "']",
    #               "//input[@accesskey='" + raw_data['accesskey'] + "']",
    #               "//input[@title='search']"                  
    #               ]

    for xpath in xpaths:
        try:
            search_box = driver.find_element_by_xpath(xpath)   
            search_box.clear()
            search_box.send_keys(search_term)
            search_box.send_keys(Keys.RETURN) 
        except (NoSuchElementException ,ElementNotVisibleException, ElementNotInteractableException):
            print('VERDICT: ERROR')


# if the module can not find or interact with th locator
# write verdict = 'Error'
else:
    print('FINALLL')
    









    
    

 







