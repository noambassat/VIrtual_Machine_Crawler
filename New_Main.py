from datetime import datetime
import pandas as pd
import time
import warnings
# from CrawlUrls import get_src, Get_Cases_Names, Get_Number_Of_Cases, scroll_down, Get_URLS
# from CrawlJSON import CrawlTopWindow, Crawl_Decisions, run
# from Save_As_Json import writeToJsonFile
# from Dates_Calculator import get_dates
import requests
# !/usr/bin/env python3 # -*- coding: utf-8 -*-

warnings.simplefilter(action='ignore', category=(FutureWarning, DeprecationWarning))
START_RUN_TIME = datetime.now()

# Paths
filePath = '/home/ubuntu/PycharmProjects/pythonProject5/Json_Files/'
DT_path = '/home/ubuntu/PycharmProjects/pythonProject5/DataFrames/'
exe_path = '/home/ubuntu/PycharmProjects/pythonProject5/chromedriver'

START_TIME = datetime.now()

Log_DF = pd.DataFrame()
Full_Log_Dict = {}
Logs_list = []
Years_and_Nums = {2011:9775} # { year_num : num_of_cases }

for year in Years_and_Nums.keys(): # CURR -> 2011 ONLY
    Counter= 1  # The Continuous number of each year
    STOP = 0
    while(Counter<Years_and_Nums[year] and STOP < 5): # While the crawler didn't reach the case's limit number yet. 5 is the max errors that can be thrown.
        curr_case = {"Case number": "%d %d" % (Counter, year)}


        Logs_list.append(curr_case)














    Full_Log_Dict[year] = {"................."}