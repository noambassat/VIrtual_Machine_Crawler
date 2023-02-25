import time
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
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import UnexpectedAlertPresentException
import Save_As_Json

########################### need to add urllib3.exceptions.MaxRetryError
# !/usr/bin/env python3 # -*- coding: utf-8 -*-


# VARIABLES


# Paths
filePath = '/home/ubuntu/PycharmProjects/VIrtual_Machine_Crawler/crawl_again_Json_Files/'
DT_path = '/home/ubuntu/PycharmProjects/VIrtual_Machine_Crawler/DataFrames/'
exe_path = '/home/ubuntu/PycharmProjects/pythonProject5/chromedriver'
links_path = '/home/ubuntu/Normalizer/Normalizer/crawl_again.csv'

##############3


# links_path = "C:/Users/Noam/PycharmProjects/pythonProject5/Normalizer/crawl_again.csv"

warnings.simplefilter(action='ignore', category=(FutureWarning, DeprecationWarning))
START_RUN_TIME = datetime.now()

# PROXY
options = Options()
PROXY = "5.79.66.2:13081"
options.add_argument('--proxy-server=%s' % PROXY)

driver = webdriver.Chrome(exe_path, options=options)


def run(driver, links):
    STOP = 0
    for Case_Link in links:

        while (
                STOP < 5):  # While the crawler didn't reach the case's limit number yet. 5 is the max errors that can be thrown.
            for i in range(7):
                if (Case_Link[67 + i] == "/"): break

            counter = Case_Link[67:67 + i]

            year = Case_Link[62:66]
            add_case = counter
            while (len(add_case) != 6): add_case = "0" + add_case
            add_case = "-" + add_case

            try:

                Case_Link = Crawl_Data.get_url(year, counter).replace(" ", "")
                print(Case_Link, "\n!!!")
                curr_case = {"מספר הליך": "%d/%d" % (int(counter), int(year)), "קישור לתיק": Case_Link,
                             "קישור נפתח": False,
                             "תיק נמצא": False, \
                             "ניסיון להורדת ההחלטות": False, "הצלחה בהורדת ההחלטות": False, "סוג מסמך": "",
                             "ניסיון להורדת מטא-דאטה": False, "הצלחה בהורדת מטא-דאטה": False}

                df = pd.DataFrame(curr_case, index=[0])
                #########################

                try:
                    for i in range(3):
                        try:
                            driver = webdriver.Chrome(exe_path)
                            driver.get(Case_Link)
                        except WebDriverException:
                            continue
                        break
                except:
                    print("!!!")

                ##########################

                ####
                WebDriverWait(driver, 4)
                try:
                    soup = BeautifulSoup(driver.page_source, 'html.parser')
                except UnexpectedAlertPresentException:
                    print("UnexpectedAlertPresentException!!!")
                    driver.quit()
                    driver = webdriver.Chrome(exe_path, options=options)
                    curr_case["קישור נפתח"] = False
                    continue
                except TypeError:
                    print("TypeError!!!")
                    curr_case["קישור נפתח"] = False
                    continue
                curr_case["קישור נפתח"] = True

                STOP = 0
                curr_case["תיק נמצא"] = True
                curr_case["קישור נפתח"] = True
                # At least 2 secs must be waiting in order to load the webpage
                time.sleep(2)
                cont = 0
                flag = 0
                while 0 <= cont < 5:
                    try:
                        myElem = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.ID, 'row_0')))
                        myElem_2 = WebDriverWait(driver, 3).until(
                            EC.presence_of_element_located((By.CLASS_NAME, 'ng-binding')))
                    except TimeoutException:

                        try:
                            if ((soup.find("div", {"class": "col-md-11"}).text).find(" 0 מסמכים לפרמטרים") != -1):
                                curr_case["תיק נמצא"] = False
                                print("Couldn't find the case: ", counter)
                                flag = 1
                                break
                        except AttributeError:
                            cont += 1
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
                if (flag != 0): continue

                START_CURR_TIME = datetime.now()

                try:

                    # curr_case["ניסיון להורדת מטא-דאטה"] = True
                    for t in range(2):
                        try:
                            # print(soup.find("div", {"class": "ng-scope"}).text)
                            time.sleep(1)
                            name_on_page = soup.find("h2", {"class": "ng-binding"})
                            name_on_page = name_on_page.text

                            case_full_name = ""
                            for i, word in enumerate(name_on_page.split(" ")):
                                if (i == 1):
                                    case_full_name += word
                                    break
                                case_full_name += word + " "

                        except AttributeError:
                            print("couldn't find case's name")
                            case_full_name = name_on_page
                            try:
                                driver.get(Case_Link)
                            except WebDriverException:
                                driver.quit()
                                driver = webdriver.Chrome(exe_path, options=options)
                                continue

                        if (not (case_full_name is None)):
                            print("Found! case name = ", case_full_name)
                            break
                    for I in range(3):
                        if (I == 3):

                            driver.quit()
                            driver = webdriver.Chrome(exe_path, options=options)
                            try:
                                driver.get(Case_Link)
                            except WebDriverException:
                                print("WEB DRIVER EXCEPTION NUM 13")
                                continue

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
                        except UnboundLocalError as ULE:
                            print("couldn't crawl data")
                            curr_case["הצלחה בהורדת ההחלטות"] = False
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
                        data = Crawl_Data.CrawlTopWindow(Case_Link, LINK, conclusion, dict,
                                                         case_full_name)  # Gets the upper window

                    except UnboundLocalError as ULE:
                        print(ULE)
                        print("couldn't crawl data")
                        curr_case["הצלחה בהורדת מטא-דאטה"] = False
                        data = 0
                        continue
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
                            continue
                        except UnboundLocalError as ULE:
                            print("couldn't crawl data")
                            curr_case["הצלחה בהורדת ההחלטות"] = False
                            data = 0
                            continue

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

                df = pd.DataFrame(curr_case, index=[0])

            # Full_Log_Dict[year] = {"................."}
            except UnexpectedAlertPresentException:
                driver.quit()
                driver = webdriver.Chrome(exe_path, options=options)
                continue


def get_links(links_path):
    df = pd.read_csv(links_path, index_col=False)
    links_list = list(df["קישור לתיק"])

    print(links_list)
    print(len(links_list))
    return links_list


#################################################


links = get_links(links_path)

run(driver, links)


