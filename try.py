from bs4 import BeautifulSoup
import requests
import urllib.request
import re
from lxml import etree


try:
    url = "https://www.google.com/"
    headers = {'User-Agent': 'Mozilla/5.0'}
    page = requests.get(url, headers=headers, timeout=1)

    soup = BeautifulSoup(page.text, "lxml")

    ######
    print("########################  AFTER REMOVE ATTRIBUTE ######")
    # Remove hidden attribute
    for hidden in soup.find_all("input", {'style':'display:none'}): 
        hidden.decompose()
    # Remove none-display attribute
    for none_display in soup.findAll("input",attrs=({"type":{"password","submit","radio","hidden", "checkbox"}})):
        none_display.decompose()

    for h in soup.find_all("input", {'hidden':'hidden'}): 
        h.decompose()
    # Regex pattern
    # Remove login attribute by regex pattern
    removePattern=re.compile("(user|login|username|password|email|name)")

    for id_login in soup.find_all("input", attrs={'class':re.compile(removePattern)}):
        id_login.decompose()

    for id_login in soup.find_all("input", attrs={'id':re.compile(removePattern)}):
        id_login.decompose()
    for name_login in soup.find_all("input", attrs={'name':re.compile(removePattern)}):
        name_login.decompose()

    # ###  Print the result after filter
    raw_data = soup.findAll("input")
    # print(raw_data)
    if not soup.find_all("input"):
        print("CHECK!!!")
    else:
        #convert tag data to string
        d=str(raw_data)
        #convert to dictionary
        u={k:v.strip('"') for k,v in re.findall(r'(\S+)=(".*?"|\S+)', d)}
        print(u)
        
except Exception as e:
    print(e)


