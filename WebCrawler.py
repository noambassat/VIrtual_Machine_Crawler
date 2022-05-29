import datetime
import time

import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains # FOR DOUBLE CLICK
import datetime as dt
import requests
import json
from selenium.webdriver.common.by import By
from lxml import etree
from urllib.request import urlopen
from datetime import timedelta

# iterate days

start_date = datetime.date(2022, 1, 1)
end_date = start_date + timedelta(days=1)
stop = datetime.date(2022, 1, 3)
single_date = start_date
while single_date != stop:
    end_date = single_date + timedelta(days=1)
    print("start: ", single_date, "end : ", end_date)
    single_date += timedelta(days=1)
print()
def date_to_string(date):
    return str(date.day) + '/' + str(date.month) + '/' + str(date.year)
driver = webdriver.Chrome(executable_path='C:/Users/Noam/Desktop/Courts Project/chromedriver.exe')
driver.get("https://supreme.court.gov.il/Pages/HomePage.aspx")
time.sleep(2)
driver.find_element_by_xpath("/html/body/form/div[3]/div[1]/div/header/div[2]/div/div[2]/div/div[2]/a[5]/span").click()
time.sleep(1)

select = Select(driver.find_element(by = By.XPATH, value = '//select[@title="טווח זמנים"]'))
select.select_by_index(7)
#start date
driver.find_element_by_xpath('/html/body/form/div[3]/div[3]/div/div/form/div/div/div[2]/div[5]/div[2]/div/div/input').send_keys(date_to_string(single_date))
#end date
driver.find_element_by_xpath('/html/body/form/div[3]/div[3]/div/div/form/div/div/div[2]/div[5]/div[3]/div/div/input').send_keys(date_to_string(end_date))
# search
driver.find_element_by_xpath('/html/body/form/div[3]/div[3]/div/div/form/div/div/div[2]/div[7]/div[2]/button').click()
time.sleep(3)

#


# soup = BeautifulSoup(driver.page_source, 'html.parser')
# print(soup)

# driver.quit()