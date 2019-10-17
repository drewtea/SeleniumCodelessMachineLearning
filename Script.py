from pathlib import Path
from time import sleep
import requests
import re
from bs4 import BeautifulSoup
from itertools import islice
import csv
import linecache
from timeit import default_timer as timer
from datetime import *

# Start timer to measure execuation time for the report
start_time = timer()

# datestamp = str(datetime.now().strftime('%d_%m_%Y_%H_%M_%S'))
# timestamp = datetime.now().strftime("%d-%m-%Y_%H:%M:%S")
# Define number of urls to process, 
# start line and end line of url file
start_url = 1
end_url = 10
number_of_urls = end_url - start_url


# Path to url file
url_file = Path("data") / "https-sites.txt"
# Path to output file
csv_file = str(start_url)+ '_' + str(end_url) + '_urldata' + '.txt'
# csv_file = str(start_url)+ '_' + str(end_url) + '_urldata' + '.txt'
output_file = Path("data") / csv_file

# Path to report file
report_file = Path("reports") / "report.txt"


# data =[]
# review=[]

# ==== Scrape search field content  =====
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
    for hidden in soup.findAll("input", {'style':'display:none'}): 
        hidden.decompose()
    # Remove none-display attribute
    for none_display in soup.findAll("input",attrs=({"type":{"password","submit","radio","hidden", "checkbox"}})):
        none_display.decompose()

    for h in soup.find_all("input", {'hidden':'hidden'}): 
        h.decompose()
    # Regex pattern
    # Remove login attribute by regex pattern
    removePattern=re.compile("(user|login|username|name|password|email)")
    # login = soup.findAll("input")

    for id_login in soup.find_all("input", attrs={'class':re.compile(removePattern)}):
        id_login.decompose()
    for id_login in soup.find_all("input", attrs={'id':re.compile(removePattern)}):
        id_login.decompose()
    for name_login in soup.find_all("input", attrs={'name':re.compile(removePattern)}):
        name_login.decompose()


    # ###  Print the result after filter
    # Define list of urls after preprocess
    raw_data = soup.findAll("input")
    # Print exception if the connection is failed
    # if Exception ==True:
    #     raw_data.append(e)
    # print(raw_data)
    if not soup.find_all("input"):
        raw_data.append('NO DATA')
    else:
        d=str(raw_data)
        u={k:v.strip('"') for k,v in re.findall(r'(\S+)=(".*?"|\S+)', d)}
    websites=[]
    websites.append(url)
    print(u)

    
        #convert to dictionary
        

    # Write direct to text format
    with open(output_file, 'a', encoding='utf-8') as f:
        print(websites, u, file=f)

    # Write to cvs format
    # with open(output_file, 'a', encoding='utf-8', newline='') as f:
    #     writer = csv.writer(f)
    #     for i in zip(websites, u):
    #         writer.writerow(i)
   
''' 

Open data file to read the list of urls
then use scrape module to retrieve the data

'''
with open(url_file, 'r') as input_file:
#     # Skip first line
#     next(input_file)
    # Read line with specific number of urls
    lines_cache = islice(input_file, start_url, end_url)   
# lines_cache = linecache.getlines('test-sites.txt')[start_url:end_url]
    # Read line by line and append 'https://'
    for current_line in lines_cache:
        url="https://"+ current_line.split()[1]
        try:
            s = scrape(url)
        except Exception as e:   
            websites=[]   
            error = []      
            websites.append(url)
            error.append('ERROR')
            with open(output_file, 'a', encoding='utf-8', newline='') as f:
                writer = csv.writer(f)
                for i in zip(websites, error):
                    writer.writerow(i)
# Print to report
end_time = timer()
# excuted_time = end_time - start_time
excuted_time = str(timedelta(seconds=(end_time - start_time)))
with open(report_file, 'a', encoding='utf-8') as f:
    print('%s was scraped from %d websites in:'%(csv_file, number_of_urls), excuted_time, file=f)