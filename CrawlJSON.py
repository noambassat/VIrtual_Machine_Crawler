import time
import numpy as np
import pandas as pd
from Printer import print_dataframe
from Save_As_Json import writeToJsonFile
from selenium import webdriver
from bs4 import BeautifulSoup
import requests

main_df = pd.read_csv(r'Decisions_Table/Decisions_Table.csv',index_col=0)
# main_df.drop('Unnamed: 0',axis= 1, inplace=True)


def Get_LINK(df):
    for i in df.index:
        if(df['סוג מסמך'][i] == 'פסק-דין'): return df['HTML_Link'][i]
    return df['HTML_Link'][0]


def cleanTXT(txt):
    txt = txt.replace('  ','')
    txt = txt.replace('\n','')
    txt = txt.replace('\t','')

    return txt

def CrawlTopWindow(CASE, n_decisions,LINK):
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
    data['מספר החלטות'] = n_decisions
    data['סיכום'] = LINK


    # for d in data:
    #     print(d, ": ",data[d])

    return data


def Crawl_Decisions(CASE):

    CASE_NUM = CASE[67:67+4]

    driver = webdriver.Chrome(executable_path='C:/Users/Noam/Desktop/Courts Project/chromedriver.exe')
    driver.get(CASE)
    time.sleep(1)
    response = requests.get(CASE)
    SOUP = BeautifulSoup(driver.page_source, 'html.parser')
    time.sleep(1)
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
                if(info.find('פסק')!=-1 and info.find('דין')!=-1): indo = "פסק דין"
                temp[label] = info
            if (len(temp) == 0): continue
            for link in hrefs:
                temp['HTML_Link'] ='https://supremedecisions.court.gov.il/'+link['href']
            case_dec[i] = temp

        except AttributeError : continue

    for row in (case_dec.values()):
        df = df.append(row, ignore_index=True)
    df.drop_duplicates(inplace=True)
    if(df['Case Number'][0] not in main_df['Case Number']):
        main_df.append(df)
        main_df.to_csv('Decisions_Table/Decisions_Table.csv')
    LINK = Get_LINK(df)
    print("!!!!!!!!!!!!!!!!!!!  ", LINK)

    return df, len(df), LINK



CASE = "https://supremedecisions.court.gov.il/Verdicts/Results/1/null/2014/8568/null/null/null/null/null"



dec_df, n_of_Decisions,LINK  = Crawl_Decisions(CASE)


print_dataframe(dec_df,320,10)

CrawlTopWindow(CASE, n_of_Decisions, LINK)

# לייצר וליבא קובץ עם כל הPATH
# לעשות קרול להחלטה של כל קייס ולהכניס לקובץ הJSON
# לייצר שמות יחודיים לכל קובץ JSON
# לעטוף את הכל שירוץ ברצף
# לבדוק ריצה של 3 ימים אם עובד
# לעשות רימוט למחשב מרוחק ולעשות קרולינג להכל