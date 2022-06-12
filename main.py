import pandas as pd
from selenium import webdriver
import time
from CrawlUrls import get_src, Get_Cases_Names, Get_Number_Of_Cases, scroll_down, Get_URLS


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


URLS = Get_URLS(Cases,start,end)
for i,url in enumerate(URLS): print(Cases[i],': ', url)


