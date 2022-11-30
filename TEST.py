import json
import html
import http.client
import urllib.parse
import time
from bs4 import BeautifulSoup
import Save_As_Json

import requests
import json
import html
# Opening JSON file
API_KEY = "2APAwmdKRCzXbasu1TrBhlvbMoMqk5nI"

TEST_PATH = 'C:/Users/Noam/Desktop/Courts Project/VIrtual_Machine_Crawler/Test/'
link = "https://supremedecisions.court.gov.il/Home/Download?path=HebrewVerdicts/00/010/000/i06&fileName=00000010.I06&type=2"
conn = http.client.HTTPSConnection("api.webscrapingapi.com")

src = "/v1?url=" + (urllib.parse.quote(link, safe="")) + "&api_key="+API_KEY+"&device=desktop&proxy_type=datacenter&render_js=1&wait_until=domcontentloaded&timeout=30000"

conn.request("GET", src)
res = conn.getresponse()
data = res.read()
html_content = (data.decode("utf-8"))

html_content = (html.unescape(html_content))
soup = BeautifulSoup(html_content, 'html.parser')
dirs = soup.findAll("div", {"align": "right"})
dirs_1 = soup.findAll('p', {"class": "Ruller3"})

if (len(dirs) < 1):
    dirs = soup.findAll("p", {"class": "3"})
    print("old file, dirs = p class 3")
    if (len(dirs) > 1):
        print("worked!")
    else:
        print("failed")