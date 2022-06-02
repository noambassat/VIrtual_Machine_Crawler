import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains # FOR DOUBLE CLICK
import time
from lxml import html
import requests

URLS = pd.DataFrame(columns=['URL'])
driver = webdriver.Chrome(executable_path='C:/Users/Noam/Desktop/Courts Project/chromedriver.exe')
driver.get("https://supreme.court.gov.il/Pages/SearchJudgments.aspx?&OpenYearDate=null&CaseNumber=null&DateType=2&SearchPeriod=null&COpenDate=30/05/2022&CEndDate=31/05/2022&freeText=null&Importance=null")

def get_urls(driver, start_date, end_date):
    CaseNUMBER = '3339'
    YEAR = start_date[-4:]
    URL = "https://supreme.court.gov.il/Pages/SearchJudgments.aspx?&OpenYearDate=" \
          + YEAR +\
          '&CaseNumber='\
          + CaseNUMBER +\
          "&DateType=2&SearchPeriod=null&COpenDate=30/05/2022&CEndDate=31/05/2022&freeText=null&Importance=null"

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    card = soup.find("div",{"class":"Layout-HomePage"}).find(
        "div",{"id":"MSOZoneCell_WebPartWPQ2"}).find(
        "div",{"class":"ms-webpart-chrome ms-webpart-chrome-vertical ms-webpart-chrome-fullWidth"}).find(
        "div",{"id":"ctl00_ctl40_g_664c5230_fd36_4083_9f79_25d174af43f8"}).find(
        "div",{"elad_wpid":"ctl00$ctl40$g_664c5230_fd36_4083_9f79_25d174af43f8"}).find(
        "iframe",{"id":"serviceFram"})
    src = card['src']
    response = requests.get(src)
    if response.status_code==200:
        source_src = BeautifulSoup(response.text,'html.parser')
        tree = html.fromstring(response.content)

get_urls(driver, '30/05/2022','31/05/2022')