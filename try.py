from pathlib import Path
from time import sleep
import requests
import re
from bs4 import BeautifulSoup
from itertools import islice
import csv
import linecache
from lxml import etree
import urllib3


from timeit import default_timer as timer
from datetime import *
from pprint import pprint

import pandas as pd


output_file = Path("data") / 'try.txt'

url = 'https://www.pornhub.com'
session = requests.Session()
adapter = requests.adapters.HTTPAdapter(max_retries=2)
session.mount('https://', adapter)
session.mount('http://', adapter)
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36"}
page = session.get(url, headers=headers, timeout=2)
# response = urllib3.urlopen('https://www.imgur.com')

response = page.text
# page.close()
soup = BeautifulSoup(response, "html.parser")
raw_data = soup.findAll("input")

if len(raw_data)>1:
    for r in raw_data:
        if (r.has_attr('autocomplete') or r.has_attr('autocapitalize') 
                or r.has_attr('spellcheck') or r.has_attr('aria-autocomplete')
                or r.has_attr('autofocus')):
            raw_data=r
            print(raw_data)



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
removePattern=re.compile("(user|login|username|name|password|email|mobile)")
# login = soup.findAll("input")

for id_login in soup.find_all("input", attrs={'class':re.compile(removePattern)}):
    id_login.decompose()
for id_login in soup.find_all("input", attrs={'id':re.compile(removePattern)}):
    id_login.decompose()
for name_login in soup.find_all("input", attrs={'name':re.compile(removePattern)}):
    name_login.decompose()
for name_login in soup.find_all("input", attrs={'aria-label':re.compile(removePattern)}):
    name_login.decompose()


    # ###  Print the result after filter
    # Define list of urls after preprocess
    # Print exception if the connection is failed
    # if Exception ==True:
    #     raw_data.append(e)
    # print(raw_data)
if not soup.find_all("input"):
        # raw_data.append('NO DATA')
    print('ERROR')
else:
    print(soup.find_all("input"))