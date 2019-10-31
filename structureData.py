from pathlib import Path
from itertools import islice, dropwhile
import csv
import os
import re
import pandas as pd
import numpy as np

# start_url = 0
# end_url = 1001

# Path to raw data
RAW_FILE = Path("data") / "0_4_urldata.csv"
# Path to dataframe file after cleaning
DF_FILE = Path("data") / "label_data_5000.csv"

# A key list to store the attribute name (key)
# element_key = ['url','name','placeholder','class','id','aria-label', 'type','title','tabindex','role','accesskey'] 
element_key = ['url','name','placeholder','class','id','aria-label']

def label_data(dict):
  # Function to label data with type of data is dictionary 
  if dict['name']:
    dict.update({'target':'name'})
  elif dict['placeholder']:
    dict.update({'target':'placeholder'})
  elif dict['class']:
    dict.update({'target':'class'})
  elif dict['id']:
    dict.update({'target':'id'})
  elif dict['aria-label']:
    dict.update({'target':'aria-label'})
  
# A dictionary to store the input search element for each website
d2={}
# A list to store the clean data
clean_data = []    

with open(RAW_FILE, 'r', encoding='utf-8') as rf, open(DF_FILE, 'a', encoding='utf-8', newline='') as dfFile:
    reader = csv.reader(rf, delimiter=',')

    # open file, read raw data from each row then process data:
    for row in reader:
      # convert raw data to dictionary
        element_dict={k:v.strip('"') for k,v in re.findall(r'(\S+)=(".*?"|\S+)', row[1])}
        # add only interested attributes
        d2 = {k: element_dict.get(k) for k in element_key } 
        # append url domain
        d2.update({'url':row[0]})
        # label dict data
        label_data(d2)
        # append data to list      
        clean_data.append(d2)

    # convert to dataframe
    df = pd.DataFrame(clean_data)
    # add 'None' for key with missing value
    df.replace('N/A',np.NaN)
    print(df)

    # write clean data to file  
    # df.to_csv(dfFile, index=False, na_rep='NA')




