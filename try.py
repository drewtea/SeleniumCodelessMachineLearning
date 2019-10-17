from bs4 import BeautifulSoup
import requests
import urllib.request
import re
from lxml import etree
from scrapely import Scraper


from scrapely import Scraper
s= Scraper()
url1='https://nzz.ch'
data={'autocomplete': 'off', 'class': 'searchbox__input', 'name': 'form[q]', 'placeholder': 'Suchen Sie Artikel oder Themen', 'type': 'text'}
s.train(url1,data)
url2='https://finra.org'
s.scrape(url2)
