from bs4 import BeautifulSoup
from selenium import webdriver
driver = webdriver.Chrome()
url = "https://dailymotion.com"
driver.get(url)
# driver.maximize_window()
# driver.implicitly_wait(10)
soup = BeautifulSoup(driver.page_source, 'lxml')
driver.quit()
for raw_data in soup.findAll("input"): 
    print(raw_data)
    print (type(raw_data))

# print(soup.prettify())
