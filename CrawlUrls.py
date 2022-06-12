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


def get_src(start_date, end_date): return 'https://supremedecisions.court.gov.il/Verdicts/Results/1/null/null/null/2/null/' + start_date.replace('/','-') + '/' + end_date.replace('/','-') + '/null'

src = get_src('30/05/2022', '31/05/2022')

driver.get(src)


time.sleep(1)


def Get_Number_Of_Cases():
    return 204

Number = Get_Number_Of_Cases()



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
Cases = []
for s in soup: Cases.append(s.text)
print(Cases)


