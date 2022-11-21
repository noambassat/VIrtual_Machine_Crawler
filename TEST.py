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
link = "https://supremedecisions.court.gov.il/Home/Download?path=HebrewVerdicts/07/010/000/N02&fileName=07000010.N02&type=2"
conn = http.client.HTTPSConnection("api.webscrapingapi.com")

src = "/v1?url=" + (urllib.parse.quote(link, safe="")) + "&api_key="+API_KEY+"&device=desktop&proxy_type=datacenter&render_js=1&wait_until=domcontentloaded&timeout=30000"

conn.request("GET", src)
res = conn.getresponse()
data = res.read()
html_content = (data.decode("utf-8"))

print(html.unescape(html_content))

# ile(TEST_PATH,'test',)
#
# f = open(fileName)

# # returns JSON object as
# # a dictionary
# data = json.load(f)
#
# # Closing file
# f.close()

# l1="מסמכים"
# l2="פסק דין או החלטה אחרונה"
# l3="כל קוד הטמל"
#
# # txt = data[l1][l2][0][l3]
# txt1 = html.unescape(txt)
# txt2=html.unescape(txt1)
#
# #print(txt2)
#
# f = open("/Users/jonathan.schler/Downloads/sample.html", "wt")
# n = f.write(txt2)
# f.close()