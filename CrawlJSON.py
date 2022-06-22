import time
import numpy as np
import pandas as pd
from Printer import print_dataframe
from Save_As_Json import writeToJsonFile
from selenium import webdriver
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from collections import defaultdict

main_df = pd.read_csv(r'Decisions_Table/Decisions_Table.csv',index_col=0)
# main_df.drop('Unnamed: 0',axis= 1, inplace=True)



def crawl_HTML(data, link):
    driver = webdriver.Chrome(executable_path='C:/Users/Noam/Desktop/Courts Project/chromedriver.exe')
    driver.get(link)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    labels = []
    content = []
    dict = {}
    text = soup.findAll("span", {"lang": "HE"})
    for s in range(len(text)):
        string = text[s].text
        print(cleanTXT(string))
        print("__________________________________________")
        # if(string.find(":")!=-1):
        #     s+=1
        #     next =text[s]
        #     while(next.find(":")!=-1):
        #         dict[s] = next
        #
    driver.close()
    return data


def Get_LINK(df,CASE):
    conclusion = "החלטה \n"
    LINK = df['HTML_Link'][0]
    for i in df.index:
        if(df['סוג מסמך'][i] == 'פסק-דין'):
            conclusion = 'פסק-דן'
            LINK = df['HTML_Link'][i]
            break
    return LINK, conclusion


def cleanTXT(txt):
    txt = txt.replace('  ','')
    txt = txt.replace('\n','')
    txt = txt.replace('\t','')

    return txt

def CrawlTopWindow(CASE, n_decisions,LINK,conclusion):
    CASE_NUM = CASE[67:67+4]
    YEAR = CASE[62:66]
    src = "https://elyon2.court.gov.il/Scripts9/mgrqispi93.dll?Appname=eScourt&Prgname=GetFileDetails_for_new_site&Arguments=-N" \
          + YEAR +"-00" +CASE_NUM +"-0"
    # print(src == "https://elyon2.court.gov.il/Scripts9/mgrqispi93.dll?Appname=eScourt&Prgname=GetFileDetails_for_new_site&Arguments=-N2014-008568-0")
    driver = webdriver.Chrome(executable_path='C:/Users/Noam/Desktop/Courts Project/chromedriver.exe')
    driver.get(CASE)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    src = soup.findAll('iframe')[2]
    try:
        src =src['ng-src']
          # Top window info
    except KeyError:
        print("KeyError")
        pass

    driver.get(src)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    LABELS = []
    for a in soup.findAll("div",{"class":"item"}):
        LABELS.append(cleanTXT(a.text))

    labels = soup.findAll("span",{"class":"caseDetails-label"})
    details = soup.findAll("span",{"class":"caseDetails-info"})
    all_data = {}
    data = {}
    for i in range(len(labels)):
        data[cleanTXT(labels[i].text)] = cleanTXT(details[i].text)


    all_data[LABELS[0]] = data


    tabs = soup.findAll("div",{"class":"tab-pane fade"})
    bigger_data = {}

    for i, tab in enumerate(tabs):
        labels = []
        data = {}
        for body in tab.findAll("tbody"):
            rows = [i for i in range(len(body.findAll('tr')))]
            for j, tr in enumerate(body.findAll('tr')):
                labels = []
                infos = []
                row = {}
                for z, td in enumerate(tr.findAll("td")):

                    try:
                        label = (cleanTXT(td['data-label']))
                        info = (cleanTXT(td.text))
                        if(label=="#"):continue
                        labels.append(label)
                        infos.append(info)
                    except KeyError:
                        pass
                row = {labels[n]:infos[n] for n in range(len(labels))}
                data[j] = row
            all_data[LABELS[i + 1]] = data
    all_data['מספר החלטות'] = n_decisions
    all_data['סוג מסמך'] = conclusion
    all_data = crawl_HTML(all_data,LINK)
    driver.close()
    return all_data


def Crawl_Decisions(CASE):
    src = "https://elyon2.court.gov.il/Scripts9/mgrqispi93.dll?Appname=eScourt&Prgname=GetFileDetails_for_new_site&Arguments=-N2014-008568-0"
    CASE_NUM = CASE[67:67 + 4]
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
    LINK, conclusion = Get_LINK(df,CASE)
    driver.close()
    return df, len(df), LINK,conclusion



CASE = "https://supremedecisions.court.gov.il/Verdicts/Results/1/null/2014/8568/null/null/null/null/null"



# dec_df, n_of_Decisions,LINK,conclusion  = Crawl_Decisions(CASE)

#
# print_dataframe(dec_df,320,10)
#
# data = CrawlTopWindow(CASE, n_of_Decisions, LINK ,conclusion)
# filePath = 'C:/Users/Noam/PycharmProjects/pythonProject5/Json_Files/'
# writeToJsonFile(filePath, 'TEST!!!', data)
#

crawl_HTML([],"https://supremedecisions.court.gov.il/Home/Download?path=HebrewVerdicts/14/680/085/t07&fileName=14085680_t07.txt&type=2")



# JSON ההררכיה
# כפילויות במילון!!!!!!
# לייצר וליבא קובץ עם כל הPATH
# לעשות קרול להחלטה של כל קייס ולהכניס לקובץ הJSON
# לייצר שמות יחודיים לכל קובץ JSON
# לעטוף את הכל שירוץ ברצף
# לבדוק ריצה של 3 ימים אם עובד
# לעשות רימוט למחשב מרוחק ולעשות קרולינג להכל