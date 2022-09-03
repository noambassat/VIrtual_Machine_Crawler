from datetime import datetime
import pandas as pd
from selenium import webdriver
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

import warnings
from CrawlUrls import get_src, Get_Cases_Names, Get_Number_Of_Cases, scroll_down, Get_URLS
from CrawlJSON import CrawlTopWindow, Crawl_Decisions
from Save_As_Json import writeToJsonFile
from Dates_Calculator import get_dates
from selenium.common.exceptions import WebDriverException, InvalidSessionIdException, NoSuchElementException, \
    UnexpectedAlertPresentException
from selenium.webdriver.chrome.options import Options
import requests

warnings.simplefilter(action='ignore', category=(FutureWarning, DeprecationWarning))
START_RUN_TIME = datetime.now()

# PATH = open('C:/Users/Noam/Desktop/Courts Project/Paths.txt', 'r')
filePath = '/home/ubuntu/PycharmProjects/pythonProject5/Json_Files/'
# exe_path = '/home/ubuntu/pythonProject5/chromedriver'
DT_path = '/home/ubuntu/PycharmProjects/pythonProject5/DataFrames/'
exe_path = '/home/ubuntu/PycharmProjects/pythonProject5/chromedriver'
options = Options()

# Hide window
# options.add_argument('--disable-gpu')
# options.add_argument('--headless')

# PROXY
PROXY = "5.79.66.2:13081"
options.add_argument('--proxy-server=%s' % PROXY)

# main_data_frame = pd.read_csv('Cases_Name.csv',encoding = "ISO-8859-8")

start = "01-01-2010"  #
end = "01-02-2010"
YEAR = 2010
driver = webdriver.Chrome(exe_path, options=options)
while (YEAR < 2023):
    start = start[:6] + str(YEAR)
    end = end[:6] + str(YEAR)
    YEAR = int(start[6:]) + 1
    print(YEAR - 1)
    all_dates = get_dates(start, end)



    for j in range(len(all_dates)):
        START_TIME = datetime.now()
        try:
            start = all_dates[j]
            end = all_dates[j + 1]
        except IndexError:
            break

        src = get_src(start, end)  # Current date link

        try:
            driver.get(src)
        except InvalidSessionIdException:
            print("Couldn't get src:\n", src)
            driver.close()
            driver = webdriver.Chrome(exe_path, options=options)
            continue
        except WebDriverException as wde:
            print(str(wde))
            print("-----")
            print(wde.args)
            print(src)
            print("trying once again.....")
            driver.close()
            driver = webdriver.Chrome(exe_path, options=options)
            try:
                driver.get(src)
            except WebDriverException as wde:
                print(str(wde))
                print("-----")
                print(wde.args)
                print(src)
            continue

        # At least 2 secs must be waiting in order to load the webpage
        delay = 5  # seconds
        try:
            myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, 'row_0')))
        except TimeoutException:
            print("Loading took too much time")
            print("Trying once again ...")
            try:
                myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, 'row_0')))
            except TimeoutException:
                print("Loading took too much time! ID in the code not working!")

        try:
            time.sleep(1)
            Number = Get_Number_Of_Cases(driver)  # All the cases that appeared that date
            Cases = Get_Cases_Names(driver, Number)  # List of Case names
            df = pd.DataFrame(Cases, columns=[start])
            # df.join(main_data_frame)
            name = DT_path + 'Cases_Name ' + start + '.csv'
            df.to_csv(name, encoding="ISO-8859-8")

            URLS = Get_URLS(Cases)  # List of current date's links
            print("Number of cases: ",len(URLS))
            for i, CASE in enumerate(URLS):
                try:
                    dec_df, LINK, conclusion, dict = Crawl_Decisions(driver, CASE)  # Gets the button window

                    if (len(dec_df) == 0):
                        dec_df, LINK, conclusion, dict = Crawl_Decisions(driver, CASE)
                        if (len(dec_df) == 0):
                            print("0 DEC!!!\n", CASE)
                            continue
                    print("The len of decisions table: ", len(dec_df))
                    time.sleep(1)
                    ###### PROBLAM IN HERE
                    data = CrawlTopWindow(CASE, LINK, conclusion, dict, df[start][i])  # Gets the upper window
                    #######
                    if data == 0:
                        print("Data Error! check the CrawlTopWindow from CrawlJSON file")
                        continue
                except OSError:
                    i -= 1
                    CASE = URLS[i]
                    ("OS Error, continue")
                    continue
                except UnexpectedAlertPresentException:
                    i -= 1
                    CASE = URLS[i]
                    ("UnexpectedAlertPresentException, continue")
                    continue
                json_name = start + "__" + str(i)
                writeToJsonFile(filePath, json_name, data)  # Write to Json file
                print("--done saving to json--")
        except NoSuchElementException:
            print(NoSuchElementException)

            continue

        except UnexpectedAlertPresentException:

            print(UnexpectedAlertPresentException)

            continue

        except AttributeError:

            print(AttributeError.args)

            continue

        except UnboundLocalError:

            print(UnboundLocalError)

            continue

        except TimeoutError:

            pass

        except requests.exceptions.ConnectTimeout:

            pass
        print("*** FINISH, THE TIME IT TOOK: ", datetime.now() - START_TIME," ***")  ######
    END_RUN_TIME = datetime.now()
    print("FINISH, THE TIME IT TOOK: ", END_RUN_TIME - START_RUN_TIME)  ######
driver.close()
