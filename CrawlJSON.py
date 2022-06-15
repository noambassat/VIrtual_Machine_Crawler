import time

import pandas as pd

from Save_As_Json import writeToJsonFile
from selenium import webdriver
from bs4 import BeautifulSoup
import requests

def cleanTXT(txt):
    txt = txt.replace('  ','')
    txt = txt.replace('\n','')
    txt = txt.replace('\t','')

    return txt

def CrawlTopWindow(CASE):
    driver = webdriver.Chrome(executable_path='C:/Users/Noam/Desktop/Courts Project/chromedriver.exe')
    driver.get(CASE)
    response = requests.get(CASE)
    SOUP = BeautifulSoup(driver.page_source, 'html.parser')
    src = SOUP.findAll('iframe')[1]
    try:
        src =src['ng-src']
        driver.get(src)  # Top window info
    except KeyError: pass
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    labels = soup.findAll("span",{"class":"caseDetails-label"})
    details = soup.findAll("span",{"class":"caseDetails-info"})

    # xpath = '/html/body/div[1]/div[1]/div/div/div[2]/a'


    for t in soup.findAll('td'):
        # labels.append(t['data-label'])
        # details.append(t.text)
        try:
            labels.append(t['data-label'].replace('\t',''))
            details.append(t.text.replace('\t',''))
        except KeyError: pass

    data = {}
    for i in range(len(labels)):
        try:
            labels[i] = labels[i].text
            details[i] = details[i].text

        except AttributeError: pass
        labels[i] = cleanTXT(labels[i])
        details[i] = cleanTXT(details[i])
        data[labels[i]] = details[i]

    for d in data:
        print(d, ": ",data[d])

    return data


def Crawl_Decisions():####################
    ###################
    CASE = "https://supremedecisions.court.gov.il/Verdicts/Results/1/null/2014/8568/null/null/null/null/null"
    CASE_NUM = CASE[67:67+4]
    #############3
    driver = webdriver.Chrome(executable_path='C:/Users/Noam/Desktop/Courts Project/chromedriver.exe')
    driver.get(CASE)
    time.sleep(1)
    response = requests.get(CASE)
    SOUP = BeautifulSoup(driver.page_source, 'html.parser')
    SOUP = SOUP.find("div",{"class":"processing-docs"}).findAll('tr')
    case_dec = {}
    df = pd.DataFrame()

    for i,s in enumerate(SOUP):
        try:
            temp = {}
            hrefs = s.findAll("a",{'title':'פתיחה כ-HTML'})

            for case in (s.findAll("td",{"ng-binding"})):

                label = cleanTXT(case['data-label'])
                if(label.find('#')!=-1): continue
                if(label.find('מ.')!=-1 or label.find("מס'")!=-1): label = 'מספר עמודים'
                temp['Case Number'] = CASE_NUM
                info = cleanTXT( case.text)
                temp[label] = info
            if (len(temp) == 0): continue
            for link in hrefs:
                temp['HTML_Link'] ='https://supremedecisions.court.gov.il/'+link['href']

            case_dec[i] = temp

        except AttributeError : pass

    for row in (case_dec.values()):
        df = df.append(row, ignore_index=True)

    print(df)
Crawl_Decisions()
