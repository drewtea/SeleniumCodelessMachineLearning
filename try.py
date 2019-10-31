from pathlib import Path
from time import sleep
import requests
import re
from bs4 import BeautifulSoup
from itertools import islice
import csv
import linecache
from lxml import etree
from millionsSites import filter_attribute


from timeit import default_timer as timer
from datetime import *
from pprint import pprint

import pandas as pd


url = 'https://www.dailymotion.com'
session = requests.Session()
adapter = requests.adapters.HTTPAdapter(max_retries=2)
session.mount('https://', adapter)
session.mount('http://', adapter)
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36"}
page = session.get(url, headers=headers, timeout=2)

response = page.text
# page.close()
soup = BeautifulSoup(response, "html.parser")
type_search = soup.findAll("input", {"type":"search"})
filter_attribute(soup)
raw_data = soup.findAll("input")
attributes = ['autocomplete', 'autocapitalize', 'aria-autocomplete', 
              'spellcheck','autofocus']
print('len of list:', len(raw_data))
# for k in raw_data:
#     print(k)

if len(raw_data)>1:
    for r in raw_data:      
        check_attr = {k: r.has_attr(k) for k in attributes}
        if True in check_attr.values():
            a=[]
            a.append(r)
            raw_data=a     
       
if not raw_data:
    # collect the input element whose attribute type='search'
    raw_data = type_search
    if not raw_data:
    # if not possible to scrape the data
    # write verdict = 'ERROR' 
        print('Error')
else:
    print(raw_data)

