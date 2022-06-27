import pandas as pd
from selenium import webdriver
import time
from CrawlUrls import get_src, Get_Cases_Names, Get_Number_Of_Cases, scroll_down, Get_URLS
from CrawlJSON import CrawlTopWindow, Crawl_Decisions
from Save_As_Json import writeToJsonFile

# PATH = open('C:/Users/Noam/Desktop/Courts Project/Paths.txt', 'r')
# filePath = 'C:/Users/Noam/PycharmProjects/pythonProject5/Json_Files/'
# print(str(PATH)[str(PATH).find('JSON:') + 1:])
# driver = webdriver.Chrome(executable_path='C:/Users/Noam/Desktop/Courts Project/chromedriver.exe')
#
# start = '30/05/2022'
# end = '31/05/2022'
# src = get_src(start, end)
#
# driver.get(src)
#
# time.sleep(1)
#
# Number = Get_Number_Of_Cases(driver)
# scroll_down(driver, Number)
# Cases = Get_Cases_Names(driver)
#
# df = pd.DataFrame(Cases, columns=[start])
#
# df.to_csv('Cases_Name.csv')
#
# print('  ... DataFrame: ... \n', df.head())
#
# driver.close()
# URLS = Get_URLS(Cases, start, end)
# for i, CASE in enumerate(URLS):
#     print(Cases[i], ': ', CASE)
#
#     dec_df, n_of_Decisions, LINK, conclusion = Crawl_Decisions(CASE)
#     data = CrawlTopWindow(CASE, n_of_Decisions, LINK, conclusion)
#     if data == 0: continue
#     json_name = Cases[i].replace("/", '_').replace('"', '').replace(' ', '') + "__" + start.replace("/", '_')
#
#     writeToJsonFile(filePath, json_name, data)
#     if (i == 5): break
#
# #
#
# #
# #
CASE = "https://supremedecisions.court.gov.il/Verdicts/Results/1/null/2014/8568/null/null/null/null/null"
#
private_CASE = "https://supremedecisions.court.gov.il/Verdicts/Results/1/null/2022/3654/null/null/null/null/null"

dec_df, n_of_Decisions,LINK,conclusion  = Crawl_Decisions(CASE)

#
# print_dataframe(dec_df,320,10)
#
data = CrawlTopWindow(CASE, n_of_Decisions, LINK ,conclusion)
if data != 0:
    filePath = 'C:/Users/Noam/PycharmProjects/pythonProject5/Json_Files/'
    writeToJsonFile(filePath, 'TEST', data)
#

# #  איך לקרוא לשמות של הג'יסון ?
# איך לעשות שפסק-דין \ החלטה אחרונה חדשה בתיק קיים תדרוס את הישן?