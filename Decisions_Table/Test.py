

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

CHROMEDRIVER_PATH  = '/home/ubuntu/PycharmProjects/pythonProject5/chromedriver'

URL = "https://api.webscrapingapi.com/v1/?api_key=qWLe3iMqS89nggeKenmcQHoI5o34uZuR"

options = Options()
options.headless = True
driver = webdriver.Chrome(CHROMEDRIVER_PATH, options=options)

driver.get(URL)

