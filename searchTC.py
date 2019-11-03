import unittest
import time, os, re
import HtmlTestRunner
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException, ElementNotVisibleException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from pathlib import Path
from selenium.webdriver.chrome.options import Options

COOKIE_EXTENTION = Path("extention") / "cookie.crx"
UBLOCK_EXTENTION = Path("extention") / "ublock.crx"


DRIVER_PATH = Path('webdriver')
REPORT_PATH = Path('results') / 'reports'
LOG_PATH =Path('results') / 'logs'
SEARCH_TERM = "Test Automation with ML/AI"


# Chose the browser for testing
# browser = webdriver.Firefox()   # Firefox verion: 70.0 (64-bit)
# browser = webdriver.Chrome()    # Chrome version: 78.0.3904.70 (Official Build) (64-bit)
# browser = webdriver.Opera()     # Opera version: 76.0.3809.132
# browser = webdriver.Ie()        # Internet Explorer version: 11.418.18362
# browser = webdriver.Edge        # Microsoft Edge version: 44.18362.387.0 build 18362 

class LocatorElement():
    """Your class which is doing the scraping"""
    def find_element(self, xpath, url):
        """A handy function to try and find the element and catch exception as error verdict.

        Args:
            xpath (str): the xpath string you are trying to find

        Returns:
            List of elements
        """
        options = webdriver.ChromeOptions()
        options.add_extension(COOKIE_EXTENTION)
        options.add_extension(UBLOCK_EXTENTION)
        # declare and initialize driver variable
        self.driver=webdriver.Chrome(chrome_options=options)
        self.driver.get(url)
        try:
            self.driver.find_element_by_xpath(xpath)
            self.driver.clear
            return self.driver.find_element_by_xpath(xpath)
        except (NoSuchElementException ,ElementNotVisibleException, ElementNotInteractableException):
            return []

    def xpaths_build (self, raw_data):
        """A method to build the xpath queries based on the scraped data from website.

        Args:
            raw_data (dict): the raw_data scraped from websites store in dictionary

        Returns:
            List of xpath queries
        """
        # List to store xpaths
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
        return xpaths

    def find_locator(self, raw_data, url):
        """method to find your locators

        Args:
            raw_data (dict): the raw_data scraped from websites store in dictionary

        Returns:
            list of locators, or empty list if no locators found
        """
        # define xpath queries
        xpaths = self.xpaths_build(raw_data)
        # iterate through them
        for xpath in xpaths:
            locators = self.find_element(xpath,url)
            if locators:
                # until you are successful 
                return locators

        # or return empty list if no locators found
            return []


class SearchTest(unittest.TestCase):

    def setUp(self,url):
        
        '''
            Setup browser driven by Selenium module
        '''
        # declare and initialize driver variable
        # self.driver =  getattr(webdriver)
        option = webdriver.ChromeOptions()
        option = webdriver.ChromeOptions()
        option.add_extension(COOKIE_EXTENTION)
        option.add_extension(UBLOCK_EXTENTION)
        # declare and initialize driver variable
        self.driver=webdriver.Chrome(chrome_options=option)

        # Firefox
        # self.driver = webdriver.Firefox()
       
        # browser should be loaded in maximized window
        self.driver.maximize_window()

        # driver should wait implicitly for a given duration, for the element under consideration to load.
        # to enforce this setting we will use builtin implicitly_wait() function of our 'driver' object.
        self.driver.get(url)
        self.driver.implicitly_wait(3)
    
    # --- Steps ---
    '''
        Funtion to find locator
    '''
    def locator_search(self,raw_data):
        element_key = ['name','placeholder','class','id','aria-label','title','role','accesskey','type'] 
        for key in element_key:
            if key in raw_data:
                try:
                    # search_term=self.driver.find_element_by_xpath("//input[@name='query']")
                    stringxPath="//input[@" + key + "='" + raw_data[key] + "']" 
                    
                    locator = self.driver.find_element_by_xpath((stringxPath))
                    locator.clear()
                    locator.send_keys(SEARCH_TERM)
                    # self.driver.implicitly_wait(20)
                    locator.send_keys(Keys.RETURN)
                    self.driver.implicitly_wait(20)
                    # to verify if the search results page loaded
                    self.assertTrue(SEARCH_TERM in self.driver.page_source)
                    break                                     
                except (NoSuchElementException, ElementNotVisibleException, ElementNotInteractableException):
                    pass
                
        
    # def tearDown(self):
    #     # to close the browser
    #     self.driver.close()

if __name__ == '__main__':
    unittest.main(testRunner=HtmlTestRunner.HTMLTestRunner(output=REPORT_PATH))