from selenium.common.exceptions import WebDriverException, InvalidSessionIdException
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import requests
import time
import re


def cleanTXT(txt):

    txt = (re.sub(r'(\ )+', ' ', txt))
    try:
        if (txt[0].isspace()):   txt = txt[1:]
        if (txt[-1].isspace()): txt = txt[:-1]
    except IndexError: return re.sub(r'(\d)+\. ', '', txt)

    txt = txt.replace(u'\xa0', u' ')

    txt = txt.replace("נ ג ד","נגד")
    txt = txt.replace('פסק-דין','פסק דין')
    txt = txt.replace('\r',' ')

    txt = txt.replace('  ', ' ')
    txt = txt.replace("נ ג ד", "נגד")

    if(txt==' ' or txt=='  '): return ''

    return txt

def slicer(text,labels,contents):
    for text in text.split('\n\n'):
        text = cleanTXT(text).replace('\n ', ' ')
        if len(text) == 0: continue
        if(text[-1]==":"):
            labels.append(cleanTXT(text[:text.find(":")]))
            continue
        #
        content = []

        for info in ((text.replace(";",","))[text.find(":")+1:]).split(','):
            info = re.sub(r'(\d)+\. ','', info)
            info = info.replace('-',' ')
            content.append(cleanTXT(info))
        if len(content)!=0: contents.append(content)

    return labels,contents

def HTML_CRAWLER(link):
    xml = requests.get(link)
    soup = BeautifulSoup(xml.content, 'lxml')
    labels = []
    contents = []
    try:
        soup = soup.find('body').find("div",{"class":"WordSection1"})
        dirs = soup.findAll("div",{"align":"right"})
    except AttributeError:
        print(soup)
        print("AttErr")
        return 0
    labels = []
    contents = []
    for s in dirs:
        text = s.text

        if(len(text)==0 or text.find(":")==-1):continue

        if (text.find("בשם ה") != -1):
            labels,contents = slicer(text, labels,contents)
            continue  ################################################


        labels.append(text[:text.find(":")].replace('\n',' '))
        info = (text[text.find(":")+1:])
        content = []
        for row in info.split('\n\n'): # content
            row = cleanTXT(row).replace('\n ',' ')
            if len (row) == 0 : continue
            row = re.sub(r'(\d)+\. ', '', row)
            row = row.replace('-',' ')
            content.append(cleanTXT(row))
        if(len(content)!=0): contents.append(content)


        # NEXT SESSION
    all = {cleanTXT(labels[n]):contents[n] for n in range(len(labels))}

    return all
    # for k, v in zip(all.keys(),all.values()):
    #     print(k,": ",v)
    #


#
# link_psak_din = "https://supremedecisions.court.gov.il/Home/Download?path=HebrewVerdicts/20/520/073/e05&fileName=20073520.E05&type=2"
# link_hasuy = "https://supremedecisions.court.gov.il/Home/Download?path=HebrewVerdicts/21/650/089/e05&fileName=21089650.E05&type=2"
#
# all = HTML_CRAWLER(link_hasuy)
# for k, v in zip(all.keys(),all.values()):
#     print(k,": ",v)
#
# txt = "   ddd          ddd          rsdgs     "
# txt =(re.sub(r'(\ )+', ' ',txt))
# if(txt[0].isspace()):   txt = txt[1:]
# if(txt[-1].isspace()): txt= txt[:-1]
#
# print(txt)
