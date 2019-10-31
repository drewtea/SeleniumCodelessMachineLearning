from pathlib import Path
from time import sleep
import requests
import re
from bs4 import BeautifulSoup
from selenium import webdriver
from itertools import islice
import csv
import linecache
from timeit import default_timer as timer
from datetime import *
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By



# Start timer to measure execuation time for the report
start_time = timer()

# datestamp = str(datetime.now().strftime('%d_%m_%Y_%H_%M_%S'))
# timestamp = datetime.now().strftime("%d-%m-%Y_%H:%M:%S")
# Define number of urls to process
# start line and end line of url file
start_url = 0
end_url = 2
number_of_urls = end_url - start_url
test_output = ['PASS', 'FAIL', 'ERROR']


# Path to url file
URL_FILE = Path("data") / "test-sites.txt"
# Path to output file
CSV_FILE = str(start_url)+ '_' + str(end_url) + '_urldata' + '.csv'
# txt_file = str(start_url)+ '_' + str(end_url) + '_urldata' + '.txt'
OUTPUT_FILE = Path("data") / CSV_FILE
# path to chrome extention
COOKIE_EXTENTION = Path("extention")/ "cookie.crx"

# Path to report file
REPORT_FILE = Path("results") / 'report' / "report.txt"
# Path to report file
VERDICT_FILE = Path("results") / "verdict-test-sites.txt"

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
   
    """Scrape scheduled link previews."""
    session = requests.Session()
    adapter = requests.adapters.HTTPAdapter(max_retries=2)
    session.mount('https://', adapter)
    session.mount('http://', adapter)
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36"}
    page = session.get(url, headers=headers, timeout=2)
    response = page.text
    page.close()
    soup = BeautifulSoup(response, "lxml")
    # sleep(1)
    # filter element
    filter_attribute(soup)
    # Scrape raw data after filter
    raw_data = soup.findAll("input")
    if not raw_data:
        # if the webpage is rendered with JavaScript making more requests to fetch additional data.
        # this case will be using Selenium to scrape the whole source page
        # adding chrome extension
        option = webdriver.ChromeOptions()
        option.add_extension(COOKIE_EXTENTION)
        driver = webdriver.Chrome(chrome_options=option)
        driver.get(url)
        driver.implicitly_wait(10)
        # Wait for page to load full
        timeout = 10
        try:
            element_present = EC.presence_of_element_located((By.XPATH, '//input'))
            WebDriverWait(driver, timeout).until(element_present)
        except TimeoutException:
            print("Timed out waiting for page to load")
        soup = BeautifulSoup(driver.page_source, 'lxml')        
        driver.quit()
        # filter attribute
        filter_attribute(soup)
        # scrape raw data after filter
        raw_data = soup.findAll("input")
        if not raw_data:
            # if not possible to scrape the data on this website
            # => write verdict = 'ERROR' 
            verdicts(domain,test_output[2])        
                   
        # convert raw data to string format
        # data_s=str(raw_data)
        # # convert raw data to dictionary 
        # data_dict={k:v.strip('"') for k,v in re.findall(r'(\S+)=(".*?"|\S+)', data_s)}

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
            else:
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

Open data file to read the list of urls
then using the scrape module to scrape the data

'''
if __name__ == '__main__':

    with open(URL_FILE, 'r') as input_file:
        # Read line with specific number of urls
        lines_cache = islice(input_file, start_url, end_url+1)   
        # Read line by line and append 'https://'
        for current_line in lines_cache:
            domain = current_line.split()[1]
            url="https://www."+ domain
            try:
                scrape(url)
            # Add exception when connecting to url is failed
            except Exception as e:   
                verdicts(domain,test_output[2])

    # End time running
    end_time = timer()
    # Excuted time running
    excuted_time = str(timedelta(seconds=(end_time - start_time)))
    # Write runing time to report
    with open(REPORT_FILE, 'a', encoding='utf-8') as f:
        print('%s was scraped from %d websites in:'%(CSV_FILE, number_of_urls), excuted_time, file=f)
