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
def get_dict(dirs):

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
    all = {}
    for n in range(len(labels)):
        all[labels[n]] =contents[n]
        if(labels[n].find('פני')!=-1): all["מספר השופטים"] = len(contents[n])

    return all

def slicer(text,labels,contents):
    for text in text.split('\n\n'):
        text = cleanTXT(text).replace('\n ', ' ')
        if len(text) == 0: continue
        if(text.find(":")!=-1):
            labels.append(cleanTXT(text[:text.find(":")]))
            # continue
        #
        content = []



        # if(((text.replace(";",","))[text.find(":")+1:]).find(",")==-1):
        #     content.append(cleanTXT(text[text.find(":")+1:]))
        #     print(content)
        # else:
        for info in ((text.replace(";",","))[text.find(":")+1:]).split(','):
            info = re.sub(r'(\d)+\. ','', info)
            info = cleanTXT(info.replace('-',' '))
            content.append(cleanTXT(info))
        contents.append(content)

    return labels,contents



def HTML_CRAWLER(link):
    xml = requests.get(link)
    soup = BeautifulSoup(xml.content, 'lxml')

    try:
        soup = soup.find('body').find("div",{"class":"WordSection1"})
        dirs = soup.findAll("div", {"align": "right"})
        dirs_1 = soup.findAll('p', {"class": "Ruller3"})

    except AttributeError:
        try:
            soup = BeautifulSoup(xml.content, 'lxml')
            soup = soup.find('body').find("div", {"class": "Section1"})
            dirs = soup.findAll("div", {"align": "right"})
            dirs_1 = soup.findAll('p', {"class": "Ruller3"})
        except AttributeError:
            print(link)

    one = get_dict(dirs)
    return {**get_dict(dirs_1), **one}
    # for k, v in zip(all.keys(),all.values()):
    #     print(k,": ",v)


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
