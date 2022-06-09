import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains # FOR DOUBLE CLICK
import time
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
    #
    # scrollable_element = driverf.find_element_by_class_name("results-listing")


    # SCROLL_PAUSE_TIME = 0.5
    #
    # # Get scroll height
    # tlast_height = driverf.execute_script("return document.body.scrollHeight")
    #     #
    #     # while True:
    #     #     # Scroll down to bottom
    #     #     driverf.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    #     #
    #     #     # Wai to load page
    #     time.sleep(SCROLL_PAUSE_TIME)
    #
    #     # Calculate new scroll height and compare with last scroll height
    #     new_height = driverf.execute_script("return document.body.scrollHeight")
    #     if new_height == last_height:
    #         break
    #     last_height = new_height
    #


    elements = driver.find_elements_by_class_name('ng-scope')
    scroll = driver.find_element_by_class_name("results-listing")
    actions = ActionChains(driver)
    actions.move_to_element(scroll).perform()

    for element in elements:
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        soup = soup.findAll('a',{'title':'הצג תיק'})


        print(len(soup))


        # for i, s in enumerate(soup): print(i, ":   ", s)


get_urls(driver, '30/05/2022','31/05/2022')