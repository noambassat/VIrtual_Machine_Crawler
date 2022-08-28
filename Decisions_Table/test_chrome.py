
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
import warnings

options = Options()

options.add_argument('--disable-gpu')
options.add_argument('--headless')
exe_path = '/home/ubuntu/pythonProject5/chromedriver'
PROXY = "5.79.66.2:13080"

options.add_argument('--proxy-server=%s' % PROXY)
driver = webdriver.Chrome(executable_path=exe_path, chrome_options=options)
driver.get("https://www.google.com")
driver.get("https://supreme.court.gov.il/Pages/fullsearch.aspx")
