import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import main



def get_src(start_date, end_date): return 'https://supremedecisions.court.gov.il/Verdicts/Results/1/null/null/null/2/null/' + start_date.replace('/','-') + '/' + end_date.replace('/','-') + '/null'

def Get_Number_Of_Cases(driver):
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    txt = soup.find('p', {'class': 'ng-binding'}).text
    return [int(s) for s in txt.split() if s.isdigit()][0]



def scroll_down(driver, Number_Of_Cases):
    driver.maximize_window()  # For maximizing window
    driver.implicitly_wait(5)  # gives an implicit wait for 5 seconds
    Counter = 99
    while(Number_Of_Cases>Counter):
        XPATH = '//*[@id="row_' + str(Counter) + '"]'
        inner_SCROLL = driver.find_element_by_xpath(XPATH)
        location = inner_SCROLL.location_once_scrolled_into_view
        Counter +=100


def Get_Cases_Names(driver,):

    elements = driver.find_elements_by_class_name('ng-scope')


    soup = BeautifulSoup(driver.page_source, 'html.parser')
    soup = soup.findAll('a', {'title': 'הצג תיק'})

    print(len(soup) , " Cases were found!")
    return [s.text for s in soup]


def Get_URLS(Cases):
    for case in Cases:
        for word in case.split(): print(word)
    return []

Get_URLS(['רע"א 3484/22','ע"א 3339/22'])

###################################################################################################

#
#
# driver = webdriver.Chrome(executable_path='C:/Users/Noam/Desktop/Courts Project/chromedriver.exe')
#
# start = '30/05/2022'
# end =  '31/05/2022'
# src = get_src(start, end)
#
# driver.get(src)
#
# time.sleep(1)
#
# Number = Get_Number_Of_Cases()
# scroll_down(Number)
# Cases = Get_Cases_Names()
#
# df =pd.DataFrame(Cases,columns=[start])
# df.to_csv('Cases_Name.csv')
# print(df.head())