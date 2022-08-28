from selenium.common.exceptions import WebDriverException, InvalidSessionIdException
from selenium.webdriver.chrome.options import Options
from Parser import HTML_CRAWLER
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import requests
import time
import re

dec_path = r'Decisions_Table/Decisions_Table.csv'
filePath = '/home/ubuntu/pythonProject5/Json_Files/'
DT_path = '/home/ubuntu/pythonProject5/DataFrames/'
exe_path = '/home/ubuntu/pythonProject5/chromedriver'


main_df = pd.read_csv(dec_path,index_col=0)
options = Options()
options.add_argument('--disable-gpu')
options.add_argument('--headless')

PROXY = "5.79.66.2:13080"

options.add_argument('--proxy-server=%s' % PROXY)

def cleanTXT(txt):


    ####################################function
    # for i,c in enumerate(txt.split()):
    #     while c==' ':
    #         c = txt[i+1:]
    txt = txt.replace(u'\xa0', u' ')

    txt = txt.replace("נ ג ד","נגד")
    txt = txt.replace('פסק-דין','פסק דין')
    txt = re.sub('\s+', ' ', txt)
    txt = (re.sub(r'(\ )+', ' ', txt))
    try:
        if (txt[0].isspace()):   txt = txt[1:]
        if (txt[-1].isspace()): txt = txt[:-1]
    except IndexError: pass

    txt = re.sub('<.*>', ' ', txt)

    txt = txt.replace("נ ג ד", "נגד")
    if(txt==' ' or txt=='  '): return ''

    return txt

def crawl_HTML(data, link, Type):
    xml = requests.get((link))
    soup = BeautifulSoup(xml.content, 'lxml')

    data_dict = HTML_CRAWLER(link)
    if(data_dict==0): data_dict = {}
    data_dict['סוג מסמך'] = Type
    data_dict['מסמך מלא'] = cleanTXT(soup.text.replace('\n\n',' ').replace(u'\xa0', u' '))
    data_dict['קישור למסמך'] = link

    conclusion = ""
    for row in soup.findAll("p",{"class":"Ruller4"}): conclusion += cleanTXT(row.text)
    data_dict["סיכום מסמך"] = cleanTXT(conclusion)

    return data_dict

def Get_LINK(df,CASE): # רק פסק-דין או החלטה אחרונה כרגע
    if(len(df)==0): return '',''
    Type = cleanTXT(df['סוג מסמך'][0])
    LINK = df['קישור למסמך הטמל'][0]
    for i in df.index:
        if(df['סוג מסמך'][i].find('דין')!=-1 and df['סוג מסמך'][i].find('פסק')!=-1 ):
            Type = 'פסק דין'
            LINK = df['קישור למסמך הטמל'][i]
            break
    return LINK, Type



def add_counters(data):
    temp_data = data.copy()
    for key in data.keys():
        if (key == "פרטים כלליים" or key == 'תיק חסוי'): continue # doesn't count this keys
        curr_key = 'מספר ' + str(key) + ' בתיק'
        if(data[key]=='אין מידע'): temp_data[curr_key] = 0
        else:
            temp_data[curr_key] = len(temp_data[key])
    return temp_data

def CrawlTopWindow(CASE,LINK,Type, dict,case_name_num):
    hidden_content = 0
    CASE_NUM = CASE[67:67+4]
    YEAR = CASE[62:66]

    try:
        driver = webdriver.Chrome(executable_path=exe_path, chrome_options=options)
        driver.get(CASE)

    except WebDriverException:
        driver = webdriver.Chrome(executable_path=exe_path, chrome_options=options)
        driver.get(CASE)

    time.sleep(1)
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    try:
        soup = soup.find("div", {"class": "details-view"})
        iframe = soup.find('iframe')
        src = iframe['ng-src']
    except KeyError:
        print("KeyError")
        src = "https://elyon2.court.gov.il/Scripts9/mgrqispi93.dll?Appname=eScourt&Prgname=GetFileDetails_for_new_site&Arguments=-N" \
              + YEAR + "-00" + CASE_NUM + "-0"
    except IndexError:
        print("IndexError")
        src = "https://elyon2.court.gov.il/Scripts9/mgrqispi93.dll?Appname=eScourt&Prgname=GetFileDetails_for_new_site&Arguments=-N" \
              + YEAR + "-00" + CASE_NUM + "-0"
        pass
    except AttributeError:
        print("AttributeError")
        src = "https://elyon2.court.gov.il/Scripts9/mgrqispi93.dll?Appname=eScourt&Prgname=GetFileDetails_for_new_site&Arguments=-N" \
              + YEAR + "-00" + CASE_NUM + "-0"
    try:
        driver.get(src)
    except WebDriverException:
        src = "https://elyon2.court.gov.il/Scripts9/mgrqispi93.dll?Appname=eScourt&Prgname=GetFileDetails_for_new_site&Arguments=-N" \
              + YEAR + "-00" + CASE_NUM + "-0"
    try:
        driver.get(src)
    except InvalidSessionIdException:
        driver.close()
        print("InvalidSessionIdException:\n", src)
        return 0
    except  WebDriverException:
        driver.close()
        print("InvalidSessionIdException:\n", src)
        return 0

    soup = BeautifulSoup(driver.page_source, 'html.parser')

    if ((soup.find("head").title.text).find("חסוי")!=-1):
        all_data = {}
        hidden_content = 1

    if not hidden_content:
        LABELS = []
        for a in soup.findAll("div",{"class":"item"}):
            LABELS.append(cleanTXT(a.text))

        labels = soup.findAll("span",{"class":"caseDetails-label"})
        details = soup.findAll("span",{"class":"caseDetails-info"})
        all_data = {}
        first_data = {}

        for i in range(len(labels)):
            first_data[cleanTXT(labels[i].text)] = cleanTXT(details[i].text)

        all_data[LABELS[0]] = first_data

        tabs = soup.findAll("div",{"class":"tab-pane fade"})
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
                            if(label=="#"): label = "מספר"
                            if(label.find("שם ב.משפט")!=-1): label = "שם בית משפט"
                            if (label.find("מ.תיק דלמטה") != -1): label = "מספר תיק דלמטה"
                            if (label.find("ת.החלטה") != -1): label = "תאריך החלטה"

                            info = (cleanTXT(td.text)).replace('\n',' ')
                            if(len(info)<1): info = "אין מידע"
                            labels.append(label)
                            infos.append(info)
                        except KeyError:
                            pass
                    if(len(infos)<1): continue
                    row = {cleanTXT(labels[n]):cleanTXT(infos[n]) for n in range(len(labels))}
                    if "סוג צד" in labels:

                        new_val = ""
                        for n,l in enumerate(labels):
                            if(l=='סוג צד'): new_val += infos[n]
                            if(l=='מספר'): new_val += " "+ infos[n]
                        row['צד'] = new_val
                    if row not in data: data.append(row)
                if(len(data)<1):
                    all_data[LABELS[i + 1]] = 'אין מידע'
                    continue
                else: all_data[LABELS[i + 1]] = data
        all_data['תיק חסוי'] = False
        ### ADDING COUNTERS

    else:
        all_data['תיק חסוי'] = True

    all_data = add_counters(all_data)
    try:
        all_data['מספר תיק מלא'] = case_name_num
        all_data['מספר תיק'] = case_name_num[case_name_num.find(" ")+1:]
        all_data['ראשי תיבות תיק'] = case_name_num[:case_name_num.find(" ")]
        all_data['שנת תיק'] = '20'+case_name_num[case_name_num.find("/")+1:]
    except KeyError:
        pass



    doc= [crawl_HTML(all_data, LINK, Type)] # רשימת מסמכי הHTML , כרגע רק 1
    counter = 0
    other_docs = []
    for row in dict.values():
        row.pop("מספר תיק")
        if row not in doc: ####################
            counter+=1
            other_docs.append(row)

    all_data['מספר החלטות בתיק'] = len(other_docs)
    all_data['קישור לתיק'] = CASE
    new_dict = {"פרטי תיק":all_data,"מסמכים":{"פסק דין או החלטה אחרונה":doc, "כל ההחלטות בתיק":other_docs}}
    driver.close()
    return new_dict

def Crawl_Decisions(CASE):
    CASE_NUM = CASE[67:67 + 4] + "/"+ CASE[64:64 + 2]
    try:
        driver = webdriver.Chrome(executable_path=exe_path, chrome_options=options)
        driver.get(CASE)
    except WebDriverException:
        driver = webdriver.Chrome(executable_path=exe_path, chrome_options=options)

        driver.get(CASE)
    time.sleep(1)
    response = requests.get(CASE)
    SOUP = BeautifulSoup(driver.page_source, 'html.parser')
    time.sleep(1)
    case_dec = {}
    df = pd.DataFrame()
    try:
        hidden_case = SOUP.findAll('td')

        SOUP = SOUP.find("div",{"class":"processing-docs"}).findAll('tr')

        for i,s in enumerate(SOUP):

            temp = {}

            hrefs = s.findAll("a",{'title':'פתיחה כ-HTML'})
            for case in (s.findAll("td",{"ng-binding"})):
                label = cleanTXT(case['data-label'])
                if(label.find('#')!=-1): continue
                if(label.find('מ.')!=-1 or label.find("מס'")!=-1): label = 'מספר עמודים'
                temp['מספר תיק'] = CASE_NUM
                info = cleanTXT(case.text)
                if(info.find('פסק')!=-1 and info.find('דין')!=-1): info = "פסק דין"
                temp[label] = info
            if (len(temp) == 0): continue
            for link in hrefs:
                temp['קישור למסמך הטמל'] ='https://supremedecisions.court.gov.il/'+link['href']
            if(temp not in case_dec.values()): case_dec[i] = temp

    except AttributeError : pass

    for row in (case_dec.values()):
        df = df.append(row, ignore_index=True)
    df.drop_duplicates(inplace=True)
    main_df = pd.read_csv(r'Decisions_Table/Decisions_Table.csv',index_col=0)
    main_df = main_df.append(df)
    main_df=main_df.reindex()
    main_df.to_csv('Decisions_Table/Decisions_Table.csv')
    LINK, Type = Get_LINK(df,CASE)
    driver.close()
    return df, LINK,Type, case_dec
