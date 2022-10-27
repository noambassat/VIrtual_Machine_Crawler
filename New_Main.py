from datetime import datetime
import pandas as pd
import time
import warnings
import Crawl_Data
import requests
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
import requests
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
    counter= 1  # The Continuous number of each year
    STOP = 0
    while(counter<Years_and_Nums[year] and STOP < 5): # While the crawler didn't reach the case's limit number yet. 5 is the max errors that can be thrown.
        curr_case = {"Case number": "%d %d" % (counter, year)}

        Case_Link = Crawl_Data.get_url(year, counter)
        try:
            driver.get(Case_Link)
        except WebDriverException as wde:
            print(str(wde),"\n",Case_Link)



        ####
        WebDriverWait(driver,3)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        if(counter>Years_and_Nums[year]):
            try:
                if((soup.find("div", {"class": "col-md-11"}).text).find(" 0 מסמכים לפרמטרים")!=-1):
                    STOP += 1
                    print("STOP ++")
                    continue
            except AttributeError:
                pass



    # At least 2 secs must be waiting in order to load the webpage
        cont = 0
        while 0 <= cont < 5:
            try:
                myElem = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, 'row_0')))
            except TimeoutException:
                if cont == 4:
                    print("Loading took too much time! ID in the code not working!")
                    break
                print("Loading took too much time \nerror number ", cont+1, "\nTrying once again ...")
                cont += 1
                continue
            cont = -1  # no errors - break out from while loop

        print("Time until now (get webdriver) is: ", datetime.now() - START_TIME)

        START_CURR_TIME = datetime.now()

        try:
            for I in range(3):
                try:
                    dec_df, LINK, conclusion, dict = Crawl_Data.Crawl_Decisions(driver, Case_Link)  # Gets the button window
                except OSError as error:
                    print("OS Error, on Crawl_Decisions, error num:", I + 1)
                    print(error)
                    continue
                if (len(dec_df) > 0): break
            if (len(dec_df) == 0):
                print("0 DEC!!!\n", Case_Link)
                driver.get(Case_Link)
                continue
            print("Time until now current case (Crawl_Decisions) is: ", datetime.now() - START_CURR_TIME)

            print("The len of decisions table: ", len(dec_df))

            try:
                #
                data = Crawl_Data.CrawlTopWindow(Case_Link, LINK, conclusion, dict)  # Gets the upper window
            # print("check type the len: ",type(data))
            except OSError as error:
                print("OS Error, on CrawlTopWindow, error num:", I + 1)
                print(error)
                data = data = Crawl_Data.CrawlTopWindow(Case_Link, LINK, conclusion, dict)
            if (len(data) < 2): print("MAIN GOT LEN LESS THAN 2!!!!!!!")

            #######
            data['פרטי תיק']['תאריך יצוא הקובץ'] = str(datetime.now().date())

            print("Time until now current case (CrawlTopWindow) is: ", datetime.now() - START_CURR_TIME)

            if data == 0:
                print("Data Error! check the CrawlTopWindow from CrawlJSON file")
                continue


        except KeyError:
            print("KEY ERROR")

        except UnexpectedAlertPresentException:
            counter -= 1
            print("UnexpectedAlertPresentException, continue")
            continue
        json_name = str(year) + "__" + str(counter)
        data['פרטי תיק']['שם הקובץ'] = json_name
        Save_As_Json.writeToJsonFile(filePath, json_name, data)  # Write to Json file
        print("--done saving to json--")
        print("Time until now current case (Done downloading current file) is: ",
              datetime.now() - START_CURR_TIME)



        counter += 1
        Logs_list.append(curr_case)

        if counter == 3: break #############################################

    # except UnexpectedAlertPresentException:
    #
    # print("UnexpectedAlertPresentException")
    #
    # continue
    #
    # except AttributeError:
    #
    # print("AttributeError")
    #
    # continue
    #
    # except UnboundLocalError:
    #
    # print("UnboundLocalError")
    #
    # continue
    #
    # except TimeoutError:
    # print("TIME OUT ERROR!!!")
    # pass
    #
    # except requests.exceptions.ConnectTimeout:
    # print("requests.exceptions.ConnectTimeout")
    # pass
    # print("*** FINISH, THE TIME IT TOOK: ", datetime.now() - START_TIME, " ***")  ######
    # except WebDriverException:
    # driver = webdriver.Chrome(exe_path, options=options)
    # print("WEB DRIVER EXCEPTION!")
    # continue










    Full_Log_Dict[year] = {"................."}