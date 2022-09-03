from selenium.common.exceptions import WebDriverException, InvalidSessionIdException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import datetime
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import requests
import time
import re

dec_path = r'Decisions_Table/Decisions_Table.csv'
filePath = '/home/ubuntu/PycharmProjects/pythonProject5/Json_Files/'
DT_path = '/home/ubuntu/PycharmProjects/pythonProject5/DataFrames/'
exe_path = '/home/ubuntu/PycharmProjects/pythonProject5/chromedriver'

CASE =  "https://supremedecisions.court.gov.il/Verdicts/Results/1/null/2010/9684/null/null/null/null/null"
LINK =  "https://supremedecisions.court.gov.il/Home/Download?path=HebrewVerdicts/10/840/096/s01&fileName=10096840_s01.txt&type=2"
dict = {1: {'מספר תיק': '9684/10', 'תאריך': '02/01/2010', 'סוג מסמך': 'החלטה', 'מספר עמודים': '1', 'קישור למסמך הטמל': 'https://supremedecisions.court.gov.il/Home/Download?path=HebrewVerdicts/10/840/096/s01&fileName=10096840_s01.txt&type=2'}}
case_name_num =  'בש"פ 9684/10'


def crawl_HTML(data, link, Type):
    sess = requests.Session()
    proxies = {"http": "http://5.79.66.2:13081", "https": "https://5.79.66.2:13081"}
    html_content = sess.get(link, proxies=proxies).text
    time.sleep(3)
    SOUP = BeautifulSoup(html_content, 'html.parser')
    data_dict = HTML_CRAWLER(link)
    if (data_dict == 0): data_dict = {}
    data_dict['סוג מסמך'] = Type
    data_dict['מסמך מלא'] = cleanTXT(SOUP.text.replace('\n\n', ' ').replace(u'\xa0', u' '))
    data_dict['קישור למסמך'] = link
    conclusion = ""
    for row in SOUP.findAll("p", {"class": "Ruller4"}): conclusion += cleanTXT(row.text)
    data_dict["סיכום מסמך"] = cleanTXT(conclusion)

    print(data_dict)
    return data_dict

def cleanTXT(txt):
    ####################################function
    # for i,c in enumerate(txt.split()):
    #     while c==' ':
    #         c = txt[i+1:]
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
    if (txt == ' ' or txt == '  '): return ''

    return txt
def slicer(text,labels,contents):
    for text in text.split('\n\n'):
        content = []
        text = cleanTXT(text).replace('\n ', ' ')
        if len(text) == 0: continue
        if(text.find(":")!=-1):
            labels.append(cleanTXT(text[:text.find(":")]))
            continue
            # continue
        for info in ((text.replace(";",","))[text.find(":")+1:]).split(','):
            info = re.sub(r'(\d)+\. ','', info)
            info = cleanTXT(info.replace('-',' '))
            if(len(info)!=0): content.append(cleanTXT(info))
        if(len(content)!=0): contents.append(content)
        else: contents.append("אין מידע")
    return labels,contents



def get_dict(dirs):

    labels = []
    contents = []
    for s in dirs:
        text = s.text
        if(len(text)==0 or text.find(":")==-1):continue

        if (text.find("בשם ה") != -1 and text.find("להצטרף")==-1):
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
            if(len(row)!=0): content.append(cleanTXT(row))
        if(len(content)!=0): contents.append(content)
        else: contents.append("אין מידע")


        # NEXT SESSION
    all = {}
    for n in range(len(labels)):
        try:
            all[labels[n]] =contents[n]
            if(labels[n].find('פני')!=-1): all["מספר השופטים"] = len(contents[n])
        except IndexError:
            pass

    return all
def HTML_CRAWLER(link):
    sess = requests.Session()
    proxies = {"http": "http://5.79.66.2:13081", "https": "https://5.79.66.2:13081"}
    html_content = sess.get(link, proxies=proxies).text
    soup = BeautifulSoup(html_content, 'html.parser')

    try:
        soup = soup.find('body').find("div",{"class":"WordSection1"})
        dirs = soup.findAll("div", {"align": "right"})
        dirs_1 = soup.findAll('p', {"class": "Ruller3"})

    except AttributeError:
        try:
            soup = BeautifulSoup(html_content, 'html.parser')
            soup = soup.find('body').find("div", {"class": "Section1"})
            dirs = soup.findAll("div", {"align": "right"})
            dirs_1 = soup.findAll('p', {"class": "Ruller3"})
        except AttributeError:
            print(link)

    one = get_dict(dirs)
    return {**get_dict(dirs_1), **one}
hidden_content = 0
CASE_NUM = CASE[67:67 + 4]
YEAR = CASE[62:66]

sess = requests.Session()
proxies = {"http": "http://5.79.66.2:13081", "https": "https://5.79.66.2:13081"}
html_content = sess.get(LINK, proxies=proxies).text
soup = BeautifulSoup(html_content, 'html.parser')
# print(soup)
# print("################")
# print("CASE = ", CASE)
# print("LINK = ", LINK)

print(" num = ", case_name_num)
# soup = BeautifulSoup(driver.page_source, 'html.parser')
try:
    soup = soup.find("div", {"class": "details-view"})
    iframe = soup.find('iframe')
    src = iframe['ng-src']
except KeyError:
    src = "https://elyon2.court.gov.il/Scripts9/mgrqispi93.dll?Appname=eScourt&Prgname=GetFileDetails_for_new_site&Arguments=-N" \
          + YEAR + "-00" + CASE_NUM + "-0"
except IndexError:
    src = "https://elyon2.court.gov.il/Scripts9/mgrqispi93.dll?Appname=eScourt&Prgname=GetFileDetails_for_new_site&Arguments=-N" \
          + YEAR + "-00" + CASE_NUM + "-0"
except AttributeError:
    src = "https://elyon2.court.gov.il/Scripts9/mgrqispi93.dll?Appname=eScourt&Prgname=GetFileDetails_for_new_site&Arguments=-N" \
          + YEAR + "-00" + CASE_NUM + "-0"
try:
    html_content = sess.get(LINK, proxies=proxies, timeout=30).text
except WebDriverException:
    src = "https://elyon2.court.gov.il/Scripts9/mgrqispi93.dll?Appname=eScourt&Prgname=GetFileDetails_for_new_site&Arguments=-N" \
          + YEAR + "-00" + CASE_NUM + "-0"
try:
    html_content = sess.get(LINK, proxies=proxies, timeout=30).text
except InvalidSessionIdException:

    print("InvalidSessionIdException:\n", src)
    pass
except  WebDriverException:

    print("InvalidSessionIdException:\n", src)
    pass
time.sleep(5)
soup = BeautifulSoup(html_content, 'html.parser')
if ((soup.find("head").title.text).find("חסוי") != -1):
    all_data = {}
    hidden_content = 1

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
                        infos.append(info)
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

try:
    all_data['מספר תיק מלא'] = case_name_num
    all_data['מספר תיק'] = case_name_num[case_name_num.find(" ") + 1:]
    all_data['ראשי תיבות תיק'] = case_name_num[:case_name_num.find(" ")]
    all_data['שנת תיק'] = '20' + case_name_num[case_name_num.find("/") + 1:]
    curr_year = str(datetime.date.today().year)[2:]
    if (int(case_name_num[case_name_num.find("/") + 1:]) > int(curr_year)): all_data['שנת תיק'] = '19' + case_name_num[
                                                                                                         case_name_num.find(
                                                                                                             "/") + 1:]
except KeyError:
    pass

doc = [[crawl_HTML(all_data, LINK, "פסק דין")]]  # רשימת מסמכי הHTML , כרגע רק 1
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
