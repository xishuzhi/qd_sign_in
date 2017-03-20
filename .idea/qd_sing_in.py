# -*- coding: utf-8 -*-
from selenium import webdriver
import time
import datetime
import traceback
import logging
import os

# 测试用例执行函数
def work(browser):
    url = "http://t.qidian.com/Profile/Score.php"
    browser.get(url)
    try:
        if os.path.exists('config.txt'):
            with open('config.txt') as f:
                txt = f.read();
                n = txt.split(',')
                # 输入账号和密码
                browser.find_element_by_id("username").send_keys(n[0])
                browser.find_element_by_id("password").send_keys(n[1])
                time.sleep(2)
                # 点击按钮提交登录表单
                #bt = browser.find_element_by_class_name("red-btn go-login btnLogin login-button")
                #browser.find_element_by_class_name("auto-login-box cf").click()
                browser.find_element_by_css_selector("a.red-btn.go-login.btnLogin.login-button").click()
                #print(browser.find_element_by_css_selector("a.red-btn.go-login.btnLogin.login-button").text)
                time.sleep(5)
        #print(browser.current_url)
        while(browser.current_url != url):
            #print("等待登陆!!!")
            time.sleep(1)
        # 验证登录成功的url
        currUrl = browser.current_url
        if currUrl == "http://t.qidian.com/Profile/Score.php":
            print(u"success")
            return True
        else:
            print(u"failure")
            writeLog()
            return False
    except:
        print(u"failure")
        writeLog()


# 写错误日志并截图
def writeLog():
    # # 组合日志文件名（当前文件名+当前时间）.比如：case_login_success_20150817192533
    # basename = os.path.splitext(os.path.basename(__file__))[0]
    # logFile = basename + "-" + datetime.datetime.now().strftime("%Y%m%d%H%M%S") + ".log"
    # logging.basicConfig(filename=logFile)
    # s = traceback.format_exc()
    # logging.error(s)
    # browser.get_screenshot_as_file("./" + logFile + "-screenshot_error.png")
    s = traceback.format_exc()
    #print(s)

def checkClick(br):
    data_now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print("star time :" + data_now)
    while True:
        os.system('cls')
        try:
            button_data = br.find_element_by_class_name("plus-items")
            radios = button_data.find_elements_by_class_name("btn")
            for bt in radios:
                print(bt.text)
                if (bt.text == '可领取'):
                    print("点击")
                    bt.click()
                    time.sleep(5)
                    br.refresh();
                    time.sleep(15)
        except:
            writeLog()
        #finally:
            print("zong shi zhi xing")
            br.refresh();
            time.sleep(15)
            return checkClick(br)
        time.sleep(5)
        try:
            n_t = datetime.datetime.now()
            now = n_t.strftime('%d')
            this_time = n_t.strftime('%Y-%m-%d %H:%M:%S')
            if str(data_now) != str(now):
                data_now = now
                br.refresh();
                time.sleep(15)
        except:
            print("time error")


if __name__ == "__main__":
    browser = webdriver.Chrome()
    start_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    this_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_str = "start time :%s\n" % start_time
    if work(browser):
        checkClick(browser)
    browser.quit()
    # while True:
    #     now = datetime.datetime.now().strftime('%d-%S')
    #     if (data_now != now):
    #         data_now = now
    #         print(data_now)