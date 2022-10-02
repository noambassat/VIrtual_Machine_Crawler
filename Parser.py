from bs4 import BeautifulSoup
import time
import re
from urllib3.exceptions import InsecureRequestWarning
from urllib3 import disable_warnings
from requests.exceptions import Timeout
disable_warnings(InsecureRequestWarning)
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

import http.client
import urllib.parse


def cleanTXT(txt):

    txt = txt.replace("'","")
    txt = (re.sub(r'(\ )+', ' ', txt))
    try:
        if (txt[0].isspace()):   txt = txt[1:]
        if (txt[-1].isspace()): txt = txt[:-1]
    except IndexError: return re.sub(r'(\d)+\. ', '', txt)

    txt = txt.replace(u'\xa0', u' ')

    txt = txt.replace("נ ג ד"," נגד ")
    txt = txt.replace('פסק-דין','פסק דין')
    txt = txt.replace('\r',' ')

    txt = txt.replace('  ', ' ')
    txt = txt.replace("נ ג ד", " נגד ")
    txt = txt.replace("\'", "'")
    if(txt==' ' or txt=='  '): return ''

    return txt
def get_dict(dirs):

    labels = []
    contents = []
    for s in dirs:
        text = cleanTXT(s.text).replace(" נגד ","")
        if(len(text)==0 or text.find(":")==-1):continue
        con = False
        for k_word in ['בשם','בם']:
            if (text.find(k_word) != -1 and text.find("להצטרף")==-1):
                labels,contents = slicer(text, labels,contents)
                con=True
                break

        if(con): continue  ################################################
        # elif (text.find("בם") != -1 and text.find("להצטרף") == -1):
        #     labels, contents = slicer(text, labels, contents)
        #     continue  ################################################
        labels.append(cleanTXT(text[:text.find(":")].replace('\n',' ')).replace(" נגד ",""))

        info = (text[text.find(":")+1:])
        content = []
        for row in info.split('\n\n'):  # content
            row = cleanTXT(row).replace('\n ',' ')
            if len (row) == 0 : continue
            row = re.sub(r'(\d)+\. ', '', row)
            row = row.replace('-',' ')
            if(len(row)!=0): content.append(cleanTXT(row))
        if(len(content)!=0): contents.append(content)
        else: contents.append("אין מידע")


        # NEXT SESSION
    all = {}
    jud = 0
    for n in range(len(labels)):
        try:
            print(labels[n],": ", contents[n])
            if(labels[n].find("לפני")!=-1):
                labels[n] = "לפני"
                jud = len(contents[n])
            all[labels[n]] = contents[n]
            # print(labels[n],": ", contents[n])




        # except TypeError as err:

        except IndexError:
            pass
    all["מספר השופטים"] = jud
    print(all.keys())
    return all


def get_deviders(string):
    # NEW FUNCTION
    # when there is a row like "עו"ד מיכל עו"ד גלעד" it doesnt catch this as an array. this function adds , between the titles in order to be able to split them in the next loop
    if (string.find( ' ועו"ד ') != -1): string = string.replace("\n", " ").replace(' ועו"ד ', ',עו"ד ')

    elif (string.find( ' עו"ד ') != -1 and string.find("' עו") == -1): string = string.replace("\n", " ").replace(' עו"ד ', ',עו"ד ')
    dividers = [";",'\n']
    for div in dividers: string = string.replace(div, ",")
    return string

def slicer(text,labels,contents):
    for txt in text.split('\n\n'):
        content = []
        txt = cleanTXT(txt).replace("\n",' ')
        string = (txt[txt.find(":")+1:])
        content_ = get_deviders(string)

        if len(txt) == 0: continue
        if(txt.find(":")!=-1):
            labels.append(cleanTXT(txt[:txt.find(":")]).replace(" נגד ",""))
            # continue

        for info in (content_[content_.find(":")+1:]).split(','):
            info = re.sub(r'(\d)+\. ','', info)
            info = cleanTXT(info.replace('-',' '))
            if(len(info)!=0): content.append(cleanTXT(info))
        if(len(content)!=0): contents.append(content)


    if(len(labels)>len(contents)):
        content_ = cleanTXT(text[text.find(":") + 1:]).replace('-',' ')
        if(content_.find(";")!=-1):
            for con in content_.split(';'):
                if(len(con)>0):
                    content.append(con.replace('\n',''))
            contents.append(content)
        elif (content_.find(",") != -1):
            for con in content_.split(','):
                if(len(con)>0):
                    content.append(con.replace('\n',''))
            contents.append(content)

        else:
            if(len(content_.replace('\n',''))>0):
                contents.append([content_.replace('\n','')])


        if(len(contents)==0):
            print("COULDNT GET THE CONTENT OF ", labels, " in the parser")
            contents.append("אין מידע")
    return labels,contents

def two_cases(soup):
    ################# PROBLEM HERE!!!!!!!
    ### TRY OUT IN CASE NUMBER 138, 02-01-2016
    ### 02-01-2016__138
    print("תיק מאוחד!!!!!!! לבדוק איך מטפלים בו ?")

    full_text = ""
    for s in soup.findAll("div", {"align": "right"}): full_text+= (s.text)
    print(repr(k) for k in full_text)
    print("_________________________")
    labels = []
    contents = []
    print("--------------- first try splitlines()")
    count_zero = 0
    for sec in full_text.splitlines():
        if(len(sec)==0):
            count_zero+=1
            continue
        else:
            print(count_zero)
            count_zero = 0
        print((sec))
    print("------------------- second try split(double enter)")
    count_zero = 0

    for sec in full_text.split("\n\n"):
        if (len(sec) == 0):
            count_zero += 1
            continue
        else:
            print(count_zero)
            count_zero = 0
        print((sec))
    print("------------------- third try split(xa0)")
    count_zero = 0

    for sec in full_text.split("\xa0"):
        if((sec)==0):
            count_zero+=1
            continue
        else:
            print(count_zero)
            count_zero = 0
        print((sec))

def HTML_CRAWLER(link):
    two_cases_bool = False
    try:
        conn = http.client.HTTPSConnection("api.webscrapingapi.com")
        src = "/v1?url=" + (urllib.parse.quote(link, safe="")) + "&api_key=UNVeJ3Li18J7vh36TLDJxZlVRLJBdyvQ&device=desktop&proxy_type=datacenter&render_js=1&wait_until=domcontentloaded&timeout=30000"

        conn.request("GET", src)
        res = conn.getresponse()
        data = res.read()
        html_content = (data.decode("utf-8"))
    except OSError:
        print("OSERROR IN CRAWL HTML")
    if (len(html_content)<5): print("HTML CRAWEL GOT LEN LOWER THAN 5!!!", html_content)


    soup = BeautifulSoup(html_content, 'html.parser')
    for I in range(2):
        try:
            if (len(soup.findAll('p', {"class": "FileNumber"})) > 1):
                print(link)
                # two_cases(soup)
                two_cases_bool = True
                #return two_cases(soup)
            dirs = soup.findAll("div", {"align": "right"})

            dirs_1 = soup.findAll('p', {"class": "Ruller3"})

        except AttributeError:
            print("AttributeError in parser")
        if(len(dirs)>1): break
    # try:
    #     soup = soup.find('body').find("div", {"class": "WordSection1"}) ###?????###
    # except AttributeError:
    #     pass

    one = get_dict(dirs)
    one["כל קוד הטמל"] = str(soup)
    one["מסמך מאוחד"] = two_cases_bool

    return {**get_dict(dirs_1), **one}
