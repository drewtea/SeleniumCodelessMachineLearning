from bs4 import BeautifulSoup
from selenium import webdriver
import re
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

def filter_attribute(soup):
    # Funtion to filter the element
    # Regex pattern for style
    removeStyle = re.compile(r"display|color|colour|none", re.IGNORECASE)
    for input_style in soup.findAll("input", {'style':removeStyle}): 
        input_style.decompose()
    # Remove none-display attribute
    removeType = re.compile(r"password|submit|radio|hidden|checkbox|range|number|file|phone|button", re.IGNORECASE)
    for input_type in soup.findAll("input",attrs=({"type":removeType})):
        input_type.decompose()

    for input_hidden in soup.find_all("input", {'hidden':'hidden'}): 
        input_hidden.decompose()
    # Regex pattern for login filter
    removePattern=re.compile(r"(user|login|username|name|password|e-mail|phone|mobilephone|email|mobile|birthday|age|hidden|submit|genre|gender|vip)",re.IGNORECASE)
    # Decompose all elements which have login pattern
    for class_login in soup.find_all("input", attrs={'class':removePattern}):
        class_login.decompose()
    for id_login in soup.find_all("input", attrs={'id':removePattern}):
        id_login.decompose()
    for name_login in soup.find_all("input", attrs={'name':removePattern}):
        name_login.decompose()
    for label_login in soup.find_all("input", attrs={'aria-label':removePattern}):
        label_login.decompose()
    for placeholder_login in soup.find_all("input", attrs={'placeholder':removePattern}):
        placeholder_login.decompose()

def filter_element(raw_data):
    if len(raw_data)>1:
        for r in raw_data:
            if (r.has_attr('autocomplete') or r.has_attr('autocapitalize') 
                    or r.has_attr('spellcheck') or r.has_attr('aria-autocomplete')
                    or r.has_attr('autofocus')):
                raw_data=r
                a=[]
                a.append(raw_data)
    return a

driver = webdriver.Chrome()
url = "https://www.google.com"
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
filter_attribute(soup)
raw_data = soup.findAll("input")
if not raw_data:
    print('Error')
if len(raw_data)>1:
        for r in raw_data:
            if (r.has_attr('autocomplete') or r.has_attr('autocapitalize') 
                    or r.has_attr('spellcheck') or r.has_attr('aria-autocomplete')
                    or r.has_attr('autofocus')):
                raw_data=r
print(raw_data)




# print(soup.prettify())
