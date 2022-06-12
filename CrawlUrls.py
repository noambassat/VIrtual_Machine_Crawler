import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains # FOR DOUBLE CLICK
import time
import numpy as np
from lxml import html
import requests
# import urllib2
from selenium.webdriver.common.keys import Keys
###
import re

# TO DO LIST

# location_once_scrolled_into_view

# GET SRC


URLS = pd.DataFrame(columns=['URL'])
driver = webdriver.Chrome(executable_path='C:/Users/Noam/Desktop/Courts Project/chromedriver.exe')
# driver.get("https://supreme.court.gov.il/Pages/SearchJudgments.aspx?&OpenYearDate=null&CaseNumber=null&DateType=2&SearchPeriod=null&COpenDate=30/05/2022&CEndDate=31/05/2022&freeText=null&Importance=null")



def get_urls(driver, start_date, end_date):
    CaseNUMBER = '3339'
    YEAR = start_date[-4:]
    URL = "https://supreme.court.gov.il/Pages/SearchJudgments.aspx?&OpenYearDate=" \
          + YEAR +\
          '&CaseNumber='\
          + CaseNUMBER +\
          "&DateType=2&SearchPeriod=null&COpenDate=30/05/2022&CEndDate=31/05/2022&freeText=null&Importance=null"

    # soup = BeautifulSoup(driver.page_source, 'html.parser')
    # #ng-scope active
    # #//*[@id="row_0"]/div[2]/a
    # card = soup.find("div",{"class":"Layout-HomePage"}).find(
    #     "div",{"id":"MSOZoneCell_WebPartWPQ2"}).find(
    #     "div",{"class":"ms-webpart-chrome ms-webpart-chrome-vertical ms-webpart-chrome-fullWidth"}).find(
    #     "div",{"id":"ctl00_ctl40_g_664c5230_fd36_4083_9f79_25d174af43f8"}).find(
    #     "div",{"elad_wpid":"ctl00$ctl40$g_664c5230_fd36_4083_9f79_25d174af43f8"}).find("iframe",{"id":"serviceFram"})
    # src = card['src']
    src1 = "https://supremedecisions.court.gov.il/Verdicts/Results/1/null/null/null/2/null/30-05-2022/31-05-2022/null"

    src = 'https://supremedecisions.court.gov.il/Verdicts/Results/1/null/null/null/2/null/' + start_date.replace('/','-') + '/' + end_date.replace('/','-') + '/null'
    driver.get(src)


    time.sleep(10)


    Number = 204
    def scroll_down(Number_Of_Cases):
        driver.maximize_window()  # For maximizing window
        driver.implicitly_wait(5)  # gives an implicit wait for 5 seconds
        Counter = 99
        while(Number_Of_Cases>Counter):
            XPATH = '//*[@id="row_' + str(Counter) + '"]'

            inner_SCROLL = driver.find_element_by_xpath(XPATH)
            location = inner_SCROLL.location_once_scrolled_into_view
            Counter +=100


    scroll_down(Number)
    elements = driver.find_elements_by_class_name('ng-scope')


    soup = BeautifulSoup(driver.page_source, 'html.parser')
    soup = soup.findAll('a', {'title': 'הצג תיק'})

    print(len(soup) , " Cases were found!")
    print((type(soup[0].title)))
    #
    # for element in elements:
    #     soup = BeautifulSoup(driver.page_source, 'html.parser')
    #     soup = soup.findAll('a',{'title':'הצג תיק'})
    #
    #
    #     # print(len(soup))


        # for i, s in enumerate(soup): print(i, ":   ", s)


get_urls(driver, '30/05/2022','31/05/2022')