
import http.client
import urllib.parse
import time
from bs4 import BeautifulSoup
YEAR = str(2012)
add_case = "480"
src ="https://elyon2.court.gov.il/Scripts9/mgrqispi93.dll?Appname=eScourt&Prgname=GetFileDetails_for_new_site&Arguments=-N" \
          + YEAR + add_case + "-0"
src = "https://supremedecisions.court.gov.il/Home/Download?path=HebrewVerdicts/12/800/004/e01&fileName=12004800_e01.txt&type=2"
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
print(soup)
#
# # tag to be replaced
# old_tag = soup.charset
#
#
#
# # input string
# old_tag.string = "utf8"
#
# '''replacing tag
# #page_element.replace_with("string") removes a tag or string from the tree,
# #and replaces it with the tag or string of your choice.'''
# soup.i.replace_with(old_tag)
#
# print(soup)
