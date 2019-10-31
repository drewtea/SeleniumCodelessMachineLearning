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


def test_search(soup):
    if soup.has_attr('name'):
        print('search by name')
    elif soup.has_attr('placeholder'):
       print()
    elif soup.has_attr('class'):
        print()
    elif soup.has_attr('id'):
        print()
    elif soup.has_attr('aria-label'):
        print
    elif soup.has_attr('title'):
        print
    elif soup.has_attr('tabindex'):
        print
    elif soup.has_attr('role'):
        print
    elif soup.has_attr('accesskey'):
        print
    elif soup.has_attr('type'):
        print


def locator_search(raw_data):
    if 'name' in raw_data:
        locator = driver.find_element_by_name(raw_data['name'])
    elif 'placeholder' in raw_data:
        locator = driver.find_element_by_xpath("//input[@placeholder='" + raw_data['placeholder'] + "']")
    elif 'class' in raw_data:
        locator = driver.find_element_by_class_name(raw_data['class'])
    elif 'id' in raw_data:
        locator = driver.find_element_by_id(raw_data['id'])
    elif 'aria-label' in raw_data:
        locator = driver.find_element_by_xpath("//input[@aria-label='" + raw_data['aria-label'] + "']")
    elif 'title' in raw_data:
        locator = driver.find_element_by_xpath("//input[@title='" + raw_data['title'] + "']")
    elif 'tabindex' in raw_data:
        locator = driver.find_element_by_xpath("//input[@tabindex='" + raw_data['tabindex'] + "']")
    elif 'role' in raw_data:
        locator = driver.find_element_by_xpath("//input[@role='" + raw_data['role'] + "']")
    elif 'accesskey' in raw_data:
        locator = driver.find_element_by_xpath("//input[@accesskey='" + raw_data['accesskey'] + "']")
    elif 'type' in raw_data:
        locator = driver.find_element_by_xpath("//input[@title='search']")
    return locator

# Construct dict for locator handler
# locator_handler = {
#                     raw_data['name']: driver.find_element_by_name(raw_data['name']),
#                     raw_data['placeholder']: driver.find_element_by_xpath("//input[@placeholder='" + raw_data['placeholder'] + "']"),
#                     raw_data['class']: driver.find_element_by_class_name(raw_data['class']),
#                     raw_data['id']: driver.find_element_by_id(raw_data['id'])
#                 }

# list
# locator_handler = [
#                     (raw_data['name'], driver.find_element_by_name(raw_data['name'])),
#                     (raw_data['placeholder'], driver.find_element_by_xpath("//input[@placeholder='" + raw_data['placeholder'] + "']")),
#                     (raw_data['class'], driver.find_element_by_class_name(raw_data['class'])),
#                     (raw_data['id'], driver.find_element_by_id(raw_data['id']))
#                 ]
for whichDict, whichFunc in locator_handler:
    try:
        search_box = locator_handler
    except KeyError:
        continue
    else:
        whichFunc()
        break
else:
    print('CAN NOT TEST')

# define xpath queries
        xpaths = ["//input[@name='" + raw_data['name'] + "']", 
                  "//input[@placeholder='" + raw_data['placeholder'] + "']",
                  "//input[@class='" + raw_data['class'] + "']",
                  "//input[@id='" + raw_data['id'] + "']",
                  "//input[@aria-label='" + raw_data['aria-label'] + "']",
                  "//input[@title='" + raw_data['title'] + "']",
                  "//input[@tabindex='" + raw_data['tabindex'] + "']",
                  "//input[@role='" + raw_data['role'] + "']",
                  "//input[@accesskey='" + raw_data['accesskey'] + "']",
                  "//input[@title='search']"                  
                  ]


########################

def locator_search(raw_data):
    if 'name' in raw_data:
        try:
            locator = driver.find_element_by_name(raw_data['name'])
        except (NoSuchElementException ,ElementNotVisibleException, ElementNotInteractableException):
            return []
    elif 'placeholder' in raw_data:
        try:
            locator = driver.find_element_by_xpath("//input[@placeholder='" + raw_data['placeholder'] + "']")
        except (NoSuchElementException ,ElementNotVisibleException, ElementNotInteractableException):
            return []
    elif 'class' in raw_data:
        try:
            locator = driver.find_element_by_class_name(raw_data['class'])
        except (NoSuchElementException ,ElementNotVisibleException, ElementNotInteractableException):
            return []
    elif 'id' in raw_data:
        try:
            locator = driver.find_element_by_id(raw_data['id'])
        except (NoSuchElementException ,ElementNotVisibleException, ElementNotInteractableException):
            return []
    elif 'aria-label' in raw_data:
        try:
            locator = driver.find_element_by_xpath("//input[@aria-label='" + raw_data['aria-label'] + "']")
        except (NoSuchElementException ,ElementNotVisibleException, ElementNotInteractableException):
            return []
    elif 'title' in raw_data:
        try:
            locator = driver.find_element_by_xpath("//input[@title='" + raw_data['title'] + "']")
        except (NoSuchElementException ,ElementNotVisibleException, ElementNotInteractableException):
            return []
    elif 'tabindex' in raw_data:
        try:
            locator = driver.find_element_by_xpath("//input[@tabindex='" + raw_data['tabindex'] + "']")
        except (NoSuchElementException ,ElementNotVisibleException, ElementNotInteractableException):
            return []
    elif 'role' in raw_data:
        try:
            locator = driver.find_element_by_xpath("//input[@role='" + raw_data['role'] + "']")
        except (NoSuchElementException ,ElementNotVisibleException, ElementNotInteractableException):
            return []
    elif 'accesskey' in raw_data:
        try:
            locator = driver.find_element_by_xpath("//input[@accesskey='" + raw_data['accesskey'] + "']")
        except (NoSuchElementException ,ElementNotVisibleException, ElementNotInteractableException):
            return []
    elif 'type' in raw_data:
        try:
            locator = driver.find_element_by_xpath("//input[@title='search']")
        except (NoSuchElementException ,ElementNotVisibleException, ElementNotInteractableException):
            return []
    return locator



    ####
    def locator_search(raw_data):

    try:
        locator = driver.find_element_by_name(raw_data['name'])
        locator.clear()
    except (NoSuchElementException ,ElementNotVisibleException, ElementNotInteractableException):
        return []

    try:
        locator = driver.find_element_by_xpath("//input[@placeholder='" + raw_data['placeholder'] + "']")
        locator.clear()
    except (NoSuchElementException ,ElementNotVisibleException, ElementNotInteractableException):
        return []

    try:
        locator = driver.find_element_by_class_name(raw_data['class'])
        locator.clear()
    except (NoSuchElementException ,ElementNotVisibleException, ElementNotInteractableException):
        return []

    try:
        locator = driver.find_element_by_id(raw_data['id'])
        locator.clear()
    except (NoSuchElementException ,ElementNotVisibleException, ElementNotInteractableException):
        return []

    try:
        locator = driver.find_element_by_xpath("//input[@aria-label='" + raw_data['aria-label'] + "']")
        locator.clear()
    except (NoSuchElementException ,ElementNotVisibleException, ElementNotInteractableException):
        return []

    try:
        locator = driver.find_element_by_xpath("//input[@title='" + raw_data['title'] + "']")
        locator.clear()
    except (NoSuchElementException ,ElementNotVisibleException, ElementNotInteractableException):
        return []

    try:
        locator = driver.find_element_by_xpath("//input[@tabindex='" + raw_data['tabindex'] + "']")
        locator.clear()
    except (NoSuchElementException ,ElementNotVisibleException, ElementNotInteractableException):
        return []

    try:
        locator = driver.find_element_by_xpath("//input[@role='" + raw_data['role'] + "']")
        locator.clear()
    except (NoSuchElementException ,ElementNotVisibleException, ElementNotInteractableException):
        return []

    try:
        locator = driver.find_element_by_xpath("//input[@accesskey='" + raw_data['accesskey'] + "']")
        locator.clear()
    except (NoSuchElementException ,ElementNotVisibleException, ElementNotInteractableException):
        return []

    try:
        locator = driver.find_element_by_xpath("//input[@title='search']")
        locator.clear()
    except (NoSuchElementException ,ElementNotVisibleException, ElementNotInteractableException):
        return []
    return locator


    #######
    def locator_search(raw_data):
    if 'name' in raw_data:
        try:
            locator = driver.find_element_by_name(raw_data['name'])
            locator.clear()
            locator.send_keys(SEARCH_TERM)
            locator.send_keys(Keys.RETURN)
        except (NoSuchElementException ,ElementNotVisibleException, ElementNotInteractableException):
            return []
    elif 'placeholder' in raw_data:
        try:
            locator = driver.find_element_by_xpath("//input[@placeholder='" + raw_data['placeholder'] + "']")
            locator.send_keys(SEARCH_TERM)
            locator.send_keys(Keys.RETURN)
        except (NoSuchElementException ,ElementNotVisibleException, ElementNotInteractableException):
            return []
    elif 'class' in raw_data:
        try:
            locator = driver.find_element_by_class_name(raw_data['class'])
            locator.send_keys(SEARCH_TERM)
            locator.send_keys(Keys.RETURN)
        except (NoSuchElementException ,ElementNotVisibleException, ElementNotInteractableException):
            return []
    elif 'id' in raw_data:
        try:
            locator = driver.find_element_by_id(raw_data['id'])
            locator.send_keys(SEARCH_TERM)
            locator.send_keys(Keys.RETURN)
        except (NoSuchElementException ,ElementNotVisibleException, ElementNotInteractableException):
            return []
    elif 'aria-label' in raw_data:
        try:
            locator = driver.find_element_by_xpath("//input[@aria-label='" + raw_data['aria-label'] + "']")
        except (NoSuchElementException ,ElementNotVisibleException, ElementNotInteractableException):
            return []
    elif 'title' in raw_data:
        try:
            locator = driver.find_element_by_xpath("//input[@title='" + raw_data['title'] + "']")
        except (NoSuchElementException ,ElementNotVisibleException, ElementNotInteractableException):
            return []
    elif 'tabindex' in raw_data:
        try:
            locator = driver.find_element_by_xpath("//input[@tabindex='" + raw_data['tabindex'] + "']")
        except (NoSuchElementException ,ElementNotVisibleException, ElementNotInteractableException):
            return []
    elif 'role' in raw_data:
        try:
            locator = driver.find_element_by_xpath("//input[@role='" + raw_data['role'] + "']")
        except (NoSuchElementException ,ElementNotVisibleException, ElementNotInteractableException):
            return []
    elif 'accesskey' in raw_data:
        try:
            locator = driver.find_element_by_xpath("//input[@accesskey='" + raw_data['accesskey'] + "']")
        except (NoSuchElementException ,ElementNotVisibleException, ElementNotInteractableException):
            return []
    elif 'type' in raw_data:
        try:
            locator = driver.find_element_by_xpath("//input[@title='search']")
        except (NoSuchElementException ,ElementNotVisibleException, ElementNotInteractableException):
            return []
    return locator



    ####################

    if 'name' in raw_data:
        try:
            locator = driver.find_element_by_name(raw_data['name'])
            locator.clear()
            locator.send_keys(SEARCH_TERM)
            locator.send_keys(Keys.RETURN)
            
        except (NoSuchElementException ,ElementNotVisibleException, ElementNotInteractableException):
            
            pass
    if 'placeholder' in raw_data:
        try:
            locator = driver.find_element_by_xpath("//input[@placeholder='" + raw_data['placeholder'] + "']")
            locator.clear()
            locator.send_keys(SEARCH_TERM)
            locator.send_keys(Keys.RETURN)
        except (NoSuchElementException ,ElementNotVisibleException, ElementNotInteractableException):
            pass
    if 'class' in raw_data:
        try:
            locator = driver.find_element_by_class_name(raw_data['class'])
            locator.clear()
            locator.send_keys(SEARCH_TERM)
            locator.send_keys(Keys.RETURN)
        except (NoSuchElementException ,ElementNotVisibleException, ElementNotInteractableException):
            pass
    if 'id' in raw_data:
        try:
            locator = driver.find_element_by_id(raw_data['id'])
            locator.clear()
            locator.send_keys(SEARCH_TERM)
            locator.send_keys(Keys.RETURN)
        except (NoSuchElementException ,ElementNotVisibleException, ElementNotInteractableException):
            pass
    if 'aria-label' in raw_data:
        try:
            locator = driver.find_element_by_xpath("//input[@aria-label='" + raw_data['aria-label'] + "']")
            locator.clear()
            locator.send_keys(SEARCH_TERM)
            locator.send_keys(Keys.RETURN)
        except (NoSuchElementException ,ElementNotVisibleException, ElementNotInteractableException):
            pass
    if 'title' in raw_data:
        try:
            locator = driver.find_element_by_xpath("//input[@title='" + raw_data['title'] + "']")
            locator.clear()
            locator.send_keys(SEARCH_TERM)
            locator.send_keys(Keys.RETURN)
        except (NoSuchElementException ,ElementNotVisibleException, ElementNotInteractableException):
            pass
     # if 'tabindex' in raw_data:
    #     try:
    #         locator = driver.find_element_by_xpath("//input[@tabindex='" + raw_data['tabindex'] + "']")
    #         locator.clear()
    #         locator.send_keys(SEARCH_TERM)
    #         locator.send_keys(Keys.RETURN)
    #     except (NoSuchElementException ,ElementNotVisibleException, ElementNotInteractableException):
    #         pass
    if 'role' in raw_data:
        try:
            locator = driver.find_element_by_xpath("//input[@role='" + raw_data['role'] + "']")
            locator.clear()
            locator.send_keys(SEARCH_TERM)
            locator.send_keys(Keys.RETURN)
        except (NoSuchElementException ,ElementNotVisibleException, ElementNotInteractableException):
            pass
    if 'accesskey' in raw_data:
        try:
            locator = driver.find_element_by_xpath("//input[@accesskey='" + raw_data['accesskey'] + "']")
            locator.clear()
            locator.send_keys(SEARCH_TERM)
            locator.send_keys(Keys.RETURN)
        except (NoSuchElementException ,ElementNotVisibleException, ElementNotInteractableException):
            pass
    if 'type' in raw_data:
        try:
            locator = driver.find_element_by_xpath("//input[@title='search']")
            locator.clear()
            locator.send_keys(SEARCH_TERM)
            locator.send_keys(Keys.RETURN)
        except (NoSuchElementException ,ElementNotVisibleException, ElementNotInteractableException):
            return []
    return locator
