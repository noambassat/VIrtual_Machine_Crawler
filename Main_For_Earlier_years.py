import Crawl_Data
import time
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


global filePath,DT_path, exe_path, Years_and_Nums,Logs_list
# !/usr/bin/env python3 # -*- coding: utf-8 -*-


#VARIABLES



# Paths

filePath = '/home/ubuntu/PycharmProjects/VIrtual_Machine_Crawler/Json_Files_2000/'
DT_path = '/home/ubuntu/PycharmProjects/VIrtual_Machine_Crawler/DataFrames/'
exe_path = '/home/ubuntu/PycharmProjects/pythonProject5/chromedriver'
log_df = '/home/ubuntu/PycharmProjects/VIrtual_Machine_Crawler/Log_dfs/Logs_DF_2000.csv'

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
# Full_Log_Dict = {}
Logs_list = []
Years_and_Nums = {x:7000 for x in range(2000,2003)} # { year_num : num_of_cases }


driver = webdriver.Chrome(exe_path, options=options)
def readANDsave_df(year):
    read_df = pd.read_csv(log_df)

    read_df.drop_duplicates(subset=['מספר הליך'], keep='last',inplace=True)


    read_df['סכימת שגיאות'] = 6 -(read_df[['קישור נפתח', 'תיק נמצא', 'ניסיון להורדת ההחלטות', 'הצלחה בהורדת ההחלטות', 'ניסיון להורדת מטא-דאטה', 'הצלחה בהורדת מטא-דאטה']].sum(axis=1))
    # print(int(read_df.iloc[-1, 0][:read_df.iloc[-1, 0].find("/")]))
    # if(int(read_df.iloc[-1, 0][:read_df.iloc[-1, 0].find("/")])>Years_and_Nums[year] and int(read_df.iloc[-1,-1])>5):
    #     print("deleting ",read_df.iloc[-1, 0])
    #     read_df = read_df.drop(read_df.index[-1],inplace=True)
    read_df.to_csv(log_df, index=False)

    return read_df

import random
def run(driver, year, range_lst):
    print(year)
    stop, STOP = 0,0  # The Continuous number of each year
    while (STOP < 5):  # While the crawler didn't reach the case's limit number yet. 5 is the max errors that can be thrown.
        if(stop==5): break
        stop+=1
        ind = random.randint(1,range_lst[-1])
        try:
            counter = range_lst[ind]
        except IndexError:
            try:
                counter += 1
            except UnboundLocalError:
                print(year)
                break

        try:
            df.to_csv(log_df, mode='a', index=False, header=False)
        except UnboundLocalError:
            pass
        except NameError:
            pass
        try:
            Case_Link = Crawl_Data.get_url(year, counter)
            curr_case = {"מספר הליך": "%d/%d" % (counter, year), "קישור לתיק": Case_Link, "קישור נפתח": False,
                         "תיק נמצא": False, \
                         "ניסיון להורדת ההחלטות": False, "הצלחה בהורדת ההחלטות": False, "סוג מסמך": "",
                         "ניסיון להורדת מטא-דאטה": False, "הצלחה בהורדת מטא-דאטה": False}

            df = pd.DataFrame(curr_case, index=[0])
            #########################

            try:
                driver.get(Case_Link)
            except WebDriverException as wde:
                print(str(wde), "\n", Case_Link)
                curr_case["קישור נפתח"] = False
                continue

            curr_case["קישור נפתח"] = True

            ##########################

            ####
            WebDriverWait(driver, 4)
            try:
                soup = BeautifulSoup(driver.page_source, 'html.parser')
            except UnexpectedAlertPresentException:
                print("UnexpectedAlertPresentException!!!")
                curr_case["קישור נפתח"] = False
                continue
            curr_case["קישור נפתח"] = True


            try:
                if (counter > Years_and_Nums[year]):
                    if ((soup.find("div", {"class": "col-md-11"}).text).find(" 0 מסמכים לפרמטרים") != -1):
                        STOP += 1
                        print("STOP ++")
                    if (STOP == 0):
                        driver.quit()
                        driver = webdriver.Chrome(exe_path, options=options)
                    curr_case["תיק נמצא"] = False
                    print("Could not find the case! case number ", counter)
                    print("Trying again ...")
                    continue
            except AttributeError:
                curr_case["תיק נמצא"] = False
                print("AttributeError")
                continue

            except UnexpectedAlertPresentException:
                driver.quit()
                driver = webdriver.Chrome(exe_path, options=options)
                curr_case["תיק נמצא"] = False
                print("UnexpectedAlertPresentException")
                continue
            STOP = 0
            curr_case["תיק נמצא"] = True
            curr_case["קישור נפתח"] = True
            # At least 2 secs must be waiting in order to load the webpage
            cont = 0
            flag = 0
            while 0 <= cont < 5:
                try:
                    myElem = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, 'row_0')))
                except TimeoutException:

                    try:
                        if ((soup.find("div", {"class": "col-md-11"}).text).find(" 0 מסמכים לפרמטרים") != -1):
                            curr_case["תיק נמצא"] = False
                            print("Couldn't find the case: ", counter)
                            flag = 1
                            break
                    except AttributeError:
                        pass
                    if cont == 4:
                        print("Loading took too much time! ID in the code not working!")
                        curr_case["תיק נמצא"] = False
                        driver.quit()
                        driver = webdriver.Chrome(exe_path, options=options)
                        flag = 1
                        break

                    print("Loading took too much time \nerror number ", cont + 1, "\nTrying once again ...")
                    cont += 1
                    continue
                except UnexpectedAlertPresentException:
                    driver.quit()
                    driver = webdriver.Chrome(exe_path, options=options)
                    curr_case["תיק נמצא"] = False
                    cont += 1
                    continue

                cont = -1  # no errors - break out from while loop
            if (flag != 0):
                ind += 1
                continue
            print("Time until now (get webdriver) is: ", datetime.now() - START_TIME)

            START_CURR_TIME = datetime.now()

            try:
                new_driver_flag = 0
                for I in range(3):
                    if(I==3):
                        driver.quit()
                        driver = webdriver.Chrome(exe_path, options=options)
                        driver.get(Case_Link)

                    try:
                        curr_case["ניסיון להורדת ההחלטות"] = True
                        print("Crawling Decisions ... ")
                        dec_df, LINK, conclusion, dict = Crawl_Data.Crawl_Decisions(driver,
                                                                                    Case_Link)  # Gets the button window

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
                    for t in range(2):
                        try:
                            name_on_page = soup.find("h2", {"class": "ng-binding"}).text
                            print("the name on page: ", name_on_page)
                            case_full_name = ""
                            for i, word in enumerate(name_on_page.split(" ")):
                                if (i == 1):
                                    case_full_name += word
                                    break
                                case_full_name += word + " "

                            print(case_full_name)
                        except AttributeError:
                            case_full_name = ""
                            driver.get(Case_Link)
                            time.sleep(1)
                        if(case_full_name!=0):break
                    data = Crawl_Data.CrawlTopWindow(Case_Link, LINK, conclusion, dict,
                                                     case_full_name)  # Gets the upper window
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
            curr_case["הצלחה בהורדת מטא-דאטה"] = True
            json_name = str(year) + "__" + str(counter)
            data['פרטי תיק']['שם הקובץ'] = json_name
            Save_As_Json.writeToJsonFile(filePath, json_name, data)  # Write to Json file
            print("--done saving to json--")
            print("Time until now current case (Done downloading current file) is: ",
                  datetime.now() - START_CURR_TIME)

            ind += 1
            df = pd.DataFrame(curr_case, index=[0])

            Logs_list.append(curr_case)
        # Full_Log_Dict[year] = {"................."}
        except UnexpectedAlertPresentException:
            driver.quit()
            driver = webdriver.Chrome(exe_path, options=options)
            continue


    df.to_csv(log_df, mode='a', index=False, header=False)
def get_lists(year):
    missing_cases,cases_names  = set(),set()
    read_df = readANDsave_df(year)
    for ind in read_df.index:

        try:
            case_name = read_df['מספר הליך'][ind]
            case_num = int(case_name[:case_name.find("/")])
            YEAR = int(case_name[case_name.find("/")+1:])

            # print(case_num)
            if(YEAR!=year): continue ################################# year != year -> בדיקה אחרי כל שנה.
            if(read_df['סכימת שגיאות'][ind]>5):
                missing_cases.add(case_num)
                continue

            cases_names.add(case_num)
        except ValueError:
            print("Value error on case_name = ", case_name ,"\n case num = ",case_num)
            continue
    return missing_cases,cases_names

def get_missing_cases(driver, year):

    for I in range(3):
        print("Crawling missing cases of year: ", year)
        missing_cases, cases_names = get_lists(year)
        print("there were found ", len(missing_cases), " missing cases!")
        for con in range(1,len(cases_names)):
            if con not in cases_names: missing_cases.add(con)
        missing_cases = sorted(missing_cases)
        print(missing_cases)
        if(len(missing_cases)==5): break
        run(driver, year, missing_cases)
        missing_cases, cases_names = get_lists(year)
        print("After running the missed cases again, there were left ", len(missing_cases))
        print(missing_cases)
        print("Done crawling missing cases for round ", I)
        print("The were left ",len(missing_cases), " cases")
    return missing_cases

already_crawled = [2011]
for year in Years_and_Nums.keys():
    if(year in already_crawled): continue
        # missing_cases = get_missing_cases(driver, year)

    readANDsave_df(year)
    run(driver, year, range(1,Years_and_Nums[year]+1)) #################

    ################################################
    # missing_cases = get_missing_cases(driver, year)
    already_crawled.append(year)

#################################################
# Logs_DF = pd.DataFrame(columns=Logs_list[0].keys())
# Logs_DF.to_csv("Full_Logs_DF.csv")



