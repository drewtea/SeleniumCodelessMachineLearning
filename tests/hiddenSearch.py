import unittest
import os
from pathlib import Path
import time
import HtmlTestRunner
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

log_dir = Path.cwd().parents[1]/ 'reports' / 'logs' 
report_dir = Path.cwd().parents[1]/ 'reports' 


class HiddenSearchBar(unittest.TestCase):
    # declare variable to store the URL to be visited
    base_url="https://www.nytimes.com/"
    
    # --- Pre - Condition ---
    # declare variable to store search term
    search_term="Test Automation with ML/AI"

    def setUp(self):
        # profile = webdriver.FirefoxProfile('C:\\Users\\Phuc\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\3932hiqc.default')
        # profile = webdriver.FirefoxProfile()
        # declare and initialize driver variable
        self.driver=webdriver.Firefox(service_log_path = os.path.devnull)
       
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
        # search_term=self.driver.find_element_by_class_name("css-1fe7a5q")
        click_button=self.driver.find_element_by_xpath("//button[@class='css-1tho1qm ewfai8r0']")
        click_button.click()
        search_term=self.driver.find_element_by_xpath("//input[@name='query']")
        # to clear any text in the search textbox
        # search_term.clear()

        # to enter the search term in the search textbox via send_keys() function
        search_term.send_keys(self.search_term)

        # to search for the entered search term
        search_term.send_keys(Keys.RETURN) 

        
if __name__ == '__main__':
    unittest.main(testRunner=HtmlTestRunner.HTMLTestRunner(output=report_dir))