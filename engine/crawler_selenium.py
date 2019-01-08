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
    processCount = 2

    ### SELENIUM Login pdwiki Test
    loginUrl = "http://pdwiki.skplanet.com/login.action"
    # driver = selLogin(loginUrl, '//*[@id="os_username"]', '********', '//*[@id="os_password"]', '********', '//*[@id="loginButton"]')

    drivers = []
    for count in range(0, processCount):
        drivers.append(selLogin(loginUrl, '//*[@id="os_username"]', '********', '//*[@id="os_password"]', '********', '//*[@id="loginButton"]'))

    keys = ["PDMS","INFRA2","INFRA","11oamerge",]
    # keys = ["PDMS","INFRA2","INFRA","11oamerge","DAS1","CTO","DA2D","ISMS","CLEAT","NBP","CTPFTGTDEV","ODR","PAD","proximitybi","OCBC","IntranetAPI","BenepiaSeoul2016","MS","Ticket","ABTEST","PDP","IMPAY","STDDEV","QA","code","PRMS2","QRDP","GCPB","GCP","SMF","SMC","PCW","LOG","pcrawler","BLIB","BGAll","intranetbo","DSH","intranetmng","PLABGUIDE","BIDATA","11LOG2DP","MLPF","ANLG","DEBI","PLANDAS","11stcorp","XL","11STDIC","hannahbi","SEARCHBI","DooraeImageSearch","GatheringImages",]
    detailurls = urlParse("http://pdwiki.skplanet.com/spaces/spacepermissions.action?key={key}", "{key}", keys)

    selectorDictList = [
        {
            'index': '어드민',
            'selector': '#aPermissionsTable > tbody > tr.space-permission-row > td:nth-child(2) > img',
            'filterAttr': 'src',
            'filterValue': '/s/en_GB/7109/fbbcac5a2a6382e2f6a78d491af75161a7840bc8/_/images/icons/emoticons/check.png',
            'attr': 'srcd'  ## . 갯수는 parent
            # 'attr': '.data-permission-user'  ## . 갯수는 parent
        },
        {
            'index': '스페이스명',
            'selector': '#rw_space_nav > div.rw_item_content.rw_has_favourite > a',
            'attr': 'title'  ## . 갯수는 parent
        },
    ]
    waitingForXpath = '//*[@id="uPermissionsTable"]/tbody/tr/td'

    rets = []

    # 한개로 돌릴때
    for url in detailurls:
        rets.append(selSinglePage(url, selectorDictList, driver=driver))

    return rets


if __name__ == "__main__":
    import time

    begin = time.time()

    result = main()
    df = pd.DataFrame(result)
    print(df)
    # toFile(df, 'wiki.csv')

    end = time.time()
    print("Eslapsed Time : {}".format(end - begin))

