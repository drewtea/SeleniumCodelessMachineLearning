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
end_url = 10
number_of_urls = end_url - start_url
test_output = ['PASS', 'FAIL', 'ERROR']


# Path to url file
url_file = Path("data") / "test-sites.txt"
# Path to output file
csv_file = str(start_url)+ '_' + str(end_url) + '_urldata' + '.csv'
# txt_file = str(start_url)+ '_' + str(end_url) + '_urldata' + '.txt'
output_file = Path("data") / csv_file

# Path to report file
report_file = Path("reports") / "report.txt"
# Path to report file
result_file = Path("results") / "verdict1.txt"

def verdicts(domain,test_output):
    # Write the verdict after testing to file
    verdict = []      
    verdict.append(test_output)
    websites=[]
    websites.append(domain)
    with open(result_file, 'a', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        for i in zip(websites, verdict):
            writer.writerow(i)

def filter_attribute(soup):
    # Funtion to filter the element
    # Regex pattern for style
    removeStyle = re.compile(r"display|color|colour|none", re.IGNORECASE)
    for input_style in soup.findAll("input", {'style':removeStyle}): 
        input_style.decompose()
    # Remove none-display attribute
    removeType = re.compile(r"password|submit|radio|hidden|checkbox|range|number|file|phone|button", re.IGNORECASE)
    for input_type in soup.findAll("input",attrs=({"type":removeType})):
        input_type.decompose()

    for input_hidden in soup.find_all("input", {'hidden':'hidden'}): 
        input_hidden.decompose()
    # Regex pattern for login filter
    removePattern=re.compile(r"(user|login|username|name|password|e-mail|phone|mobilephone|email|mobile|birthday|age|hidden|submit|genre|gender|vip)",re.IGNORECASE)
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
    if not soup.find_all("input"):
        # if the webpage is rendered with JavaScript making more requests to fetch additional data.
        # this case will be using Selenium to scrape the whole source page
        driver = webdriver.Chrome()
        driver.get(url)
        # driver.implicitly_wait(10)
        # Wait for page to load full
        timeout = 5
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
            # if not possible to scrape the data
            # write verdict = 'ERROR' 
            verdicts(domain,test_output[2])        
    else:
        raw_data      
         
        
        # convert raw data to string format
        # data_s=str(raw_data)
        # # convert raw data to dictionary 
        # data_dict={k:v.strip('"') for k,v in re.findall(r'(\S+)=(".*?"|\S+)', data_s)}

    # If list has more than one element
    # filter again
    if len(raw_data)>1:
        for r in raw_data:
            if (r.has_attr('autocomplete') or r.has_attr('autocapitalize') 
                    or r.has_attr('spellcheck') or r.has_attr('aria-autocomplete')
                    or r.has_attr('autofocus') or r.has_attr('placeholder') ):
                raw_data=r
                a=[]
                a.append(r)
                raw_data=a
    # list to store url sites
    websites=[]
    websites.append(domain)

    # Write direct to text format
    # with open(output_file, 'a', encoding='utf-8') as f:
    #     print(websites, raw_data, file=f)

    # Write to cvs format
    with open(output_file, 'a', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        for i in zip(websites, raw_data):
         writer.writerow(i)
   
''' 

Open data file to read the list of urls
then using the scrape module to scrape the data

'''
with open(url_file, 'r') as input_file:
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
with open(report_file, 'a', encoding='utf-8') as f:
    print('%s was scraped from %d websites in:'%(csv_file, number_of_urls), excuted_time, file=f)
