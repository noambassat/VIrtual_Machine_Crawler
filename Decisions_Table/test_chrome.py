import requests
from bs4 import BeautifulSoup

# Proxies:
sess = requests.Session()
sess1 = requests.Session()
sess2 = requests.Session()

proxies = {"http": "http://37.48.118.4:13081"}
proxies = {"http": "http://5.79.66.2:13081","https": "https://5.79.66.2:13081"}


url_to_get_via_https = "https://supremedecisions.court.gov.il/Verdicts/Results/1/null/1994/6563/null/null/null/null/null"
#url_to_get_via_https = "https://api.ipify.org?format=json"

# <body class="search-page" dir="auto" id="out    proxies = {"http": "http://5.79.66.2:13081", "https": "https://5.79.66.2:13081"}
#     time.sleep(1)
#     print("CRAWL HTML\n",link)
#     try:
#         html_content = sess.get(link, proxies=proxies).text
#     except OSError:
#         sess1 = requests.Session()
#         html_content = sess1.get(link, proxies=proxies, verify = False).texter" lang="he">

html_content = sess.get(url_to_get_via_https, proxies=proxies).text
SOUP = BeautifulSoup(html_content, 'html.parser')
print(SOUP.find("div",{"class":"modal-body"}))