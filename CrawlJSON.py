from selenium.common.exceptions import WebDriverException, InvalidSessionIdException
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import requests
import time

main_df = pd.read_csv(r'Decisions_Table/Decisions_Table.csv',index_col=0)
options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')  # Last I checked this was necessary.

def crawl_HTML(data, link, type):
    xml = requests.get((link))
    soup = BeautifulSoup(xml.content, 'lxml')
    labels = []
    contents = []
    text = soup.findAll("p",{"class":"BodyRuller"})

    for s in range(len(text)):
        string = cleanTXT(text[s].text)
        space= string.find(":")
        if(space!=-1):
            labels.append(string[:space])
            content = []
            for i in range(s+1,len(text)):

                string = cleanTXT(text[i].text)

                if(string.find(":")!=-1):
                    s=i+1
                    break
                if(string.find("נגד")!=-1 or string.find("המשיב")!=-1): break
                if (len(string) > 1): content.append(string)

            if(len(content)>1): contents.append(content)

    dict = {}
    dict['סוג מסמך'] = type
    dict['מסמך מלא'] = (soup.text.replace('\n\n','')).replace(u'\xa0', u' ')
    dict['קישור למסמך'] = link
    for i in range(len(labels)):
        try:
            dict[labels[i]] = contents[i]
        except IndexError:
            break

    soup = BeautifulSoup(xml.content, 'lxml')
    conclusion = ""
    for row in soup.findAll("p",{"class":"Ruller41"}):
        conclusion += row.text
    dict["סיכום מסמך HTML"] = conclusion
    return dict

def Get_LINK(df,CASE): # רק פסק-דין או החלטה אחרונה כרגע
    conclusion = "החלטה \n"
    if(len(df)==0): return '',''
    LINK = df['HTML_Link'][0]
    for i in df.index:
        if(df['סוג מסמך'][i] == 'פסק-דין'):
            conclusion = 'פסק-דן'
            LINK = df['HTML_Link'][i]
            break
    return LINK, conclusion

def cleanTXT(txt):
    txt = txt.replace(u'\xa0', u' ')
    txt = txt.replace('  ','')
    txt = txt.replace('\n','')
    txt = txt.replace('\t','')

    return txt

def add_counters(data):
    temp_data = data.copy()
    for key in data.keys():
        if (key == "פרטים כלליים" or key == 'תיק חסוי'): continue # doesn't count this keys
        curr_key = 'מספר ' + str(key) + ' בתיק'
        temp_data[curr_key] = len(temp_data[key])
    return temp_data

def CrawlTopWindow(CASE, n_decisions,LINK,conclusion, dict):
    hidden_content = 0
    CASE_NUM = CASE[67:67+4]
    YEAR = CASE[62:66]

    try:
        driver = webdriver.Chrome(executable_path='C:/Users/Noam/Desktop/Courts Project/chromedriver.exe',chrome_options=options)
        driver.get(CASE)

    except WebDriverException:
        driver = webdriver.Chrome(executable_path='C:/Users/Noam/Desktop/Courts Project/chromedriver.exe',chrome_options=options)
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
        data = {}

        for i in range(len(labels)):
            data[cleanTXT(labels[i].text)] = cleanTXT(details[i].text)

        all_data[LABELS[0]] = data

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
                    for z, td in enumerate(tr.findAll("td")):

                        try:
                            label = (cleanTXT(td['data-label']))
                            info = (cleanTXT(td.text))
                            labels.append(label)
                            infos.append(info)
                        except KeyError:
                            pass
                    row = {labels[n]:infos[n] for n in range(len(labels))}
                    data.append(row)
                all_data[LABELS[i + 1]] = data

        ### ADDING COUNTERS

    else:
        all_data['תיק חסוי'] = True

    all_data = add_counters(all_data)

    all_data['Case Number'] = CASE_NUM
    all_data['מספר החלטות'] = n_decisions
    all_data['קישור לתיק'] = CASE

    docs_arr=[crawl_HTML(all_data,LINK,conclusion)] # רשימת מסמכי הHTML , כרגע רק 1
    for row in dict.values():
        row.pop("Case Number")
        if row not in docs_arr: docs_arr.append(row)
    new_dict = {"פרטי תיק":all_data,"מסמכים":docs_arr}
    driver.close()
    return new_dict

def Crawl_Decisions(CASE):
    src = "https://elyon2.court.gov.il/Scripts9/mgrqispi93.dll?Appname=eScourt&Prgname=GetFileDetails_for_new_site&Arguments=-N2014-008568-0"
    CASE_NUM = CASE[67:67 + 4] + "/"+ CASE[64:64 + 2]
    driver = webdriver.Chrome(executable_path='C:/Users/Noam/Desktop/Courts Project/chromedriver.exe',chrome_options=options)
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
                temp['Case Number'] = CASE_NUM
                info = cleanTXT( case.text)
                if(info.find('פסק')!=-1 and info.find('דין')!=-1): indo = "פסק דין"
                temp[label] = info
            if (len(temp) == 0): continue
            for link in hrefs:
                temp['HTML_Link'] ='https://supremedecisions.court.gov.il/'+link['href']
            case_dec[i] = temp

    except AttributeError : pass

    for row in (case_dec.values()):
        df = df.append(row, ignore_index=True)
    df.drop_duplicates(inplace=True)
    main_df = pd.read_csv(r'Decisions_Table/Decisions_Table.csv',index_col=0)
    main_df = main_df.append(df)
    main_df=main_df.reindex()
    main_df.to_csv('Decisions_Table/Decisions_Table.csv')
    LINK, conclusion = Get_LINK(df,CASE)
    driver.close()
    return df, len(df), LINK,conclusion, case_dec