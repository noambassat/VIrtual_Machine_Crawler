import Crawl_Data
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import warnings
from selenium.common.exceptions import WebDriverException, InvalidSessionIdException, NoSuchElementException, \
    UnexpectedAlertPresentException
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import UnexpectedAlertPresentException
import Save_As_Json

# !/usr/bin/env python3 # -*- coding: utf-8 -*-


#VARIABLES

global filePath,DT_path, exe_path


# Paths
filePath = '/home/ubuntu/PycharmProjects/pythonProject5/NewMain/Json_Files/'
DT_path = '/home/ubuntu/PycharmProjects/pythonProject5/NewMain/DataFrames/'
exe_path = '/home/ubuntu/PycharmProjects/pythonProject5/chromedriver'


warnings.simplefilter(action='ignore', category=(FutureWarning, DeprecationWarning))
START_RUN_TIME = datetime.now()


# PROXY
options = Options()
PROXY = "5.79.66.2:13081"
options.add_argument('--proxy-server=%s' % PROXY)

""""
IMPORTANT LOGICAL LINKS:
    src = "https://elyon2.court.gov.il/Scripts9/mgrqispi93.dll?Appname=eScourt&Prgname=GetFileDetails_for_new_site&Arguments=-N" \
          + YEAR + add_case + "-0"  ---> FOR CRAWLING TOP WINDOW


    Case_Link = "https://supremedecisions.court.gov.il/Verdicts/Results/1/null/"+ str(year) +"/" + str(case_num) +"/1/8/null/null/null"
"""
START_TIME = datetime.now()

Log_DF = pd.DataFrame()
Full_Log_Dict = {}
Logs_list = []
Years_and_Nums = {2011:9775} # { year_num : num_of_cases }

driver = webdriver.Chrome(exe_path, options=options)

for year in Years_and_Nums.keys(): # CURR -> 2011 ONLY
    counter, STOP = 391,0  # The Continuous number of each year
    while(counter<Years_and_Nums[year] and STOP < 5): # While the crawler didn't reach the case's limit number yet. 5 is the max errors that can be thrown.
        try:
            df.to_csv('Logs_DF.csv', mode='a', index=False, header=False)
        except UnboundLocalError:
            pass
        except NameError:
            pass


        Case_Link = Crawl_Data.get_url(year, counter)
        curr_case = {"מספר הליך": "%d/%d" % (counter, year),"קישור לתיק": Case_Link,"קישור נפתח":False,"תיק נמצא":False,\
                     "ניסיון להורדת ההחלטות":False,"הצלחה בהורדת ההחלטות": False, "סוג מסמך": "", "ניסיון להורדת מטא-דאטה": False,"הצלחה בהורדת מטא-דאטה":False}

        #########################

        try:
            driver.get(Case_Link)
        except WebDriverException as wde:
            print(str(wde),"\n",Case_Link)
            curr_case["קישור נפתח"] = False
            continue


        curr_case["קישור נפתח"] = True

        ##########################

        ####
        WebDriverWait(driver,4)
        try:
            soup = BeautifulSoup(driver.page_source, 'html.parser')
        except UnexpectedAlertPresentException:
            print("UnexpectedAlertPresentException!!!")
            curr_case["קישור נפתח"] = False
            continue


        try:
            if (counter > Years_and_Nums[year]):
                if((soup.find("div", {"class": "col-md-11"}).text).find(" 0 מסמכים לפרמטרים")!=-1):
                    STOP += 1
                    print("STOP ++")
                if(STOP==0):
                    driver.close()
                    driver = webdriver.Chrome(exe_path, options=options)
                curr_case["תיק נמצא"] = False
                print("Could not find the case!")
                print("Trying again ...")
                continue
        except AttributeError:
            pass
        STOP = 0
        curr_case["תיק נמצא"] = True
    # At least 2 secs must be waiting in order to load the webpage
        cont = 0
        while 0 <= cont < 5:
            try:
                myElem = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, 'row_0')))
            except TimeoutException:
                if cont == 4:
                    print("Loading took too much time! ID in the code not working!")
                    curr_case["תיק נמצא"] = False
                    break
                print("Loading took too much time \nerror number ", cont+1, "\nTrying once again ...")
                cont += 1
                continue
            except UnexpectedAlertPresentException:
                driver.close()
                driver = webdriver.Chrome(exe_path, options=options)
            cont = -1  # no errors - break out from while loop

        print("Time until now (get webdriver) is: ", datetime.now() - START_TIME)

        START_CURR_TIME = datetime.now()

        try:
            for I in range(3):
                try:
                    curr_case["ניסיון להורדת ההחלטות"] = True
                    print("Crawling Decisions ... ")
                    dec_df, LINK, conclusion, dict = Crawl_Data.Crawl_Decisions(driver, Case_Link)  # Gets the button window

                except OSError as error:
                    print("OS Error, on Crawl_Decisions, error num:", I + 1)
                    curr_case["הצלחה בהורדת ההחלטות"] = False
                    print(error)
                    continue
                break

            if (len(dec_df) == 0):
                print("0 DEC!!!\n", Case_Link)
                try:
                    driver.get(Case_Link)
                except WebDriverException:
                    print("WebDriverException")
                curr_case["הצלחה בהורדת ההחלטות"] = False
                continue

            curr_case["הצלחה בהורדת ההחלטות"] = True
            curr_case["סוג מסמך"] = conclusion
            print("Time until now current case (Crawl_Decisions) is: ", datetime.now() - START_CURR_TIME)

            print("The len of decisions table: ", len(dec_df))

            try:

                curr_case["ניסיון להורדת מטא-דאטה"] = True
                try:
                    name_on_page = soup.find("h2",{"class":"ng-binding"}).text

                    case_full_name = ""
                    for i,word in enumerate(name_on_page.split(" ")):
                        if (i == 1):
                            case_full_name += word
                            break
                        case_full_name += word + " "

                    print(case_full_name)
                except AttributeError:
                    case_full_name = ""
                data = Crawl_Data.CrawlTopWindow(Case_Link, LINK, conclusion, dict,case_full_name)  # Gets the upper window
            # print("check type the len: ",type(data))

            except OSError as error:
                print("OS Error, on CrawlTopWindow, error num:", I + 1)
                print(error)
                try:
                    data = Crawl_Data.CrawlTopWindow(Case_Link, LINK, conclusion, dict)
                except OSError as error:
                    print("OS Error, on CrawlTopWindow, error num:", I + 1)
                    print(error)
                    curr_case["הצלחה בהורדת מטא-דאטה"] = False
                    data = 0

            try:
                if (len(data) < 2):
                    print("MAIN GOT LEN LESS THAN !!!!!!!")
                    curr_case["הצלחה בהורדת מטא-דאטה"] = False
                    continue
            except:

                print("error while crawling top window")

                curr_case["הצלחה בהורדת מטא-דאטה"] = False
                continue

            #######
            curr_case["הצלחה בהורדת מטא-דאטה"] = True
            data['פרטי תיק']['תאריך יצוא הקובץ'] = str(datetime.now().date())

            print("Time until now current case (CrawlTopWindow) is: ", datetime.now() - START_CURR_TIME)

            if data == 0:
                print("Data Error! check the CrawlTopWindow from CrawlJSON file")
                curr_case["הצלחה בהורדת מטא-דאטה"] = False
                continue

        except KeyError:
            print("KEY ERROR")

        except UnexpectedAlertPresentException:

            print("UnexpectedAlertPresentException, continue")
            curr_case["הצלחה בהורדת מטא-דאטה"] = False
            continue

        json_name = str(year) + "__" + str(counter)
        data['פרטי תיק']['שם הקובץ'] = json_name
        Save_As_Json.writeToJsonFile(filePath, json_name, data)  # Write to Json file
        print("--done saving to json--")
        print("Time until now current case (Done downloading current file) is: ",
              datetime.now() - START_CURR_TIME)


        counter += 1
        df = pd.DataFrame(curr_case, index=[0])

        Logs_list.append(curr_case)
    # Full_Log_Dict[year] = {"................."}
df.to_csv('Logs_DF.csv', mode='a', index=False, header=False)

# Logs_DF = pd.DataFrame(columns=Logs_list[0].keys())
# Logs_DF.to_csv("Full_Logs_DF.csv")



