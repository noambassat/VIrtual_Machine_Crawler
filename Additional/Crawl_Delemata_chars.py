from selenium.common.exceptions import WebDriverException, InvalidSessionIdException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

import http.client
import ssl
import urllib.parse
import parser
import datetime
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import requests
from requests import exceptions
import time
import re
from urllib3.exceptions import InsecureRequestWarning
from urllib3 import disable_warnings
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

url = 'https://supremedecisions.court.gov.il/Verdicts/Search/1'
exe_path = 'C:/Users/Noam/Desktop/Courts Project/chromedriver.exe'

driver = webdriver.Chrome(exe_path)
driver.get(url)

driver.find_element(By.ID,"halihtypeselect")

soup = BeautifulSoup(driver.page_source,'html.parser')


list_dict = {"תחילית": [], "הסבר": []}
info = []
initial_delemata = soup.findAll("select",{"id":"halihtypeselect"})[1]
for j, case_in in enumerate(initial_delemata):
    if(j==0):continue
    try:
        a,b = case_in.text.split("-")
        list_dict["תחילית"].append(a)
        list_dict["הסבר"].append(b)
        if(len( list_dict["תחילית"])!=len(list_dict["הסבר"])): list_dict["הסבר"].append("")

    except ValueError:
        a,b , c = case_in.text.split("-")
        b += " " + c
        list_dict["תחילית"].append(a)
        list_dict["הסבר"].append(b)
        if(len( list_dict["תחילית"])!=len(list_dict["הסבר"])): list_dict["הסבר"].append("")



df = pd.DataFrame(list_dict)
print(df.head())
df.to_csv('delemata_initials.csv',index=False ,encoding = 'utf-8-sig')
