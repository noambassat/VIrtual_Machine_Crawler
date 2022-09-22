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

        if (text.find("בשם ה") != -1 and text.find("להצטרף")==-1):
            labels,contents = slicer(text, labels,contents)
            continue  ################################################

        labels.append(text[:text.find(":")].replace('\n',' '))

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
    for n in range(len(labels)):
        try:
            all[labels[n]] =contents[n]
            if(labels[n].find('פני')!=-1): all["מספר השופטים"] = len(contents[n])
        except IndexError:
            pass

    return all

def slicer(text,labels,contents):
    for text in text.split('\n\n'):
        content = []
        text = cleanTXT(text).replace("\n",' ')
        content_ = (text[text.find(":")+1:])

        if len(text) == 0: continue
        if(text.find(":")!=-1):
            labels.append(cleanTXT(text[:text.find(":")]))
            # continue
            # continue
        for info in ((content_.replace(";",",").replace("\n",","))[content_.find(":")+1:]).split(','):
            info = re.sub(r'(\d)+\. ','', info)
            info = cleanTXT(info.replace('-',' '))
            if(len(info)!=0): content.append(cleanTXT(info))
        if(len(content)!=0): contents.append(content)
        else: contents.append("אין מידע")
    return labels,contents



def HTML_CRAWLER(link):

    for I in range(3):
        try:
            print(link)
            conn = http.client.HTTPSConnection("api.webscrapingapi.com")
            src = "/v1?url=" + (urllib.parse.quote(link, safe="")) + "&api_key=qWLe3iMqS89nggeKenmcQHoI5o34uZuR&device=desktop&proxy_type=datacenter&render_js=1&wait_until=domcontentloaded&timeout=30000"
            conn.request("GET", src)
            res = conn.getresponse()
            data = res.read()
            html_content = (data.decode("utf-8"))
        except OSError:
            print("OSERROR IN CRAWL HTML, PARSER, NUMBER: ",I)
        if (len(html_content) > 2): break
    #
    # except OSError:
    #     print("OSError from parser!!!")
    #     sess1 = requests.Session()
    #     html_content = sess1.get(link, proxies=proxies, verify=False, timeout=10).text

    soup = BeautifulSoup(html_content, 'html.parser')
    for I in range(2):
        try:

            dirs = soup.findAll("div", {"align": "right"})
            dirs_1 = soup.findAll('p', {"class": "Ruller3"})


        except AttributeError:
            print("AttributeError in parser")
        if(len(dirs)>1): break
    try:
        soup = soup.find('body').find("div", {"class": "WordSection1"})
    except AttributeError:
        pass

    one = get_dict(dirs)
    return {**get_dict(dirs_1), **one}
    # for k, v in zip(all.keys(),all.values()):
    #     print(k,": ",v)


#
# link_psak_din = "https://supremedecisions.court.gov.il/Home/Download?path=HebrewVerdicts/20/520/073/e05&fileName=20073520.E05&type=2"
# link_hasuy = "https://supremedecisions.court.gov.il/Home/Download?path=HebrewVerdicts/21/650/089/e05&fileName=21089650.E05&type=2"
#

