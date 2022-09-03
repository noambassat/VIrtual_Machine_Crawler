from bs4 import BeautifulSoup
import datetime

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
        inner_SCROLL = driver.find_element('xpath',XPATH)
        location = inner_SCROLL.location_once_scrolled_into_view
        Counter +=100
    return driver


def Get_Cases_Names(driver,Number_Of_Cases):

    # elements = driver.find_elements_by_class_name('ng-scope')
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    soup = soup.findAll('a', {'title': 'הצג תיק'})
    stop = 0

    while(len(soup)!=Number_Of_Cases and stop!=50):
        driver = scroll_down(driver, Number_Of_Cases)
        # elements = driver.find_elements_by_class_name('ng-scope')

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        soup = soup.findAll('a', {'title': 'הצג תיק'})
        stop+=1
    return [s.text for s in soup]


def Get_URLS(Cases):
    URLS = []
    for case in Cases:

        for word in case.split():
            if(word.find('/') == -1): continue
            case = word[:word.find('/')]
            year = '20' + word[word.find('/')+1:]
            curr_year = str(datetime.date.today().year)[2:]

            if(int(word[word.find('/')+1:])>int(curr_year)): year = '19' +  word[word.find('/')+1:]
            # 2022/3635   #######################################

            url = "https://supremedecisions.court.gov.il/Verdicts/Results/1/null/" \
                  +year+ "/"\
                        +case+"/null/null/null/null/null"
            URLS.append(url)
    return URLS
