# -*- coding:utf-8 -*-

import io
import sys
from selenium import webdriver

browser = webdriver.Chrome()

def abc():
    pass

# info
# https://movie.douban.com/subject/26611804/ 

def subject():

    # https://movie.douban.com/subject/30140571/
    dbId = 30140571
    dbPath = "https://movie.douban.com/subject/%s/" % (dbId)
    browser.get(dbPath)
    browser.execute_script("$('span').css('display', 'inline');")
    
    # #info > span:nth-child(1) > span.attrs > a
    # //*[@id="info"]
    
    # 导演
    # //*[@id="info"]/span[1]/span[2]/a
    elem = browser.find_element_by_xpath('//*[@id="info"]/span[1]/span[2]/a[1]')
    print(elem.text)
    
    # 编辑
    # //*[@id="info"]/span[2]/span[2]/a[1]
    elem = browser.find_elements_by_xpath('//*[@id="info"]/span[2]/span[2]/a')
    for ele in elem:
        print(ele.text)

    # 主演
    print(u'\n\n主演:')
    # //*[@id="info"]/span[3]/span[2]/span[1]/a
    elem = browser.find_elements_by_xpath('//*[@id="info"]/span[3]/span[2]/span[*]/a')
    for ele in elem:
        if ele.text:
            print((ele.text).encode("GBK", 'ignore'))

    # 其它
    infos = browser.find_element_by_xpath('//*[@id="info"]')
    if infos.text:
        print((infos.text).encode("GBK", 'ignore'))


subject()

