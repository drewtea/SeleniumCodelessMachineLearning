import os
from pathlib import Path
import re
from bs4 import BeautifulSoup
import requests
import csv
import linecache
import time
from datetime import datetime
from datetime import timedelta
from timeit import default_timer as timer
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.options import Options as Options_FF
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException, ElementNotVisibleException
from selenium.common.exceptions import InvalidElementStateException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from itertools import islice



''' Chose the browser for testing '''
    # 'chrome':     Chrome version: 78.0.3904.70 (Official Build) (64-bit)
    # 'firefox':    Firefox verion: 70.0 (64-bit)
    # 'opera':      Opera version: 76.0.3809.132
    # 'ie':         Internet Explorer version: 11.418.18362
    # 'edge':       Microsoft Edge version: 44.18362.387.0 build 18362
    # 'phantom':    PhantomJS version:
    # 'mult_brs':   Multiple browsers ( testing against cross browsers)
WEB_BROWSER = 'chrome'

''' Chose the option for browser '''
    # 'none': not using option
    # 'addon': using addon, default = None
    # 'headless': using headless browser, default = None
BROWSER_OPTION = 'none'

# Search keyword for testing search functionality
SEARCH_TERM = "selenium"
# Define number of urls to process
# start line and end line of url file
START_URL = 0
END_URL = 2
number_of_urls = END_URL - START_URL
test_output = ['PASS', 'FAIL', 'ERROR']

datestamp = str(datetime.now().strftime('%d_%m_%Y_%H_%M_%S'))
timestamp = datetime.now().strftime("%d-%m-%Y_%H:%M:%S")
# Path to url file
URL_FILE = Path("data") / "test-sites.txt"
# Path to output file
CSV_FILE = str(START_URL)+ '_' + str(END_URL) + '_urldata' + '.csv'
# txt_file = str(START_URL)+ '_' + str(END_URL) + '_urldata' + '.txt'
OUTPUT_FILE = Path("data") / CSV_FILE
# path to chrome extention
COOKIE_CHROME = Path("extention") / "cookie_chrome.crx"
UBLOCK_CHROME = Path("extention") / "uBlock_chrome.crx"
# path to firefox extention
COOKIE_FF = Path("extention") / "cookie_ff.xpi"
UBLOCK_FF = Path("extention") / "uBlock_ff.xpi"
# Path to report file
REPORT_FILE = Path("results") / 'reports'/ "report.txt"
# Path to report file
VERDICT_FILE = Path("results") / "verdict_test-sites.txt"

# Start timer to measure execuation time for the report
start_time = timer()

def browser(browser_name):
    # Setup browser using Selenium
    # Chrome
    if browser_name == 'chrome':      
        if BROWSER_OPTION == 'addon':
            options = Options()
            options.add_extension(COOKIE_CHROME)
            options.add_extension(UBLOCK_CHROME)
            driver = webdriver.Chrome(options=options)
        if BROWSER_OPTION == 'headless':
            options = Options()
            options.add_argument('headless')
            driver = webdriver.Chrome(options=options)
        if BROWSER_OPTION == 'none':
            driver = webdriver.Chrome()
    # Firefox
    if browser_name == 'firefox':
        if BROWSER_OPTION == 'addon':
            profile = webdriver.FirefoxProfile()
            profile.add_extension(r"D:\CCN\Intership_TSP\CodelessML\extention\cookie_ff.xpi")
            profile.add_extension(r"D:\CCN\Intership_TSP\CodelessML\extention\uBlock_ff.xpi")
            driver = webdriver.Firefox(profile)
        # headless browser
        if BROWSER_OPTION == 'headless':
            options = Options_FF()
            options.headless = True
            driver = webdriver.Firefox(options=options)
        else:
            driver = webdriver.Firefox()
    # Opera
    if browser_name == 'opera':
        options = webdriver.ChromeOptions()
        options.binary_location = r"C:\Users\Phuc\AppData\Local\Programs\Opera\64.0.3417.92\opera.exe"
        driver = webdriver.Opera(options=options)
    # Edge
    if browser_name == 'edge':     
        driver = webdriver.Edge()

    # Internet Explorer
    if browser_name == 'ie':
        driver = webdriver.Ie()

	# multiple browsers ( testing against cross browsers)
    if browser_name == 'mult_brs':
        desired_cap = []
        desired_cap.append ({'browserName':'chrome', 'javascriptEnabled':'true', 'version':'', 'platform':'ANY'})
        desired_cap.append ({'browserName':'firefox', 'javascriptEnabled':'true', 'version':'', 'platform':'ANY'})
        browser_list = ['chrome', 'firefox', 'opera', 'edge', 'ie']        
        for browser in desired_cap:
            driver = webdriver.Remote(
            command_executor='http://192.168.1.18:30756',
            desired_capabilities=browser)
    
    return driver
    
    # For cleanup, quit the driver
    # driver.quit()

def verdicts(domain,test_output):
    # Write the verdict after testing to file
    verdict = []      
    verdict.append(test_output)
    websites=[]
    websites.append(domain)
    with open(VERDICT_FILE, 'a', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        for i in zip(websites, verdict):
            writer.writerow(i)

def filter_attribute(soup):
    # Funtion to filter the element
    # Regex pattern for style
    removeStyle = re.compile(r"display", re.IGNORECASE)
    for input_style in soup.findAll("input", {'style':removeStyle}): 
        input_style.decompose()
    # filter type attribute
    removeType = re.compile(r"password|submit|radio|hidden|checkbox|range|number|file|phone|button|image", re.IGNORECASE)
    for input_type in soup.findAll("input",attrs=({"type":removeType})):
        input_type.decompose()

    for input_hidden in soup.find_all("input", {'hidden':'hidden'}): 
        input_hidden.decompose()

    # remove readonly attribute
    for readonly in soup.find_all("input"):
        if readonly.has_attr('readonly'):
            readonly.decompose()
    # Regex pattern for login filter
    removePattern=re.compile(r"(user|login|username|name|password|e-mail|phone|mobilephone|email|mobile|birthday|age|hidden|submit|genre|gender|vip|location|captcha|postal)",re.IGNORECASE)
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
    for placeholder_login in soup.find_all("input", attrs={'autocomplete':removePattern}):
        placeholder_login.decompose()

''' 
Module to scrape the search element of website
=== Scrape search field content of html DOM  ===
'''
def scrape(url):   
    """
    Scrape webpage by providing url.
    If the webpage is rendered with JavaScript making more requests to fetch additional data,
    this case will be using Selenium to scrape the whole source page
    
    """
    driver=browser(WEB_BROWSER)
    driver.get(url)
    driver.implicitly_wait(10)
    soup = BeautifulSoup(driver.page_source, 'lxml')        
    driver.quit()
    # scrape element with direct type='search'
    type_search = soup.findAll("input", {"type":"search"})
    # filter attribute
    filter_attribute(soup)
    # scrape raw data after filter
    raw_data = soup.findAll("input")
    if not raw_data:  
        """Scrape website by request module"""
        session = requests.Session()
        adapter = requests.adapters.HTTPAdapter(max_retries=2)
        session.mount('https://', adapter)
        session.mount('http://', adapter)
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36"}
        page = session.get(url, headers=headers, timeout=2)
        response = page.text
        page.close()
        soup = BeautifulSoup(response, "lxml")
        type_search = soup.findAll("input", {"type":"search"})       
        # sleep(1)
        # filter element
        filter_attribute(soup)
        # Scrape raw data after filter
        raw_data = soup.findAll("input")
        print('SCRAPED BY REQUEST MODULE')
        print(raw_data)
    # If list has more than one element
    # filter again
    attributes = ['autocomplete', 'autocapitalize', 'aria-autocomplete', 
                   'spellcheck','autofocus']
    if len(raw_data)>1:
        for r in raw_data:      
            check_attr = {k: r.has_attr(k) for k in attributes}
            if True in check_attr.values():
                a=[]
                a.append(r)
                raw_data=a                     
    # if not possible to scrape the data on website
    if not raw_data:  
        # collect the input element whose attribute type='search'
        raw_data = type_search
        if not raw_data:
        # write verdict = 'ERROR' 
            verdicts(domain,test_output[2])  

    # list to store url sites
    websites=[]
    websites.append(domain)

    # Write direct to text format
    # with open(OUTPUT_FILE, 'a', encoding='utf-8') as f:
    #     print(websites, raw_data, file=f)

    # Write to cvs format
    with open(OUTPUT_FILE, 'a', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        for i in zip(websites, raw_data):
         writer.writerow(i)

'''
    Funtion to find locator
'''
def locator_element(raw_data):
    element_key = ['name','placeholder','class','id','aria-label','title','role','accesskey','type'] 
    for key in element_key:
        if key in raw_data:
            try:
                stringxPath="//input[@" + key + "='" + raw_data[key] + "']" 
                print (stringxPath)                
                locator = driver.find_element_by_xpath((stringxPath))
                locator.clear()
                locator.send_keys(SEARCH_TERM)
                locator.send_keys(Keys.RETURN)
                break                                     
            except (NoSuchElementException, ElementNotVisibleException, ElementNotInteractableException, InvalidElementStateException):
                pass          
      
''' 
Open data file to read the list of urls
then using the scrape module to scrape the data
'''
if __name__ == '__main__':
    
    '''
        Scrape website content
    '''
    # with open(URL_FILE, 'r') as input_file:
    #     # Read line with specific number of urls
    #     lines_cache = islice(input_file, START_URL, END_URL)   
    #     # Read line by line and append 'https://'
    #     for current_line in lines_cache:
    #         domain = current_line.split()[1]
    #         url="https://"+ domain
    #         try:
    #             scrape(url)
    #         # Add exception when connecting to url is failed
    #         except Exception as e:   
    #             verdicts(domain,test_output[2])
    end_scrape_time = timer()

    '''
        Test search functionality of website
    '''
    start_test_time = timer()
    with open(OUTPUT_FILE, 'r', encoding='utf-8') as out_file:
        reader = csv.reader(out_file, delimiter=',')
        for row in reader:            
            url="https://www."+ row[0]
            # convert raw data to dictionary
            raw_data={k:v.strip('"') for k,v in re.findall(r'(\S+)=(".*?"|\S+)', row[1])}
            driver=browser(WEB_BROWSER)
            # driver.implicitly_wait(10)
            driver.get(url)
            driver.implicitly_wait(5)
            initial_url = driver.current_url
            print("TESTING SITE: ",row[0])
            locator_element(raw_data)
            driver.implicitly_wait(10)        
            handles = driver.window_handles
            if len(handles)>1:
                driver.switch_to_window(handles[1])
                initial_url = driver.current_url
            time.sleep(1)
            try:                
                WebDriverWait(driver, 10).until(EC.url_changes(initial_url))                
            except TimeoutException as e:
                print("Title exception: ",driver.title)    
            title= driver.current_url
            if SEARCH_TERM in title:
                # Pass case
                verdicts(row[0],test_output[0])            
            else:
                # Fail case
                verdicts(row[0],test_output[1])
            print("PAGE TITLE: ", title)
            print("======================================")
            # driver.close()
    end_test_time = timer()

    '''
        Logs and reports
    '''
    #   End time running
    end_time = timer()
    # Excuted time running
    scrape_time = str(timedelta(seconds=(end_scrape_time - start_time)))
    test_time = str(timedelta(seconds=(end_test_time - start_test_time)))
    excuted_time = str(timedelta(seconds=(end_time - start_time)))    
    # Write runing time to report
    with open(VERDICT_FILE, 'a', encoding='utf-8') as f:
        print('Test executing date: %s ' %(timestamp), file=f)
        print('Browser: %s' %(WEB_BROWSER), file=f)
        print('Browser option:', BROWSER_OPTION, file=f)
        print('Number of websites: %d'%(number_of_urls), file=f)
        print('Scraped time:', scrape_time, file=f)
        print('Testing time:', test_time, file=f)
        print('Total finish time:', excuted_time, file=f)
        print('======================================================', file=f)

 