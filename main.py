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

START_RUN_TIME = datetime.now()
options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')  # Last I checked this was necessary.


import warnings
warnings.simplefilter(action='ignore', category=(FutureWarning, DeprecationWarning))


PATH = open('C:/Users/Noam/Desktop/Courts Project/Paths.txt', 'r')
filePath = 'C:/Users/Noam/PycharmProjects/pythonProject5/Json_Files/'
exe_path = 'C:/Users/Noam/Desktop/Courts Project/chromedriver.exe'

# main_data_frame = pd.read_csv('Cases_Name.csv',encoding = "ISO-8859-8")




start = "01-01-2022"
end = "01-02-2022"

all_dates = get_dates(start,end)
print(all_dates)
for i in range(len(all_dates)):
    # main_data_frame = pd.read_csv('Cases_Name.csv', encoding="ISO-8859-8")
    try:
        start = all_dates[i]
        end = all_dates[i+1]
    except IndexError: break

    src = get_src(start, end)
    driver = webdriver.Chrome(executable_path=exe_path,chrome_options=options)

    try:
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
        name = 'DataFrames/Cases_Name '+start+'.csv'
        df.to_csv(name,encoding = "ISO-8859-8")

        # print('  ... DataFrame: ... \n', df.head())

        driver.close()
        URLS = Get_URLS(Cases, start, end)
        for i, CASE in enumerate(URLS):
            # try:
            dec_df, n_of_Decisions, LINK, conclusion, dict = Crawl_Decisions(CASE)
            data = CrawlTopWindow(CASE, n_of_Decisions, LINK, conclusion,dict)
            # except AttributeError:
            #     print(AttributeError)
            #     continue
            if data == 0: continue
            json_name = start + "__"+ str(i)

            writeToJsonFile(filePath, json_name, data)
    except NoSuchElementException:
        continue
END_RUN_TIME = datetime.now()
print("FINISH, THE TIME IT TOOK: ",END_RUN_TIME-START_RUN_TIME)
# CASE = "https://supremedecisions.court.gov.il/Verdicts/Results/1/null/2014/8568/null/null/null/null/null"
# #
# private_CASE = "https://supremedecisions.court.gov.il/Verdicts/Results/1/null/2022/3654/null/null/null/null/null"
#
# dec_df, n_of_Decisions,LINK,conclusion  = Crawl_Decisions(CASE)
#
# #
# # print_dataframe(dec_df,320,10)
# #
# data = CrawlTopWindow(CASE, n_of_Decisions, LINK ,conclusion)
# if data != 0:
#     filePath = 'C:/Users/Noam/PycharmProjects/pythonProject5/Json_Files/'
#     writeToJsonFile(filePath, 'TEST', data)

#





# להחזיר את ימי שבת v
# מסמך תיעוד!
# לייצר וליבא קובץ עם כל הPATH קובץ
# לעשות רימוט למחשב מרוחק ולעשות קרולינג להכל
# לבדוק בכמה מהמסמכים יש 2 תיקים
# להוסיף שנה בטבלת הקישורים v
# להוסיף את כל המסמכים לJSON V
# מדגם של שבוע מכל שנה 1-8 לינואר מ2010
# להוסיף לכל ג'ייסון את טבלת קישורי ההחלטות V
# להוסיף את התיקים החסויים !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# לבדוק תיק דלמטה בJSON
# להריץ על חודש לשלוח גייסון ליהונתן ואיילת
# HANDLESS CHROME
# DISABLE PYTHON WARNING




########################


# בדקתי ריצה עבור 10 ימים 3 קייסים ביום
# ההרכיה בגייסון
# הוספתי בדיקה של תיק חסוי - במקרה זה התיק לא נכנס לקבצי הג'ייסון
# בדיקה של ימי שבת
# שמות הגייסון מורכבים מתאריך וממספר סידורי


####################################


# # איך מוחקים את האזהרות?
# # firefox
# לוודא שפסק-דין \ החלטה אחרונה חדשה בתיק קיים תדרוס את הישן?
# מקרה של קייס חסוי, מה לעשות ?