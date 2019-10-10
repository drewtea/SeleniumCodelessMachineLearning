from selenium import webdriver
from selenium.webdriver.firefox.webdriver import FirefoxProfile

profile = FirefoxProfile('C:\\Users\\Phuc\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\3932hiqc.default')
driver = webdriver.Firefox(profile)
driver.get('https://www.mlb.com/')
search = driver.find_element_by_class_name('p-icon p-icon--search')
search.send
