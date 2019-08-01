from selenium import webdriver
import requests
import re
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

WEBDRIVER_PATH = r'./chromedriver'
LIBERTYKOREA_URL = r'http://www.libertykoreaparty.kr/web/news/briefing/delegateBriefing/mainDelegateBriefingView.do'


def app():
    driver = webdriver.Chrome(WEBDRIVER_PATH)
    # set options of webdriver
    # options = webdriver.ChromeOptions()
    # options.add_argument('headless')
    # options.add_argument('user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 \
    #                     (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36')
    driver.get(LIBERTYKOREA_URL)
    # base url for crawling articles
    baseUrl = "http://www.libertykoreaparty.kr/web/news/briefing/delegateBriefing/readDelegateBriefingView.do"
    seen = set()

    # number of articles in a page
    length = len(driver.find_elements_by_css_selector("div.board_group.st_list1 > table > tbody tr > td.subject > a"))
    print(length)

    # crawl articles in a page
    # TODO: crawl data moving pages
    # TODO: design db structure, insert crawled data into db

    i = 1
    while i <= length:
        # click nth article
        onClick = driver.find_element_by_css_selector("div.board_group.st_list1 > table > tbody > tr:nth-child({})\
            > td.subject > a".format(i)).get_attribute('onclick')
        bbsId = re.search("SPB_\d+", onClick).group()
        # check duplication
        if bbsId in seen:
            continue
        seen.add(bbsId)

        # parse content
        content = parseContent(baseUrl, {'bbsId': bbsId})
        print(i, "th article:", content["title"])

        # insert content into db

        i += 1

    driver.close()




def parseContent(url, param):
    html = requests.request('get', url, params=param)
    dom = BeautifulSoup(html.text, 'lxml')
    return {"title": dom.select_one('td.subject2').text, \
           "body": dom.select_one('#txt_print').text, \
           "date": dom.select_one('#txt_date').text, \
           "keyword": dom.select_one('div.keyword').text.split(': ')[1].split(', ')}


if __name__ == '__main__':
    app()