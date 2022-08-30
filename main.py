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
filePath = '/home/ubuntu/pythonProject5/Json_Files/'
exe_path = '/home/ubuntu/pythonProject5/chromedriver'
DT_path = '/home/ubuntu/pythonProject5/DataFrames/'
exe_path = '/home/ubuntu/pythonProject5/chromedriver'
options = Options()

# Hide window
# options.add_argument('--disable-gpu')
# options.add_argument('--headless')

# PROXY
PROXY = "5.79.66.2:13081"
options.add_argument('--proxy-server=%s' % PROXY)

# main_data_frame = pd.read_csv('Cases_Name.csv',encoding = "ISO-8859-8")

start = "02-01-2013"  #
end = "01-02-2013"

all_dates = get_dates(start, end)

driver = webdriver.Chrome(exe_path, options=options)

for j in range(len(all_dates)):
    try:
        start = all_dates[j]
        end = all_dates[j + 1]
    except IndexError:
        break

    src = get_src(start, end)  # Current date's link

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
        print("Page is ready!")
    except TimeoutException:
        print("Loading took too much time! ID in the code not working!")

    try:
        Number = Get_Number_Of_Cases(driver)  # Returns the number of the cases of that date
        Cases = Get_Cases_Names(driver, Number)  # List of Case names
        df = pd.DataFrame(Cases, columns=[start])
        # df.join(main_data_frame)
        name = DT_path + 'Cases_Name ' + start + '.csv'
        df.to_csv(name, encoding="ISO-8859-8")

        URLS = Get_URLS(Cases)  # List of current date's links
        print(len(URLS))
        for i, CASE in enumerate(URLS):
            dec_df, LINK, conclusion, dict = Crawl_Decisions(CASE)  # Gets the button window
            if (len(dec_df) == 0): continue
            data = CrawlTopWindow(CASE, LINK, conclusion, dict, df[start][i])  # Gets the upper window
            if data == 0: continue
            json_name = start + "__" + str(i)

            writeToJsonFile(filePath, json_name, data)  # Write to Json file

    except NoSuchElementException:
        continue
    except UnexpectedAlertPresentException:
        continue
    except AttributeError:
        continue
    except UnboundLocalError:
        continue
    except TimeoutError:
        pass
    except requests.exceptions.ConnectTimeout:
        pass
    print("It took: ", datetime.now() - START_RUN_TIME, "for the ", (start), " with ", Number, " Cases")

END_RUN_TIME = datetime.now()
print("FINISH, THE TIME IT TOOK, from 04.01.22-01.02.2022: ", END_RUN_TIME - START_RUN_TIME)  ######
driver.close()
