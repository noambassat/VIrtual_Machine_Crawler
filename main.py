from datetime import datetime
import pandas as pd
from selenium import webdriver
import time
from CrawlUrls import get_src, Get_Cases_Names, Get_Number_Of_Cases, scroll_down, Get_URLS
from CrawlJSON import CrawlTopWindow, Crawl_Decisions
from Save_As_Json import writeToJsonFile
from Dates_Calculator import get_dates
from selenium.common.exceptions import InvalidSessionIdException,NoSuchElementException
from selenium.webdriver.chrome.options import Options
import warnings


START_RUN_TIME = datetime.now()
options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')



warnings.simplefilter(action='ignore', category=(FutureWarning, DeprecationWarning))


# PATH = open('C:/Users/Noam/Desktop/Courts Project/Paths.txt', 'r')
filePath = '/home/ubuntu/pythonProject5/Json_Files/'
exe_path = '/home/ubuntu/pythonProject5/chromedriver'
DT_path = '/home/ubuntu/pythonProject5/DataFrames/'

# main_data_frame = pd.read_csv('Cases_Name.csv',encoding = "ISO-8859-8")



start = "01-01-2010" #
end = "15-07-2022"

all_dates = get_dates(start,end)

for i in range(len(all_dates)):
    # main_data_frame = pd.read_csv('Cases_Name.csv', encoding="ISO-8859-8")
    try:
        start = all_dates[i]
        end = all_dates[i+1]
    except IndexError: break

    src = get_src(start, end)

    try:
        driver = webdriver.Chrome(executable_path=exe_path, chrome_options=options)
        driver.get(src)
    except InvalidSessionIdException:
        print("Couldn't get src:\n", src)
        driver.close()
        continue
    time.sleep(1)
    try:
        Number = Get_Number_Of_Cases(driver)
        Cases = Get_Cases_Names(driver,Number)
        df = pd.DataFrame(Cases, columns=[start])
        # df.join(main_data_frame)
        name = DT_path +'Cases_Name '+start+'.csv'
        df.to_csv(name,encoding = "ISO-8859-8")
        print(start)
        # print('  ... DataFrame: ... \n', df.head())

        driver.close()
        URLS = Get_URLS(Cases)
        print(Number)
        for i, CASE in enumerate(URLS):
            # try:
            dec_df, LINK, conclusion, dict = Crawl_Decisions(CASE)
            if(len(dec_df)==0):continue
            time.sleep(1)
            data = CrawlTopWindow(CASE, LINK, conclusion,dict,df[start][i])
            # except AttributeError:
            #     print(AttributeError)
            #     continue
            if data == 0: continue
            json_name = start + "__"+ str(i)

            writeToJsonFile(filePath, json_name, data)
    except NoSuchElementException:
        continue
END_RUN_TIME = datetime.now()
print("FINISH, THE TIME IT TOOK, from 04.01.22-01.02.2022: ",END_RUN_TIME-START_RUN_TIME)######


