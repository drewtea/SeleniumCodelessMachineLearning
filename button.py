from bs4 import BeautifulSoup
import requests
import urllib.request
import re
from lxml import etree

url = "https://www.nationalgeographic.com/"
headers = {'User-Agent': 'Mozilla/5.0'}
page = requests.get(url, headers=headers, timeout=1)

soup = BeautifulSoup(page.text, "lxml")
# for b in soup.select('button:is(.search)'):
#     print(b)
# def must_contain_all(*strings):                                                 
#     def must_contain(markup):                                                   
#         return markup is not None and all(s in markup for s in strings)         
#     return must_contain
# def criterion(tag):
#     if tag.name == "button" and tag.attrs(must_contain_all('search')):
#         return tag
# #   return tag.name('button') and re.search('search', tag.text)

# for r in soup.findAll(criterion):
#     print(r)
span = soup.find_all('span')
for s in span:
    print(s)
s=str(span)
d=dict(re.findall(r'(\S+)=(".*?"|\S+)', s))
print(d)
u={k:v.strip('"') for k,v in re.findall(r'(\S+)=(".*?"|\S+)', s)}
print(u)


