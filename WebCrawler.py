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


start_date = '21/05/2022'
end_date = '22/05/2022'

driver = webdriver.Chrome(executable_path='C:/Users/Noam/Desktop/Courts Project/chromedriver.exe')
driver.get("https://www.supreme.court.gov.il/Pages/HomePage.aspx")
driver.find_element_by_xpath("/html/body/form/div[3]/div[1]/div/header/div[2]/div/div[2]/div/div[2]/a[5]/span").click()
time.sleep(1)

select = Select(driver.find_element(by = By.XPATH, value = '//select[@title="טווח זמנים"]'))
select.select_by_index(7)
#start date
driver.find_element_by_xpath('/html/body/form/div[3]/div[3]/div/div/form/div/div/div[2]/div[5]/div[2]/div/div/input').send_keys(start_date)
#end date
driver.find_element_by_xpath('/html/body/form/div[3]/div[3]/div/div/form/div/div/div[2]/div[5]/div[3]/div/div/input').send_keys(end_date)
# search
driver.find_element_by_xpath('/html/body/form/div[3]/div[3]/div/div/form/div/div/div[2]/div[7]/div[2]/button').click()
time.sleep(3)

#


# soup = BeautifulSoup(driver.page_source, 'html.parser')
# print(soup)

# driver.quit()