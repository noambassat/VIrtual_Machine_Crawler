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
    for row in soup.text.splitlines():
         print(repr(row))
    # labels = []
    # contents = []
    # for dir in dirs:
    #     for t in dir.findAll("table", {"class": "MsoNormalTable"}):
    #         content = []
    #         if(t.text.find(":")==-1): continue
    #         for t in t.findAll("p",{"class":"BodyRuller"}):
    #             text = cleanTXT(t.text)
    #             if(len(text)==0): continue
    #             if(text.find(":")!=-1): # LABELS
    #                 labels.append(text[:text.find(":")])
    #                 print("333333",text[:text.find(":")])
    #                 continue
    #             if(text.find(",")!=-1):
    #                 for new_text in text.split(','):
    #                     if(len(new_text)==0):continue
    #                     content.append(new_text)
    #                     print(new_text)
    #             else:
    #                 content.append(text)
    #                 print(text)
    #         if(len(content)!=0):
    #          contents.append(content)
    # print(labels)
    # print(contents)
    # all = {labels[n]:contents[n] for n in range(len(contents))}
    # for k,v in zip(all.keys(),all.values()):
    #     print(k,": ",v)
    #


CHECKER("https://supremedecisions.court.gov.il/Home/Download?path=HebrewVerdicts/20/520/073/e05&fileName=20073520.E05&type=2")