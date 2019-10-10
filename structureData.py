from pathlib import Path
import requests
import re
from itertools import islice
import csv

start_url = 0
end_url = 4

data_file = Path("data") / "1_1001_urldata.csv"
skip=('NO DATA!!|ERROR!!!')


noise_amp=[]         #an empty list to store the second column
with open(data_file, 'r', encoding='utf-8') as rf:
    reader = csv.reader(rf, delimiter=',')
    for row in reader:
      noise_amp.append(row[1])
      d=str(noise_amp)
      u={k:v.strip('"') for k,v in re.findall(r'(\S+)=(".*?"|\S+)', d)}
      print(u)