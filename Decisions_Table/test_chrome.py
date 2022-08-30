
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import warnings


options = Options()

options.add_argument('--disable-gpu')
#options.add_argument('--headless')
exe_path = '/home/ubuntu/pythonProject5/chromedriver'
PROXY = "5.79.66.2:13080"


# firefox_capabilities = webdriver.DesiredCapabilities.FIREFOX
# firefox_capabilities['marionette'] = True


# firefox_capabilities['proxy'] = {
#     "proxyType": "MANUAL",
#     "httpProxy": proxy,
#     "sslProxy": proxy
# }

options.add_argument('--proxy-server=%s' % PROXY)
driver = webdriver.Chrome(executable_path=exe_path, chrome_options=options)

driver.get("https:/google.com")
driver.get("https://supreme.court.gov.il/Pages/fullsearch.aspx")
driver.get("https://supremedecisions.court.gov.il/Verdicts/Results/1/null/null/null/2/null/01-01-2013/02-01-2013/null")

driver.close()
