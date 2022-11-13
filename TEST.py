import json
import html
import http.client
import urllib.parse
import time
from bs4 import BeautifulSoup
import Save_As_Json
YEAR = str(2012)
filePath ='Temp_json/'
add_case = "480"
src = "https://supremedecisions.court.gov.il/Verdicts/Search/1"
print(src)
API_KEY = "2APAwmdKRCzXbasu1TrBhlvbMoMqk5nI"
conn = http.client.HTTPSConnection("api.webscrapingapi.com")
print(1)
src = "/v1?url=" + (urllib.parse.quote(src,
                                       safe="")) + "&api_key=" + API_KEY + "&device=desktop&proxy_type=datacenter&render_js=1&wait_until=domcontentloaded&timeout=30000"
print(2)
import ssl

conn.request("GET", src)
print(3)

res = conn.getresponse()
print(4)
time.sleep(1)
data = res.read()

html_content = (data.decode("utf-8"))
soup = BeautifulSoup(html_content, 'html.parser')
soup = str(soup).replace("windows-1255","utf8")
soup = BeautifulSoup(soup, features="html.parser")
soups = soup.findAll("div")
for i, so in enumerate(soups):
    print(so)
# S = soup.find("div",{"class":"ng-scope"})
# print(S)
# s = S.find("div",{"class":"searchBlock block-6"})
# print(s)
# Opening JSON file

# Save_As_Json.writeToJsonFile(filePath,'Temp_Json', {soup})
#
# f = open('Temp_Json.json')
#
# # returns JSON object as
# # a dictionary
# data = json.load(f)
#
# # Closing file
# f.close()
#
# l1="מסמכים"
# l2="פסק דין או החלטה אחרונה"
# l3="כל קוד הטמל"
#
# txt = data[l1][l2][0][l3]
# txt1 = html.unescape(txt)
# txt2=html.unescape(txt1)
#
# #print(txt2)
#
# f = open(filePath+'Temp_Json.json', "wt")
# n = f.write(txt2)
# f.close()