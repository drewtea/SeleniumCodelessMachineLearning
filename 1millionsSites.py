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

# Start timer to measure execuation time for the report
start_time = timer()

# datestamp = str(datetime.now().strftime('%d_%m_%Y_%H_%M_%S'))
# timestamp = datetime.now().strftime("%d-%m-%Y_%H:%M:%S")
# Define number of urls to process
# start line and end line of url file
start_url = 0
end_url = 4
number_of_urls = end_url - start_url
test_output = ['PASS', 'FAIL', 'ERROR']


# Path to url file
url_file = Path("data") / "test_sites.txt"
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

def filter_elemment(soup):
    # Funtion to filter the element
    # Exclude login form, email form...
    for hidden in soup.findAll("input", {'style':'display:none'}): 
        hidden.decompose()
    # Remove none-display attribute
    for none_display in soup.findAll("input",attrs=({"type":{"password","submit","radio","hidden", "checkbox","range","number"}})):
        none_display.decompose()

    for h in soup.find_all("input", {'hidden':'hidden'}): 
        h.decompose()
    # Regex pattern
    # Remove login attribute by regex pattern
    removePattern=re.compile(r"(user|login|username|name|password|email|mobile|hidden|submit|genre)")
    # login = soup.findAll("input")

    for id_login in soup.find_all("input", attrs={'class':re.compile(removePattern)}):
        id_login.decompose()
    for id_login in soup.find_all("input", attrs={'id':re.compile(removePattern)}):
        id_login.decompose()
    for name_login in soup.find_all("input", attrs={'name':re.compile(removePattern)}):
        name_login.decompose()
    for name_login in soup.find_all("input", attrs={'aria-label':re.compile(removePattern)}):
        name_login.decompose()

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
    filter_elemment(soup)
    # Scrape raw data after filter
    raw_data = soup.findAll("input")
    if not soup.find_all("input"):
        # if the webpage is rendered with JavaScript making more requests to fetch additional data.
        # this case will be using Selenium to scrape the whole source page
        driver = webdriver.Chrome()
        driver.get(url)
        soup = BeautifulSoup(driver.page_source, 'lxml')
        driver.quit()
        # filter element 
        filter_elemment(soup)
        # scrape raw data after filter
        raw_data = soup.findAll("input")
        if not raw_data:
            # if can not scrape the data
            # write verdict = 'ERROR' 
            verdicts(domain,test_output[2])
    else:
        raw_data
        # convert raw data to string format
        # data_s=str(raw_data)
        # # convert raw data to dictionary 
        # data_dict={k:v.strip('"') for k,v in re.findall(r'(\S+)=(".*?"|\S+)', data_s)}

    # List to store url link
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
        url="https://"+ domain
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
