import unittest
import HtmlTestRunner
import time
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


# Chose the browser for testing
# browser = webdriver.Chrome()    # Chrome version: 78.0.3904.70 (Official Build) (64-bit)
# browser = webdriver.Firefox()   # Firefox verion: 70.0 (64-bit)
# browser = webdriver.Opera()     # Opera version: 76.0.3809.132
# browser = webdriver.Ie()        # Internet Explorer version: 11.418.18362
# browser = webdriver.Edge        # Microsoft Edge version: 44.18362.387.0 build 18362 

COOKIE_EXTENTION = Path("extention") / "cookie.crx"
UBLOCK_EXTENTION = Path("extention") / "ublock.crx"

class Webdriver(unittest.TestCase):
    # declare variable to store the URL to be visited

    # --- Pre - Condition ---
    def setUp(self,url):
        options = webdriver.ChromeOptions()
        options.add_extension(COOKIE_EXTENTION)
        options.add_extension(UBLOCK_EXTENTION)
        # declare and initialize driver variable
        self.driver=webdriver.Chrome(chrome_options=options)
        # to load a given URL in browser window
        self.driver.get(self.url)
       
        # browser should be loaded in maximized window
        self.driver.maximize_window()

        # driver should wait implicitly for a given duration, for the element under consideration to load.
        # to enforce this setting we will use builtin implicitly_wait() function of our 'driver' object.
        self.driver.implicitly_wait(10)  #10 is in seconds
        # Wait for page to load full
        timeout = 5
        try:
            element_present = EC.presence_of_element_located((By.XPATH, '//input'))
            WebDriverWait(self.driver, timeout).until(element_present)
        except TimeoutException:
            print("Timed out waiting for page to load")



    # --- Steps ---
    
    def test_search(self, url):
        # to load a given URL in browser window
        self.driver.get(self.url) 
        
        # to enter search term, we need to locate the search textbox
        search_term=self.driver.find_element_by_xpath("//input[@id='ts_input']")

        # to clear any text in the search textbox
        search_term.clear()

        # to enter the search term in the search textbox via send_keys() function
        search_term.send_keys(self.search_term)

        # to search for the entered search term
        search_term.send_keys(Keys.RETURN)

        # to verify if the search results page loaded
        #self.assertIn(self.search_term,self.driver.title)

        # to verify if the search results page contains any results or no results were found.
        # self.assertNotIn("No results found.",self.driver.page_source)

    # --- Post - Condition ---
    # def tearDown(self):
    #     # to close the browser
    #     self.driver.close()

if __name__ == '__main__':
    unittest.main(testRunner=HtmlTestRunner.HTMLTestRunner(output="D:\\CCN\\Intership_TSP\\CodelessML\\reports"))