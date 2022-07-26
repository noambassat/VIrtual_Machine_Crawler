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

# !/usr/bin/env python3 # -*- coding: utf-8 -*-
disable_warnings(InsecureRequestWarning)


global API_KEY,filePath,DT_path, exe_path
API_KEY = "2APAwmdKRCzXbasu1TrBhlvbMoMqk5nI"
# Paths
filePath = '/home/ubuntu/PycharmProjects/VIrtual_Machine_Crawler/Json_Files/'
DT_path = '/home/ubuntu/PycharmProjects/VIrtual_Machine_Crawler/DataFrames/'
exe_path = '/home/ubuntu/PycharmProjects/pythonProject5/chromedriver'



options = Options()
# options.add_argument('--disable-gpu')
# options.add_argument('--headless')

PROXY = "5.79.66.2:13081"

options.add_argument('--proxy-server=%s' % PROXY)


def get_url(year, case_num): return  "https://supremedecisions.court.gov.il/Verdicts/Results/1/null/"+ str(year) +"/" + str(case_num) +"/1/8/null/null/null"

def cleanTXT(text):

    try:
        txt = text.encode('cp1252').decode('cp1255', errors='replace')
    except UnicodeEncodeError:
        txt = text
    txt = txt.replace(u'\xa0', u' ')

    txt = txt.replace("נ ג ד", "נגד")
    txt = txt.replace('פסק-דין', 'פסק דין')
    txt = re.sub('\s+', ' ', txt)
    txt = (re.sub(r'(\ )+', ' ', txt))
    try:
        if (txt[0].isspace()):   txt = txt[1:]
        if (txt[-1].isspace()): txt = txt[:-1]
    except IndexError:
        pass

    txt = re.sub('<.*>', ' ', txt)

    txt = txt.replace("נ ג ד", "נגד")
    txt = txt.replace("\'", "'")

    if (txt == ' ' or txt == '  '): return ''

    return txt

def Get_Text(link):
    conn = http.client.HTTPSConnection("api.webscrapingapi.com")
    src = "/v1?url=" + (urllib.parse.quote(link,
                                           safe="")) + "&api_key="+API_KEY+"&device=desktop&proxy_type=datacenter&render_js=1&wait_until=domcontentloaded&timeout=30000"

    conn.request("GET", src)

    res = conn.getresponse()
    print(res)
    data = res.read()

    html_content = (data.decode("utf-8"))
    SOUP = BeautifulSoup(html_content, 'html.parser')
    print(SOUP.find("body").text)
    return(SOUP)

def Get_LINK(df):  # רק פסק-דין או החלטה אחרונה כרגע
    if (len(df) == 0): return '', ''
    Type = cleanTXT(df['סוג מסמך'][0])
    LINK = df['קישור למסמך הטמל'][0]
    for i in df.index:
        if (df['סוג מסמך'][i].find('דין') != -1 and df['סוג מסמך'][i].find('פסק') != -1):
            Type = 'פסק דין'
            LINK = df['קישור למסמך הטמל'][i]
            break
    return LINK, Type


def crawl_HTML(year, data, link, Type):
    # sess1 = requests.Session()
    # proxies = {"http": "http://5.79.66.2:13081", "https": "https://5.79.66.2:13081"}

    try:

        conn = http.client.HTTPSConnection("api.webscrapingapi.com")
        src = "/v1?url=" + (urllib.parse.quote(link,
                                               safe="")) + "&api_key="+API_KEY+"&device=desktop&proxy_type=datacenter&render_js=1&wait_until=domcontentloaded&timeout=30000"

        conn.request("GET", src)
        res = conn.getresponse()
        data = res.read()

        html_content = (data.decode("utf-8"))
    except exceptions.Timeout:
        print("TIME OUT ERROR")
    except OSError:
        print("OSError from crawl_html func")
    SOUP = BeautifulSoup(html_content, 'html.parser')
    data_dict = parser.HTML_CRAWLER(year, link)
    if (data_dict == 0): data_dict = {}
    data_dict['סוג מסמך'] = Type
    data_dict['מסמך מלא'] = cleanTXT(SOUP.text.replace('\n\n', ' ').replace(u'\xa0', u' '))
    data_dict['קישור למסמך'] = link
    conclusion = ""
    for row in SOUP.findAll("p", {"class": "Ruller4"}): conclusion += cleanTXT(row.text)
    data_dict["סיכום מסמך"] = cleanTXT(conclusion)
    return data_dict


def add_counters(data):
    temp_data = data.copy()
    for key in data.keys():
        if (key == "פרמטים כלליים" or key == 'תיק חסוי'): continue  # doesn't count this keys
        curr_key = 'מספר ' + str(key) + ' בתיק'
        if (data[key] == 'אין מידע'):
            temp_data[curr_key] = 0
        else:
            temp_data[curr_key] = len(temp_data[key])
    return temp_data


def CrawlTopWindow(CASE, LINK, Type, dict,case_name_num):

    hidden_content = 0
    for i in range(7):
        if (CASE[67 +i]=="/"): break

    CASE_NUM = CASE[67:67 + i]
    YEAR = CASE[62:66]
    add_case =  CASE_NUM
    while(len(add_case)!=6): add_case = "0" + add_case
    add_case = "-" + add_case

    src = "https://elyon2.court.gov.il/Scripts9/mgrqispi93.dll?Appname=eScourt&Prgname=GetFileDetails_for_new_site&Arguments=-N" \
          + YEAR + add_case + "-0"

    try:

        conn = http.client.HTTPSConnection("api.webscrapingapi.com")
        src = "/v1?url=" + (urllib.parse.quote(src, safe="")) + "&api_key="+API_KEY+"&device=desktop&proxy_type=datacenter&render_js=1&wait_until=domcontentloaded&timeout=30000"

        conn.request("GET", src)

        res = conn.getresponse()
        data = res.read()

        html_content = (data.decode("utf-8"))

    except OSError as err:
        print(err)
        print("OS ERROR IN CRAWL TOP WINDOW!")
        print(err)
        return 0

    if(len(html_content)<1): print("the len is lower than !!!!!", html_content)

    soup = BeautifulSoup(html_content, 'html.parser')
    try:
        if ((soup.find("head").title.text).find("חסוי") != -1):
            all_data = {}
            hidden_content = 1
    except AttributeError:
        pass

    if not hidden_content:
        LABELS = []
        for a in soup.findAll("div", {"class": "item"}):
            LABELS.append(cleanTXT(a.text))

        labels = soup.findAll("span", {"class": "caseDetails-label"})
        details = soup.findAll("span", {"class": "caseDetails-info"})
        all_data = {}
        first_data = {}
        for i in range(len(labels)):
            first_data[cleanTXT(labels[i].text)] = cleanTXT(details[i].text)

            if(i==0):case_name_num = cleanTXT(details[i].text)

        try:
            all_data[LABELS[0]] = first_data
        except IndexError:
            pass
        tabs = soup.findAll("div", {"class": "tab-pane fade"})
        bigger_data = {}
        for i, tab in enumerate(tabs):
            labels = []
            data = []
            for body in tab.findAll("tbody"):
                rows = [i for i in range(len(body.findAll('tr')))]
                for j, tr in enumerate(body.findAll('tr')):
                    labels = []
                    infos = []
                    row = {}
                    for z, td in enumerate(tr.findAll("td")):

                        try:
                            label = (cleanTXT(td['data-label']))
                            if (label == "#"): label = "מספר"
                            if (label.find("שם ב.משפט") != -1): label = "שם בית משפט"
                            if (label.find("מ.תיק דלמטה") != -1): label = "מספר תיק דלמטה"
                            if (label.find("ת.החלטה") != -1): label = "תאריך החלטה"

                            info = (cleanTXT(td.text)).replace('\n', ' ')
                            if (len(info) < 1): info = "אין מידע"
                            labels.append(label)
                            infos.append(cleanTXT(info))
                        except KeyError:
                            pass
                    if (len(infos) < 1): continue
                    row = {cleanTXT(labels[n]): cleanTXT(infos[n]) for n in range(len(labels))}
                    if "סוג צד" in labels:

                        new_val = ""
                        for n, l in enumerate(labels):
                            if (l == 'סוג צד'): new_val += infos[n]
                            if (l == 'מספר'): new_val += " " + infos[n]
                        row['צד'] = new_val
                    if row not in data: data.append(row)
                if (len(data) < 1):
                    all_data[LABELS[i + 1]] = 'אין מידע'
                    continue
                else:
                    all_data[LABELS[i + 1]] = data
        all_data['תיק חסוי'] = False
        ### ADDING COUNTERS
    else:
        all_data['תיק חסוי'] = True
    all_data = add_counters(all_data)
    try:
        all_data['מספר תיק מלא'] = case_name_num
        all_data['מספר תיק'] = case_name_num[case_name_num.find(" ") + 1:]
        all_data['ראשי תיבות תיק'] = case_name_num[:case_name_num.find(" ")]
        all_data['שנת תיק'] = '20' + case_name_num[case_name_num.find("/") + 1:]
        all_data['תאריך יצוא התיק'] = str(datetime.datetime.now().date())

    except KeyError:
        print("KEY ERROR ...")
    except AttributeError:
        all_data['מספר תיק מלא'] = ""
        all_data['מספר תיק'] = ""
        all_data['ראשי תיבות תיק'] = ""
        all_data['שנת תיק'] = ""
        all_data['תא"ריך יצוא התיק'] = str(datetime.datetime.now().date())
    print("crawling top window ...")
    doc = [crawl_HTML(YEAR,all_data, LINK, Type)]  # רשימת מסמכי הHTML , כרגע רק 1
    counter = 0
    other_docs = []
    for row in dict.values():
        row.pop("מספר תיק")
        if row not in doc:  ####################
            counter += 1
            other_docs.append(row)
    all_data['מספר החלטות בתיק'] = len(other_docs)
    all_data['קישור לתיק'] = CASE
    new_dict = {"פרטי תיק": all_data, "מסמכים": {"פסק דין או החלטה אחרונה": doc, "כל ההחלטות בתיק": other_docs}}
    return new_dict

def Crawl_Decisions(driver, CASE):

    CASE_NUM = CASE[67:67 + 4] + "/" + CASE[64:64 + 2]
    try:
        # driver = webdriver.Chrome(exe_path, options=options)
        driver.get(CASE)
    except InvalidSessionIdException:
        print("Couldn't get src:\n", CASE)
        driver.close()
        driver = webdriver.Chrome(exe_path, options=options)
    except WebDriverException as wde:
        print(str(wde),"\n","--------",wde.args ,"\n", CASE, "\n","trying once again.....")
        driver.close()
        driver = webdriver.Chrome(exe_path, options=options)
        try:
            driver.get(CASE)
        except WebDriverException as wde:
            print(str(wde),"\n","--------",wde.args ,"\n", CASE)
    try:
        myElem = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'row_0')))

    except TimeoutException:
        print("Loading took too much time! crawl dec")

    SOUP = BeautifulSoup(driver.page_source, 'html.parser')
    # At least 2 secs must be waiting in order to load the webpage

    case_dec = {}
    df = pd.DataFrame()
    try:
        hidden_case = SOUP.findAll('td')

        SOUP = SOUP.find("div", {"class": "processing-docs"}).findAll('tr')
        ###

        for i, s in enumerate(SOUP):

            temp = {}

            hrefs = s.findAll("a", {'title': 'פתיחה כ-HTML'})
            for case in (s.findAll("td", {"ng-binding"})):
                label = cleanTXT(case['data-label'])
                if (label.find('#') != -1): continue
                if (label.find('מ.') != -1 or label.find("מס'") != -1): label = 'מספר עמודים'
                temp['מספר תיק'] = CASE_NUM
                info = cleanTXT(case.text)
                if (info.find('פסק') != -1 and info.find('דין') != -1): info = "פסק דין"
                temp[label] = info

            if (len(temp) == 0): continue
            for link in hrefs:
                temp['קישור למסמך הטמל'] = 'https://supremedecisions.court.gov.il/' + link['href']
            if (temp not in case_dec.values()): case_dec[i] = temp

    except AttributeError:
        print("AttributeError")
        pass

    for row in (case_dec.values()):
        df = df.append(row, ignore_index=True)
    df.drop_duplicates(inplace=True)
    try:
        main_df = pd.read_csv('/home/ubuntu/PycharmProjects/VIrtual_Machine_Crawler/Decisions_Table/Decisions_Table.csv', index_col=0, dtype='unicode', low_memory=False, error_bad_lines=False)
        main_df = main_df.append(df)
        main_df = main_df.reindex()
    except pd.errors.EmptyDataError as err:
        main_df = df.copy()
    except UnicodeDecodeError:
        main_df = df.copy()
    except IndexError:
        main_df = df.copy()

    main_df.to_csv('Decisions_Table/Decisions_Table.csv')

    LINK, Type = Get_LINK(df)
    return df, LINK, Type, case_dec