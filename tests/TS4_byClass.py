import os
from pathlib import Path
import unittest
import time
import HtmlTestRunner
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

log_dir = Path.cwd().parents[1]/ 'reports' / 'logs'

class GoogleSearch(unittest.TestCase):
    # declare variable to store the URL to be visited
    base_url="ttps://www.nytimes.com"
    
    # --- Pre - Condition ---
    # declare variable to store search term
    search_term="Test Automation with ML/AI"
    # profile = webdriver.FirefoxProfile('C:\\Users\\Phuc\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\3932hiqc.default')
    
    def setUp(self):
        # declare and initialize driver variable
        profile = webdriver.FirefoxProfile('C:\\Users\\Phuc\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\3932hiqc.default')
        profile.set_preference("webdriver.log.file",log_dir)
        self.driver=webdriver.Firefox(profile)
       
        # browser should be loaded in maximized window
        self.driver.maximize_window()

        # driver should wait implicitly for a given duration, for the element under consideration to load.
        # to enforce this setting we will use builtin implicitly_wait() function of our 'driver' object.
        self.driver.implicitly_wait(10)  #10 is in seconds

   
    # --- Steps ---
    
    def test_search(self):
        # to load a given URL in browser window
        self.driver.get(self.base_url) 
        
        # to enter search term, we need to locate the search textbox
        search_term=self.driver.find_element_by_class_name('p-player-search__input p-player-search__input--md')

        # to clear any text in the search textbox
        search_term.clear()

        # to enter the search term in the search textbox via send_keys() function
        search_term.send_keys(self.search_term)

        # to search for the entered search term
        search_term.send_keys(Keys.RETURN) 
        
if __name__ == '__main__':
    unittest.main(testRunner=HtmlTestRunner.HTMLTestRunner(output="D:\CCN\Intership_TSP\CodelessML\reports"))