import unittest
import HtmlTestRunner
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


class Search(unittest.TestCase):
    # declare variable to store the URL to be visited
    base_url="https://www.mlb.com/"

    # --- Pre - Condition ---
    def setUp(self):
        # declare and initialize driver variable
        self.driver=webdriver.Firefox(executable_path="D:\CCN\Intership_TSP\CodelessML\geckodriver.exe")
       
        # browser should be loaded in maximized window
        self.driver.maximize_window()

        # driver should wait implicitly for a given duration, for the element under consideration to load.
        # to enforce this setting we will use builtin implicitly_wait() function of our 'driver' object.
        self.driver.implicitly_wait(10)  #10 is in seconds

    # declare variable to store search term
    search_term="Raspberry"

    # --- Steps ---
    
    def test_search(self):
        # to load a given URL in browser window
        self.driver.get(self.base_url) 
        
        # to enter search term, we need to locate the search textbox
        search_term=self.driver.find_element_by_class_name("p-player-search__input p-player-search__input--md")

        # to clear any text in the search textbox
        search_term.clear()

        # to enter the search term in the search textbox via send_keys() function
        search_term.send_keys(self.search_term)

        # to search for the entered search term
        search_term.send_keys(Keys.RETURN)

        # to verify if the search results page loaded
        #self.assertIn(self.search_term,self.driver.title)

        # to verify if the search results page contains any results or no results were found.
        self.assertNotIn("No results found.",self.driver.page_source)

    # --- Post - Condition ---
    # def tearDown(self):
    #     # to close the browser
    #     self.driver.close()

if __name__ == '__main__':
    unittest.main(testRunner=HtmlTestRunner.HTMLTestRunner(output="D:\CCN\Intership_TSP\CodelessML"))