from pathlib import Path
from time import sleep
import re
from bs4 import BeautifulSoup
from selenium import webdriver
from itertools import islice
import requests
import csv
import linecache
from timeit import default_timer as timer
from datetime import *
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException, ElementNotVisibleException
import os
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

def mode_local(browser_name):
        """Open new brower on local mode"""
        # browser_name = self.bot_config.config['browser']
        
        if browser_name == "chrome":
            curr_caps = DesiredCapabilities.CHROME.copy()
            curr_driver = webdriver.Chrome(
                executable_path=curr_driver_path,
                desired_capabilities=curr_caps
            )
        elif browser_name == "firefox":
            self.curr_caps = DesiredCapabilities.FIREFOX.copy()
            self.curr_driver = webdriver.Firefox(
                executable_path=self.curr_driver_path,
                capabilities=self.curr_caps
            )
        elif browser_name == "iexplorer":
            self.curr_caps = DesiredCapabilities.INTERNETEXPLORER.copy()
            self.curr_driver = webdriver.Ie(
                executable_path=self.curr_driver_path,
                capabilities=self.curr_caps
            )
        elif browser_name == "edge":
            self.curr_caps = DesiredCapabilities.EDGE.copy()
            self.curr_driver = webdriver.Edge(
                executable_path=self.curr_driver_path,
                capabilities=self.curr_caps
            )
        elif browser_name == "phantomjs":
            self.curr_caps = DesiredCapabilities.PHANTOMJS.copy()
            self.curr_driver = webdriver.PhantomJS(
                executable_path=self.curr_driver_path,
                desired_capabilities=self.curr_caps
            )
        elif browser_name == "opera":
            self.curr_caps = DesiredCapabilities.OPERA.copy()
            self.curr_driver = webdriver.Opera(
                executable_path=self.curr_driver_path,
                desired_capabilities=self.curr_caps
            )
        else:
            raise Exception(
                message=("config file error, SECTION=bot, KEY=browser isn't "
                         "valid value: {}".format(browser_name)),
                log=self.log
            ) 
mode_local('edge')