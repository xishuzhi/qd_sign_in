# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait  # 显示等待
from selenium.common.exceptions import WebDriverException   #
import time
import datetime
import os
import json


class NextDayTools:
    def __init__(self):
        self.start_time_datetime = datetime.datetime.now()      # 记录程序启动时间
        self.record_day_old = datetime.datetime.day             # 记录日期
        self.save_datetime = datetime.datetime.now()            # 记录时间
        self.update_datetime = datetime.datetime.now()          # 持续记录的更新时间
        self.next_datetime = datetime.datetime.now()            # 记录下一次执行时间

    # 更新时间
    def update(self):
        self.update_datetime = datetime.datetime.now()

    # 刷新日期
    def refresh_day(self):
        self.record_day_old = datetime.datetime.day
        self.save_datetime = datetime.datetime.now()

    def check_new_day(self):

        result = False
        _day = (self.update_datetime.day - self.save_datetime.day)

        if _day != 0:
            result = True

        print('程序启动时间：'+self.start_time_datetime.strftime('%Y-%m-%d %H:%M:%S')+'\n检查是否新的一天!\ntime_now  = '
              + self.update_datetime.strftime('%Y-%m-%d %H:%M:%S')+'\nsave_time = '
              + self.save_datetime.strftime('%Y-%m-%d %H:%M:%S')+'\n结果:'+str(_day))
        return result


    def check_time_seconds(self, seconds):
        result = False
        _seconds = (self.update_datetime - self.save_datetime).seconds
        if _seconds > seconds:
            result = True
        return result


class must_get_url(object):
    '''
    必须到达的URL
       参数：
       url    - 必须到达的地址
    '''
    def __init__(self, url):
        self.url = url

    def __call__(self, driver):
        # driver.get(self.url)
        print(driver.current_url)
        return self.url == driver.current_url


class qd_sing_in:
    def __init__(self, br_name=''):
        self.url = "https://my.qidian.com/level"
        self.url_qd = "https://www.qidian.com"
        self.cookies_file = 'qd.cookies.txt'
        self.cookies = ''
        self.step = {0: 300, 1: 300, 2: 600, 3: 1200, 4: 1800, 5: 3600, 6: 3600, 7: 3600, 8: 3600}
        self.index = 0

        if br_name == 'IE' or br_name == 'ie' or br_name == 'Ie':
            self.browser = webdriver.Ie()
        else:
            self.browser = webdriver.Chrome()

    def login_qd(self):
        self.browser.get(self.url_qd)
        if os.path.exists(self.cookies_file):
            try:
                with open(self.cookies_file, 'r', encoding='utf-8') as f:
                    cookies_lsit = json.loads(f.read())
                    f.close()
                    for l in cookies_lsit:
                        self.browser.add_cookie(l)
                        print('导入cookies：' + str(l))
            except WebDriverException as e:
                print('导入cookies错误：' + e.msg)
        result = self.open_qd_level()
        if result:
            self.cookies = self.browser.get_cookies()
            with open('qd.cookies.txt', 'w', encoding='utf-8') as f:
                f.write(json.dumps(self.cookies))
                f.close()
        return result

    def open_qd_level(self):
        result = False
        try:
            if self.url != self.browser.current_url:
                self.browser.get(self.url)
            result = WebDriverWait(self.browser, 120).until(must_get_url(self.url))
        except WebDriverException as e:
            print('open_qd错误：'+e.msg)
        return result

    def quit(self):
        self.browser.quit()

    def find_btn(self, btn_name='ui-button'):
        try:
            btn = self.browser.find_element_by_class_name(btn_name)
            if btn.text == '领取':
                print('找到领取经验按钮')
                # btn.click()
            else:
                print('时间未到：'+btn.text)
                t = btn.text.split(':')
                second = int(t[0])*60 + int(t[1])
                print(second)
            return True
            # print('查找btn2结果：' + btn.text)
        except WebDriverException as e:
            # print('find_element_by_class_name错误：'+e.msg)
            return False

    def find_btn_by_class(self, element, name):
        try:
            btn = element.find_element_by_class_name(name)
            return btn
        except WebDriverException as e:
            return None

    def find_award_task_status(self):
        try:
            time_str = self.browser.find_element_by_class_name('award-task-status')
        except WebDriverException as e:
            print('find_award_task_status错误：'+e.msg)

    def check_next_time(self):
        try:
            btn = self.browser.find_element_by_class_name('ui-button')
            if btn.text == '领取':
                return True, 0
                # pass
            else:
                print('时间未到：'+btn.text)
                t = btn.text.split(':')
                second = int(t[0])*60 + int(t[1])
                print('距离下次签到剩余时间：'+str(second)+'秒')
                return False, second
        except WebDriverException:
            return True, -1
            # pass

    # 执行签到函数
    def sing_in(self):
        sing_finish = False
        second = -1
        if not self.open_qd_level():
            time.sleep(10)
            return sing_finish, second
        try:
            items = self.browser.find_elements_by_class_name('award-task-item')
            count = 0
            for i in items:
                ii = i.text.split('\n')
                for n in ii:
                    if n == '已领取':
                        count += 1
            self.index = count
            print('总签到数量为：' + str(count))
            if self.index == 8:
                print('今天的签到已经完成')
                sing_finish = True
                return sing_finish, second
            btn = self.browser.find_element_by_class_name('ui-button')
            if btn.text == '领取':
                print('找到领取经验按钮，点击领取经验')
                btn.click()
                self.index += 1
                second = 0
            else:
                print('时间未到：'+btn.text)
                t = btn.text.split(':')
                second = int(t[0])*60 + int(t[1])
                print('距离下次签到剩余时间：'+str(second)+'秒')

        except WebDriverException:
            sing_finish = True

        return sing_finish, second


def main():
    # 初始化计时工具
    dt = NextDayTools()
    # 初始化起点签到类
    qd = qd_sing_in()
    # 登录起点
    if qd.login_qd():
        # 签到结果是否完成,签到序号,距离下一次签到剩余等待时间（秒）
        # is_finish, index, seconds = qd.sing_in()
        is_finish, seconds = qd.sing_in()
        while True:
            os.system('cls')
            dt.update()             # 更新时间记录
            if dt.check_new_day():
                print('第二天了，开始签到')
                # 执行签到函数
                is_finish, seconds = qd.sing_in()
                # 新的一天，刷新日期
                dt.refresh_day()
            if not is_finish:
                is_finish, seconds = qd.check_next_time()
                if dt.check_time_seconds(seconds):
                    is_finish, seconds = qd.sing_in()
            else:
                print('今天签到已经完成')
            time.sleep(10)
    qd.quit()



def get_time():
    dt = datetime.datetime.now()

    t = {'年': str(dt.strftime('%Y')), '月': str(dt.strftime('%m')), '日': str(dt.strftime('%d')),
         '时': str(dt.strftime('%H')), '分': str(dt.strftime('%M')), '秒': str(dt.strftime('%S'))}
    return t



def test():
    dt = NextDayTools()
    qd = qd_sing_in()
    if qd.open_qd():
        # 签到结果是否完成,签到序号,距离下一次签到剩余等待时间（秒）
        is_finish, index, seconds = qd.sing_in()
        while True:
            os.system('cls')
            dt.update()             # 更新时间记录
            if dt.check_new_day():
                print('第二天了，开始签到')
                # 执行签到函数
                is_finish, index, seconds = qd.sing_in()
                # 新的一天，刷新日期
                dt.refresh_day()
            if not is_finish:
                if dt.check_time_seconds(seconds):
                    is_finish, index, seconds = qd.sing_in()
            else:
                print('今天签到已经完成')
            # print('签到结果:%s,序号:%s,等待时间:%s' % (is_finish, index, seconds))
            print('签到序号:'+index)
            time.sleep(10)
    qd.quit()



if __name__ == "__main__":
    main()






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

iedriver = r"F:\temp\IEDriverServer.exe"
os.environ["webdriver.ie.driver"] = iedriver
browser = webdriver.Ie(iedriver)
http://my.qidian.com/level


#elTaskWrap > li:nth-child(1) > a

//*[@id="elTaskWrap"]/li[1]/a

//*[@id="elTaskWrap"]/li[2]/span

//*[@id="elTaskWrap"]/li[1]/a

//*[@id="elTaskWrap"]/li[3]/span

//*[@id="elTaskWrap"]/li[2]/span

<a href="javascript:;" class="ui-button ui-button-small elGetExp " data-num="1" data-timeleft="0" data-vip="2">领取</a>

#elOldexp

//*[@id="elOldexp"]
"""