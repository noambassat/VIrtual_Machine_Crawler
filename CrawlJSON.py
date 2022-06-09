import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains # FOR DOUBLE CLICK
import time
from lxml import html
import requests
import json

CASE = "https://supreme.court.gov.il/Pages/SearchJudgments.aspx?&OpenYearDate=2022&CaseNumber=3484&DateType=2&SearchPeriod=null&COpenDate=30/05/2022&CEndDate=31/05/2022&freeText=null&Importance=null"
driver = webdriver.Chrome(executable_path='C:/Users/Noam/Desktop/Courts Project/chromedriver.exe')
driver.get(CASE)

response = requests.get(CASE)
SOUP = BeautifulSoup(response.content, 'html.parser')
driver.find



# from requests_html import HTMLSession
#
# session = HTMLSession()
# url = 'https://supreme.court.gov.il/Pages/SearchJudgments.aspx?&OpenYearDate=null&CaseNumber=null&DateType=2&SearchPeriod=null&COpenDate=30/05/2022&CEndDate=31/05/2022&freeText=null&Importance=null'
# r = session.get(url)
#
# r.html.render(sleep=1, keep_page=True, scrolldown=1)
#
# a_S = r.html.find("הצג תיק")
# print(a_S)
# for item in a_S:
#     a = {
#         'title' : item.text,
#         'link' : item.absolute_links
#     }
#     print(a)