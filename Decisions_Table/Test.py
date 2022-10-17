from bs4 import  BeautifulSoup
import http.client
import urllib.parse

# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
#
# # CHROMEDRIVER_PATH  = '/home/ubuntu/PycharmProjects/pythonProject5/chromedriver'
# link = "https://supremedecisions.court.gov.il/Verdicts/Results/1/null/null/null/2/null/01-01-2010/02-01-2010/null"
# # URL = "https://api.webscrapingapi.com/v1/?api_key=4AcAfWEcuu9LzMeCiM4brs5XaBhGrKFT&device=desktop&proxy_type=datacenter&render_js=1&wait_until=domcontentloaded&timeout=30000&url=" + (urllib.parse.quote(src, safe=""))
# #
# #
# # options = Options()
# #
# # driver = webdriver.Chrome(CHROMEDRIVER_PATH, options=options)
# #
# # driver.get(URL)
# #
# # file = open('seleniumpage.txt', mode='w', encoding='utf-8')
# # file.write(driver.page_source)
# conn = http.client.HTTPSConnection("api.webscrapingapi.com")
# src = "/v1?url=" + (urllib.parse.quote(link,
#                                        safe="")) + "&api_key=4AcAfWEcuu9LzMeCiM4brs5XaBhGrKFT&device=desktop&proxy_type=datacenter&render_js=1&wait_until=domcontentloaded&timeout=30000"
# conn.request("GET", src)
# res = conn.getresponse()
# data = res.read()
# html_content = (data.decode("utf-8"))
# soup = BeautifulSoup(html_content, 'html.parser')
#
#
# print(soup)\
