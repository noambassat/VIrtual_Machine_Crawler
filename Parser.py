from selenium.common.exceptions import WebDriverException, InvalidSessionIdException
from selenium.webdriver.chrome.options import Options
from CrawlJSON import cleanTXT
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import requests
import time
import re


def CHECKER(link):
    xml = requests.get(link)
    soup = BeautifulSoup(xml.content, 'lxml')
    labels = []
    contents = []
    soup = soup.find('body').find("div",{"class":"WordSection1"})
    dirs = soup.findAll("div",{"dir":"rtl"})
    for dir in dirs:
        # print(dir)
        for t in dir.findAll("table", {"class": "MsoNormalTable"}):
            for i in t.findAll("p",{"class":"BodyRuller"}):
                if(i.text.find(",")!=-1):
                    for j in i.text.split(','):
                        print(j)
                        print("@@@@@@@@@@")
                else:
                    print(i.text)
                    print("_______________________")
            # if(row.find(":")!=-1): print(row)



CHECKER("https://supremedecisions.court.gov.il/Home/Download?path=HebrewVerdicts/20/520/073/e05&fileName=20073520.E05&type=2")
