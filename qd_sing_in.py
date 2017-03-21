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
                txt = f.read()
                n = txt.split(',')
                # 输入账号和密码
                browser.find_element_by_id("username").send_keys(n[0])
                browser.find_element_by_id("password").send_keys(n[1])
                time.sleep(1)
                # 点击按钮提交登录表单
                browser.find_element_by_css_selector("a.red-btn.go-login.btnLogin.login-button").click()
                time.sleep(5)
        #print(browser.current_url)
        while(browser.current_url != url):
            #print("等待登陆!!!")
            time.sleep(1)
        # 验证登录成功的url
        currUrl = browser.current_url
        if currUrl == url:
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
    #s = traceback.format_exc()
    #print(s)
    pass

def checkClick(br):
    data_now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print("star time :" + data_now)
    isNextDay = False
    isFinish = False
    while True:
        os.system('cls')
        try:
            n_t = datetime.datetime.now()
            now = n_t.strftime('%d')
            this_time = n_t.strftime('%Y-%m-%d %H:%M:%S')
            print(this_time)
            if str(data_now) != str(now):
                data_now = now
                isNextDay = True
                isFinish = False
                br.refresh()
                time.sleep(15)
            if isFinish:
                print('Wait for the next day!')
                time.sleep(1)
                return checkClick(br)
        except:
            print("time error")
        try:
            button_data = br.find_element_by_class_name("plus-items")
            radios = button_data.find_elements_by_class_name("btn")
            sing_in_count = 0
            for bt in radios:
                print(bt.text)
                if(bt.text[0:3] == '经验值'):
                    sing_in_count = sing_in_count + 1
                if bt.text == '可领取':
                    print("点击")
                    isNextDay = False
                    bt.click()
                    time.sleep(5)
                    br.refresh()
                    time.sleep(10)
            print("sing_in_count = "+ sing_in_count)
            if sing_in_count == 8:
                isFinish = True
        except:
            writeLog()
            print("............")
            br.refresh()
            time.sleep(15)
            return checkClick(br)
        time.sleep(5)
        if isNextDay:
            br.refresh()
            time.sleep(10)


if __name__ == "__main__":
    browser = webdriver.Chrome()
    start_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_str = "start time :%s\n" % start_time
    if work(browser):
        checkClick(browser)
    browser.quit()


"""
//*[@id="online-exp-get5"]
#online-exp-get5

body > div.fix-layout.column-wild-content > div.fl-right-wrap > div.exp-tasks > div.month-ticket.award-for-login > ul > li:nth-child(1) > a

/html/body/div[8]/div[2]/div[2]/div[2]/ul/li[1]/a
//*[@id="online-exp-get5"]
//*[@id="online-exp-get10"]
/html/body/div[8]/div[2]/div[2]/div[2]/ul/li[3]/a
/html/body/div[8]/div[2]/div[2]/div[2]/ul/li[4]/a
/html/body/div[8]/div[2]/div[2]/div[2]/ul/li[3]/a

弹出按钮
//*[@id="btnClose_dialog_869"]/span
//*[@id="btnClose_dialog_565"]

弹出框
//*[@id="alert_box_container_dialog_869"]/table/tbody/tr[2]/td[2]/div/div[1]/strong
//*[@id="alert_box_container_dialog_869"]/table/tbody/tr[2]/td[1]
x
//*[@id="alert_box_container_dialog_869"]/table/tbody/tr[2]/td[2]/div/div[3]/text()
//*[@id="anchorclose_dialog_869"]



"""