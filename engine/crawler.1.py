import sys
import datetime, re
import django
from django.utils import timezone
django.setup()

import requests
from multiprocessing import Process
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.alert import Alert
from .models import *
import logging

## LOGGING setup
myLogger = logging.getLogger("my")
myLogger.setLevel(logging.INFO)
stream_handler = logging.StreamHandler()
formatter = logging.Formatter('[%(levelname)s - %(asctime)s] %(message)s')
stream_handler.setFormatter(formatter)
file_handler = logging.FileHandler('crawler.log')
file_handler.setFormatter(formatter)
myLogger.addHandler(stream_handler)
myLogger.addHandler(file_handler)

def getLastPage(site, soup):
    try: 
        lastPage = soup.select_one(site.recentPageSelector.replace('child', 'of-type'))['href']
        lastPageId = int(re.search(site.recentPageRegex, lastPage).group())
        return lastPageId
    except Exception as ex:
        myLogger.error("Last Page Selector Error : {}".format(ex))
        return 0

def extractMagnet(site, task, soup, category, pageId, dateTime):

    try:
        title = soup.select_one(site.titleSelector.replace('child', 'of-type')).getText().strip()
        magnet = soup.select_one(site.magnetSelector.replace('child', 'of-type'))[site.magnetAttribute]
        magnet = magnet.replace("(","").replace(")","").replace("\'","").replace(";","")        # 특수문자 제거
        magnet = magnet.replace("magnet_link", "magnet:?xt=urn:btih:")          # 스크립트 코드인 경우
        
        myLogger.info("{}({}) -> {} / {}".format(pageId, category, title, magnet))
        
        # SAVE
        magnet = Magnet(magnet = magnet, title = title, sourceDomain = site.sitename, updateDate = dateTime)
        magnet.save()
    except Exception as ex:
        myLogger.error("EXCEPTION : {} ({} - {} - {})".format(ex, site.sitename, category, pageId))
    
    # Task DB update
    task.currentPageId = pageId
    task.updateDate = dateTime
    task.save()

def crawlSingleCategory(site, category):
    startDt = timezone.localtime()
    myLogger.info("=========================")
    myLogger.info(" START AT for {} : {}".format(category, startDt))
    myLogger.info("=========================")

    if site.method == "selenium":
        # For SERVER
        # chrome_options = Options()
        # chrome_options.add_argument('--headless')
        # chrome_options.add_argument('--no-sandbox')
        # chrome_options.add_argument('--disable-dev-shm-usage')
        # driver = webdriver.Chrome('/home/junhyuk_jin/workspace/toy/toy/chromedriver_linux64', chrome_options=chrome_options)

        # For Local
        driver = webdriver.Chrome(r'C:\workspace\Python\toy\toy\chromedriver.exe')
        driver.implicitly_wait(3)
        
        task = Task.objects.filter(sitename = site.sitename, category = category).last()
        if task is None:
            task = Task.objects.create(sitename = site.sitename, category = category, currentPageId = 1, startPageId = 0, updateDate = timezone.localtime())

        # Last page 구하기
        driver.get(site.categoryListPage)
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        lastPageId = getLastPage(site, soup)
        myLogger.info("LAST Page of {} - {} : {}".format(site.sitename, category, lastPageId))

        for pageId in range(task.currentPageId, lastPageId + 1):
            driver.get(site.detailPageUrl.replace("{category}", category).replace("{page}", str(pageId)))
            
            try: 
                alert = Alert(driver)
                alert.dismiss()
            except:
                a = 1  ## 아무것도 안하게 못하나.. 

            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
            dateTime = datetime.datetime.now(tz=timezone.utc)

            extractMagnet(site, task, soup, category, pageId, dateTime)
 
        driver.close()
    
    else:
        task = Task.objects.filter(sitename = site.sitename, category = category).last()
        if task is None:
            task = Task(sitename = site.sitename, category = category, currentPageId = 0, startPageId = 0, updateDate = timezone.localtime())
            task.save()

        # Last page 구하기
        req = requests.get(site.categoryListPage.replace('{category}', category))
        html = req.content.decode('utf-8','replace')
        soup = BeautifulSoup(html, 'html.parser')
        lastPageId = getLastPage(site, soup)
        myLogger.info("LAST Page of {} - {} : {}".format(site.sitename, category, lastPageId))

        for pageId in range(task.currentPageId, lastPageId + 1):
            req = requests.get(site.detailPageUrl.replace("{category}", category).replace("{page}", str(pageId)))
            html = req.content.decode('utf-8','replace')
            soup = BeautifulSoup(html, 'html.parser')
            dateTime = datetime.datetime.now(tz=timezone.utc)

            extractMagnet(site, task, soup, category, pageId, dateTime)
    
    endDt = timezone.localtime()
    myLogger.info("=========================")
    myLogger.info(" END AT for {} : {}".format(category, endDt))
    myLogger.info("=========================")


def startCrawler(site, multiprocessEnable=False):
    if site.enable == False:
        return

    categories = site.categories.split(",")
    categories = [category.strip() for category in categories]

    if multiprocessEnable == True:

        processes = []

        for category in categories:
            processes.append(Process(target=crawlSingleCategory, args=(site, category)))

        for process in processes:
            process.start()

        for process in processes:
            process.join()
    
    else: 
        for category in categories:
            crawlSingleCategory(site, category) 

if __name__ == "__main__":
    sites = List.objects.all()
    for site in sites:
        startCrawler(site, True)