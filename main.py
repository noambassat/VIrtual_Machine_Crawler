from datetime import datetime
import pandas as pd
from selenium import webdriver
import time
import warnings
from CrawlUrls import get_src, Get_Cases_Names, Get_Number_Of_Cases, scroll_down, Get_URLS
from CrawlJSON import CrawlTopWindow, Crawl_Decisions
from Save_As_Json import writeToJsonFile
from Dates_Calculator import get_dates
from selenium.common.exceptions import WebDriverException, InvalidSessionIdException,NoSuchElementException, UnexpectedAlertPresentException
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


options = Options()

options.add_argument('--disable-gpu')
options.add_argument('--headless')

PROXY = "5.79.66.2:13081"


# main_data_frame = pd.read_csv('Cases_Name.csv',encoding = "ISO-8859-8")


#### 05-03-2010  with  8  Cases ####

start = "01-01-2013" #
end = "15-07-2022"

all_dates = get_dates(start,end)

for j in range(len(all_dates)):
    # main_data_frame = pd.read_csv('Cases_Name.csv', encoding="ISO-8859-8")
    try:
        start = all_dates[j]
        end = all_dates[j+1]
    except IndexError: break

    src = get_src(start, end)

    try:
        driver = webdriver.Chrome(executable_path=exe_path, chrome_options=options)
        driver.get(src)
    except InvalidSessionIdException:
        print("Couldn't get src:\n", src)
        driver.close()
        continue
    except WebDriverException:
        print(str(wde))
        print("-----")
        print(wde.args)
        print(src)
        print("trying once again.....")
        driver.close()
        try:
            driver = webdriver.Chrome(executable_path=exe_path, chrome_options=options)
            driver.get(src)
        except WebDriverException as wde:
            print(str(wde))
            print("-----")
            print(wde.args)
            print(src)
        continue
    time.sleep(2)
    try:
        Number = Get_Number_Of_Cases(driver)
        Cases = Get_Cases_Names(driver)
        df = pd.DataFrame(Cases, columns=[start])
        # df.join(main_data_frame)
        name = DT_path +'Cases_Name '+start+'.csv'
        df.to_csv(name,encoding = "ISO-8859-8")

        driver.close()
        URLS = Get_URLS(Cases)
        print(len(URLS))
        for i, CASE in enumerate(URLS):
            dec_df, LINK, conclusion, dict = Crawl_Decisions(CASE)
            if(len(dec_df)==0):continue
            time.sleep(1)
            data = CrawlTopWindow(CASE, LINK, conclusion,dict,df[start][i])
            if data == 0: continue
            json_name = start + "__"+ str(i)

            writeToJsonFile(filePath, json_name, data)
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
    print("It took: ", datetime.now()-START_RUN_TIME,"for the ",(start), " with ", Number, " Cases")

    driver.close()
END_RUN_TIME = datetime.now()
print("FINISH, THE TIME IT TOOK, from 04.01.22-01.02.2022: ",END_RUN_TIME-START_RUN_TIME)######
