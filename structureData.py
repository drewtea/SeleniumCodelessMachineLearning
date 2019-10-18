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
raw_file = Path("data") / "1_100_urldata.csv"
# Path to dataframe file after cleaning
df_file = Path("data") / "df.csv"

# A key list to store the attribute name (key)
element_key = ['url','name','placeholder','class','id','aria-label','title','tabindex','role','accesskey']   
# A dictionary to store the element for each website
d2={}
# A list to store the clean data
clean_data = []    

with open(raw_file, 'r', encoding='utf-8') as rf, open(df_file, 'a', encoding='utf-8', newline='') as dfFile:
    reader = csv.reader(rf, delimiter=',')

    # open file, read raw data from each row then process data:
    for row in reader:
      # convert raw data to dictionary
        element_dict={k:v.strip('"') for k,v in re.findall(r'(\S+)=(".*?"|\S+)', row[1])}
        # add 'None' for key with missing value
        d2 = {k: element_dict.get(k,np.NaN) for k in element_key } 
        d2.update({'url':row[0]})
        clean_data.append(d2)
    # convert to dataframe
    df = pd.DataFrame(clean_data)
    # print(df)
    # df.replace('N/A',np.NaN)

    # write clean data to file  
    df.to_csv(dfFile, index=False, na_rep='NA')

        
