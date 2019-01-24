import datetime, re
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import logging
import pandas as pd
from multiprocessing import Pool
from html_parser import *

## LOGGING setup
myLogger = logging.getLogger("my")
myLogger.setLevel(logging.INFO)
# stream_handler = logging.StreamHandler()
formatter = logging.Formatter('[%(levelname)s - %(asctime)s] %(message)s')
# stream_handler.setFormatter(formatter)
file_handler = logging.FileHandler('crawler.log')
file_handler.setFormatter(formatter)
# myLogger.addHandler(stream_handler)
myLogger.addHandler(file_handler)


### Chrome DRIVER 
CHROME_DRIVER = '/Users/1001078/Documents/workspace/Python/crawler/engine/chromedriver_mac'



# LoginData Sample
"""
    {
        'nameAttr_of_inputTag': 'value',
        'nameAttr_of_inputTag': 'value',
    },
"""
def selLogin(loginUrl, idXpath, id, pwdXpath, pwd, submitXpath):

    driver = webdriver.Chrome(CHROME_DRIVER)
    driver.implicitly_wait(3)

    driver.get(loginUrl)
    driver.find_element_by_xpath(idXpath).send_keys(id)
    driver.find_element_by_xpath(pwdXpath).send_keys(pwd)
    driver.find_element_by_xpath(submitXpath).click()

    return driver


def selNestedPage(url, selector, startAt=0, limit=-1, driver=None, waitingForXpath=None, delay=3, clickXpath=None):

    selectorDictList = [
        {
            'selector' : selector,
            'startAt': 1,
            'attr' : 'href',
            'startAt': startAt,
            'limit': limit
        },
    ]

    if driver is None :   
        driver = webdriver.Chrome(CHROME_DRIVER)
        driver.implicitly_wait(3)

    driver.get(url)
    
    if clickXpath:
        try:
            driver.find_element_by_xpath(clickXpath).click()
        except:
            print("Not clickable xpath")
            driver.close()

    if waitingForXpath:
        try:
            state = EC.presence_of_element_located((By.XPATH, waitingForXpath))
            WebDriverWait(driver, delay).until(state)
            print("Document is ready")
        except TimeoutException:
            print("Time out")
            driver.close()

    html = driver.page_source

    result = _parseHtml(html, selectorDictList)

    driver.close()
    
    links = result[selectorDictList[0].get('index', 'unknown')]    
    return _getFullPath(url, links)

def selAction(driver, xpathForClick, xpathForSendkeys=None, sendkeys=None, frameName=None, switchNewWindow=False):
    if frameName:
        driver.switch_to.frame(driver.find_element_by_name(frameName))

    try:
        state = EC.presence_of_element_located((By.XPATH, xpathForClick))
        WebDriverWait(driver, 3).until(state)
        print("Document is ready")
    except TimeoutException:
        print("Time out")
        driver.close()

    if sendkeys is not None:
        driver.find_element_by_xpath(xpathForSendkeys).clear()
        driver.find_element_by_xpath(xpathForSendkeys).send_keys(sendkeys)
    
    driver.find_element_by_xpath(xpathForClick).click()
    
    if switchNewWindow == True:
        WebDriverWait(driver, 10).until(lambda d: len(d.window_handles) == 2)
        driver.switch_to_window(driver.window_handles[1])

        # # wait to make sure the new window is loaded
        # WebDriverWait(driver, 10).until(lambda d: d.title != "")

    return driver

# selectorDictList Sample
"""
    {
        'index': 'index1',
        'selector' : "#div_content > div > div.list_title > a.list_subject > span.subject_fixed",
        'startAt': 0,
        'attr' : 'data-role',
        'limit' : 0,
        'filterAttr' : 'src',
        'filterValue' : 'value',
    },
"""
def selSinglePage(url, selectorDictList, driver=None, waitingForXpath=None, delay=3):

    if driver is None:
        driver = webdriver.Chrome(CHROME_DRIVER)
        driver.implicitly_wait(3)

    # if sessionDriver:
    #     cookies = sessionDriver.get_cookies()
    #     for cookie in cookies:
    #         driver.add_cookie(cookie)
    # else:
    #     session_url = sessionDriver.command_executor._url  
    #     session_id = sessionDriver.session_id
    #     driver = webdriver.Remote(command_executor=session_url,desired_capabilities={})
    #     driver.session_id = session_id  

    if url:
        try:
            driver.get(url)
        except Exception as ex:
            print(ex)

    if waitingForXpath:
        try:
            state = EC.presence_of_element_located((By.XPATH, waitingForXpath))
            WebDriverWait(driver, delay).until(state)
            print("Document is ready")
        except TimeoutException:
            print("Time out")

    html = driver.page_source

    result = parseHtml(html, selectorDictList)

    return result
    
 
def main():
    processCount = 1

    ### SELENIUM Login pdwiki Test
    loginUrl = "http://pnetsso.skplanet.com/login.asp"
    # driver = selLogin(loginUrl, '//*[@id="os_username"]', '********', '//*[@id="os_password"]', '********', '//*[@id="loginButton"]')

    drivers = []
    for count in range(0, processCount):
        drivers.append(selLogin(loginUrl, '//*[@id="txtUSER"]', '*******', '//*[@id="txtPASSWORD"]', '*******', '//*[@id="divPop"]/table/tbody/tr[6]/td/img[1]'))
    
    for driver in drivers:
        driver = selAction(driver, '//*[@id="lay_header"]/div/div/div[4]/a', switchNewWindow=True, frameName="fm_gnb")


    keys = ["amsong","psc","PP43911","PP40441","PP81961","PP48224","PP08821","1002587","PP48955","1002237","1000897","1001219","1002405","1001479","1003849","1003744","1001291","1001969","1002006","1000022","1002396","1003742","1002353","PP37852","1003870","PP78271","PP80091","1000641","1000108","1002878","1003887","1002966","PP81233","1001085","1004003","1001001","1002475","1003681","1000019","1000392","1002483","1001504","1002757","1002350","1002539","1003055","1000714","1003899","PP53292","PP71046","PP57384","PP60198","PP55156","PP53853","PP25221","PP02887","PP53615","PP02301","PP48842","9001001","PP77005","PP58071","PP77451","9001033","PP78223","1002383","1002982","1002354","1001920","1000273","1003291","1001946","1002218","1003436","1001078","1000504","1002181","1002318","1002516","1003642","1001210","1001740","1001416","1000301","1003475","1000851","1002723","PP55902","1001185","1002305","1000206"]
    
    selectorDictList = [
        {
            'index': '어드민',
            'selector': '#gvList_ctl02_btnName',
            # 'filterAttr': 'src',
            # 'filterValue': '/s/en_GB/7109/fbbcac5a2a6382e2f6a78d491af75161a7840bc8/_/images/icons/emoticons/check.png',
            # 'attr': 'srcd'  ## . 갯수는 parent
            # 'attr': '.data-permission-user'  ## . 갯수는 parent
        },
    ]
    # waitingForXpath = '//*[@id="uPermissionsTable"]/tbody/tr/td'

    rets = []

    for key in keys:
        driver = selAction(drivers[0], xpathForClick='//*[@id="ucSearchBox_btnSearch2"]', xpathForSendkeys='//*[@id="ucSearchBox_txtSearchText"]', sendkeys=key)
        time.sleep(0.5)
        rets.append(selSinglePage(None, selectorDictList, driver=driver))

    # 한개로 돌릴때
    # for url in detailurls:
    #     rets.append(selSinglePage(url, selectorDictList, driver=driver))

    driver.quit()

    return rets


if __name__ == "__main__":
    import time

    begin = time.time()

    result = main()
    df = pd.DataFrame(result)
    print(df)
    toFile(df, 'pdwiki_admin_list.csv')

    end = time.time()
    print("Eslapsed Time : {}".format(end - begin))

