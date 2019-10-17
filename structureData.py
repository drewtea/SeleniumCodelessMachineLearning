from pathlib import Path
import requests
import re
from itertools import islice, dropwhile
import csv
import os
from scrapely import Scraper

# start_url = 0
# end_url = 1001

# Path to raw data
raw_file = Path("data") / "2001_3001_urldata.csv"
# Skip lines
skip=['NO DATA!!', 'ERROR!!!']
clean_file = Path("data") / "clean1_file.csv"
df_file = Path("data") / "df.csv"

# an empty list to store the raw data
element = []   
url =[]
s = Scraper()
# website = []      
with open(raw_file, 'r', encoding='utf-8') as rf, open(clean_file, 'a', encoding='utf-8', newline='') as wf:
    reader = csv.reader(rf, delimiter=',')
    # writer = csv.writer(wf)

    # for row in islice(reader,start_url,end_url):
    for row in reader:
      if not any(line in row for line in skip):
        print(row[0])
        # url.append(row[0])
        # writer.writerow(row)
      # # print(row[0],row[1])
        element.append(row[1])
      # convert raw data to string
        element_s=str(element)
      # convert raw data to dictionary
        element_dict={k:v.strip('"') for k,v in re.findall(r'(\S+)=(".*?"|\S+)', element_s)}
        # print(element_dict, file=wf)
        # s.train(row[0],element_dict)
        
        
