# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait  # 显示等待
from selenium.common.exceptions import WebDriverException   #
import time
import datetime
import os
import json

from selenium.webdriver import Remote
from selenium.webdriver.chrome import options
from selenium.common.exceptions import InvalidArgumentException

class ReuseChrome(Remote):

    def __init__(self, command_executor, session_id):
        self.r_session_id = session_id
        Remote.__init__(self, command_executor=command_executor, desired_capabilities={})

    def start_session(self, capabilities, browser_profile=None):
        """
        重写start_session方法
        """
        if not isinstance(capabilities, dict):
            raise InvalidArgumentException("Capabilities must be a dictionary")
        if browser_profile:
            if "moz:firefoxOptions" in capabilities:
                capabilities["moz:firefoxOptions"]["profile"] = browser_profile.encoded
            else:
                capabilities.update({'firefox_profile': browser_profile.encoded})

        self.capabilities = options.Options().to_capabilities()
        self.session_id = self.r_session_id
        self.w3c = False


def test1():
    browser = webdriver.Chrome()
    browser.get('https://www.115.com')
    current_url = browser.current_url
    executor_url = browser.command_executor._url
    session_id = browser.session_id

    print(current_url)
    print(session_id)
    print(executor_url)

    del browser

    time.sleep(5)


    driver2 = ReuseChrome(command_executor=executor_url, session_id=session_id)
    print(driver2.current_url)
    driver2.get('http://tieba.baidu.com')

    time.sleep(25)


def test2():
    browser = webdriver.Chrome()
    browser.get('https://www.115.com')
    current_url = browser.current_url
    executor_url = browser.command_executor._url
    session_id = browser.session_id

    print(current_url)
    print(session_id)
    print(executor_url)

    while True:
        print('等待5秒。。。：'+browser.current_url)
        print('cookies:'+str(browser.get_cookies()))
        time.sleep(5)

    '''
    第一步：get('https://115.com/)
    第二步：登录成功跳转'https://115.com/home/userhome'
    第三步：打开'https://home.115.com/
    第四步:查找签到按钮'btn = browser.find_element_by_class_name('white-modal')
    btn   class = 'white-modal sign sign-new'
    
    cookies:[{'domain': 'home.115.com', 'httpOnly': True, 'value': '7819730515463984112425242ee9572cb6a5a6802effdd0bd2f0616c2fbe72', 'expiry': 1549076801.670187, 'secure': False, 'path': '/', 'name': 'acw_tc'}, {'domain': '.115.com', 'httpOnly': True, 'value': '5338142_A1_1546398434', 'secure': False, 'path': '/', 'name': 'UID'}, {'domain': '.115.com', 'httpOnly': True, 'value': 'fca8bc60a10a114862deb3b751af4389', 'secure': False, 'path': '/', 'name': 'CID'}, {'domain': '.115.com', 'httpOnly': True, 'value': 'a8ec1537691a11916e15d72657450ed6e8620bb7eb21a46a0efd3589d99944b55928fb2972f55ad74d9c434e122cbb1c9155b0008f02815794714d10', 'secure': False, 'path': '/', 'name': 'SEID'}]
    
    '''

# test2()
with open('115.cookies.txt', 'r', encoding='utf-8') as f:
    print(f.read())
    cookies_lsit = json.loads(f.read())
    f.close()
    for l in cookies_lsit:
        print('导入cookies：' + str(l))

