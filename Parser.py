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


def cleanTXT(txt):
    # try:
    #     txt = text.encode('cp1252').decode('cp1255',errors='replace')
    # except UnicodeError:
    # 	txt = text

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



def HTML_CRAWLER(sess, link):
    proxies = {"http": "http://5.79.66.2:13081", "https": "https://5.79.66.2:13081"}

    try:
        retry = Retry(connect=3, backoff_factor=1)
        adapter = HTTPAdapter(max_retries=retry)
        sess.mount('http://', adapter)
        sess.mount('https://', adapter)
        html_content = sess.get(link, proxies=proxies, verify=False, timeout=15).text
    except Timeout:
        html_content = sess.get(link, proxies=proxies, verify=False, timeout=15).text

    except OSError:
        print("OSError from parser!!!")
        sess1 = requests.Session()
        html_content = sess1.get(link, proxies=proxies, verify=False, timeout=5).text

    time.sleep(0.5)
    soup = BeautifulSoup(html_content, 'html.parser')

    try:

        soup = soup.find('body').find("div",{"class":"WordSection1"})
        dirs = soup.findAll("div", {"align": "right"})
        dirs_1 = soup.findAll('p', {"class": "Ruller3"})

    except AttributeError:

        try:

            soup = BeautifulSoup(html_content, 'html.parser')
            soup = soup.find('body').find("div", {"class": "Section1"})
            dirs = soup.findAll("div", {"align": "right"}) # list of the labels
            dirs_1 = soup.findAll('p', {"class": "Ruller3"})

        except AttributeError:

            print("Attribute Error during parsing in: ")
            print(link)

    one = get_dict(dirs)
    return {**get_dict(dirs_1), **one}
    # for k, v in zip(all.keys(),all.values()):
    #     print(k,": ",v)


#
# link_psak_din = "https://supremedecisions.court.gov.il/Home/Download?path=HebrewVerdicts/20/520/073/e05&fileName=20073520.E05&type=2"
# link_hasuy = "https://supremedecisions.court.gov.il/Home/Download?path=HebrewVerdicts/21/650/089/e05&fileName=21089650.E05&type=2"
#
