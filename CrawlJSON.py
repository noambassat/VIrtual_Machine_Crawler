from Save_As_Json import writeToJsonFile
from selenium import webdriver
from bs4 import BeautifulSoup
import requests

CASE = "https://supremedecisions.court.gov.il/Verdicts/Results/1/null/2022/3635/null/null/null/null/null"
driver = webdriver.Chrome(executable_path='C:/Users/Noam/Desktop/Courts Project/chromedriver.exe')
driver.get(CASE)

response = requests.get(CASE)
# data = response.json()

SOUP = BeautifulSoup(driver.page_source, 'html.parser')
src = SOUP.findAll('iframe')[1]
try:
    src =src['ng-src']
    driver.get(src)  # Top window info
except KeyError: pass
soup = BeautifulSoup(driver.page_source, 'html.parser')
labels = soup.findAll("span",{"class":"caseDetails-label"})
details = soup.findAll("span",{"class":"caseDetails-info"})

# xpath = '/html/body/div[1]/div[1]/div/div/div[2]/a'


for t in soup.findAll('td'):
    # labels.append(t['data-label'])
    # details.append(t.text)
    try:
        labels.append(t['data-label'].replace('\t',''))
        details.append(t.text.replace('\t',''))
    except KeyError: pass

data = {}
for i in range(len(labels)):
    try:
        labels[i] = labels[i].text
        details[i] = details[i].text
    except AttributeError: pass
    data[labels[i]] = details[i]

for i,d in enumerate(data):
    print(d, ": ",data[d])


writeToJsonFile('TEST',data)