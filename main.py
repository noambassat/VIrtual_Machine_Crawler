import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import main

import CrawlUrls
from CrawlUrls import get_src, Get_Cases_Names, Get_Number_Of_Cases, scroll_down


driver = webdriver.Chrome(executable_path='C:/Users/Noam/Desktop/Courts Project/chromedriver.exe')

start = '30/05/2022'
end =  '31/05/2022'
src = get_src(start, end)

driver.get(src)

time.sleep(1)

Number = Get_Number_Of_Cases(driver)
scroll_down(driver, Number)
Cases = Get_Cases_Names(driver)

df =pd.DataFrame(Cases,columns=[start])
df.to_csv('Cases_Name.csv')
print(df.head())

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
