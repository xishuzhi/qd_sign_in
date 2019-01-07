# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait  # 显示等待
from selenium.common.exceptions import WebDriverException
import time
import datetime
import os
import json
from threading import Thread


class NextDayTools:
    def __init__(self, first_run=True):
        self.start_time_datetime = datetime.datetime.now()      # 记录程序启动时间
        self.record_day_old = datetime.datetime.day             # 记录日期
        self.save_datetime = datetime.datetime.now()            # 记录时间
        self.update_datetime = datetime.datetime.now()          # 持续记录的更新时间
        self.next_datetime = datetime.datetime.now()            # 记录下一次执行时间
        self.first_run = first_run                              # 第一次运行记录

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

        if self.first_run:
            result = True
            self.first_run =False

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
        self.url_login='https://passport.qidian.com/?appid=10&areaid=1&auto=1&autotime=30&version=1.0&ticket=1&target=top&popup=0&source=pc&returnurl=https%3A%2F%2Fmy.qidian.com'
        self.url_passport = 'https://passport.qidian.com'
        self.url_myqd = 'https://my.qidian.com'
        self.position_url_passport = 27
        self.cookies_file = 'qd.cookies.txt'
        self.cookies = ''
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

    def open_qd_level(self, refresh=False):
        result = False
        try:
            if self.url != self.browser.current_url or refresh:
                self.browser.get(self.url)
            if self.browser.current_url == self.position_url_passport \
                    or self.browser.current_url[0:self.position_url_passport] == self.url_passport:
                if os.path.exists('config.txt'):
                    with open('config.txt') as f:
                        txt = f.read()
                        n = txt.split(',')
                        # 输入账号和密码
                        self.browser.find_element_by_id("username").send_keys(n[0])
                        self.browser.find_element_by_id("password").send_keys(n[1])
                        time.sleep(1)
                        # 点击按钮提交登录表单
                        self.browser.find_element_by_css_selector("a.red-btn.go-login.btnLogin.login-button").click()
                        time.sleep(5)
                        self.browser.get(self.url)

            result = WebDriverWait(self.browser, 120).until(must_get_url(self.url))
        except WebDriverException as e:
            print('open_qd错误：'+e.msg)
        return result

    def open_myqd(self):
        self.browser.get(self.url)

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
                return -1
            else:
                print('check_next_time时间未到：'+btn.text)
                t = btn.text.split(':')
                if len(t) == 2:
                    second = int(t[0])*60 + int(t[1])
                    print('check_next_time距离下次签到剩余时间：'+str(second)+'秒')
                    return second
                else:
                    return -1
        except WebDriverException:
            return -1

    def check_login_failed(self):
        if self.browser.current_url == self.url_login or self.browser.current_url[0:self.position_url_passport] == self.url_passport:
            return True
        else:
            return False

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
            print('sing_in总领取经验数量为：' + str(count))
            if self.index == 8:
                print('sing_in今天的签到已经完成')
                sing_finish = True
                return sing_finish, second
            btn = self.browser.find_element_by_class_name('ui-button')
            if btn.text == '领取':
                print('sing_in找到领取经验按钮，点击领取经验')
                btn.click()
                self.browser.implicitly_wait(3)
                self.index += 1
                second = 0
            else:
                print('sing_in时间未到：'+btn.text)
                t = btn.text.split(':')
                if len(t) == 2:
                    second = int(t[0])*60 + int(t[1])
                    print('sing_in距离下次领取经验剩余时间：'+str(second)+'秒')

        except WebDriverException:
            # sing_finish = True
            # self.open_qd_level(True)
            # return self.sing_in()
            print('貌似签到完成了，需要再次检查')
        return sing_finish, second


class start_sing_in(Thread):
    def __init__(self, qd):
        Thread.__init__(self)
        self.qd = qd

    def run(self):
        # 登录起点
        if self.qd.login_qd():
            # 签到结果是否完成,距离下一次签到剩余等待时间（秒）
            is_finish, seconds = self.qd.sing_in()
            while True:
                os.system('cls')
                if not is_finish:
                    seconds = self.qd.check_next_time()
                    if seconds <= 0:
                        is_finish, seconds = self.qd.sing_in()
                    time.sleep(1)
                else:
                    print('main今天领取经验已经完成')
                    self.qd.quit()
                    break


def main():
    # 初始化计时工具
    dt = NextDayTools()
    # 初始化起点签到类
    qd = qd_sing_in()
    sing_in_thread = start_sing_in(qd)
    while True:
        os.system('cls')
        dt.update()  # 更新时间记录
        if dt.check_new_day():
            print('main第二天了，开始领取经验')
            if not sing_in_thread.isAlive():
                sing_in_thread.start()
                sing_in_thread.join()
            else:
                print('main等待签到完成')
            print('main签到完成，退出线程')


def get_time():
    dt = datetime.datetime.now()

    t = {'年': str(dt.strftime('%Y')), '月': str(dt.strftime('%m')), '日': str(dt.strftime('%d')),
         '时': str(dt.strftime('%H')), '分': str(dt.strftime('%M')), '秒': str(dt.strftime('%S'))}
    return t


def test():
    # 初始化计时工具
    dt = NextDayTools()
    # 初始化起点签到类
    qd = qd_sing_in()
    # 登录起点
    if qd.login_qd():
        # 签到结果是否完成,签到序号,距离下一次签到剩余等待时间（秒）
        is_finish, seconds = qd.sing_in()
        try_count = 0
        while True:
            os.system('cls')
            dt.update()  # 更新时间记录
            if dt.check_new_day():
                print('第二天了，开始签到')
                # 刷新页面
                if qd.open_qd_level(True):
                    # 执行签到函数
                    is_finish, seconds = qd.sing_in()
                # 新的一天，刷新日期，不管是否成功签到都刷新日期
                dt.refresh_day()
            if not is_finish:
                is_finish, seconds = qd.check_next_time()
                if seconds < 0:
                    is_finish, seconds = qd.sing_in()
            else:
                print('今天签到已经完成')
            if qd.check_login_failed():
                try_count += 1
            if try_count > 5:
                break
            time.sleep(10)
    qd.quit()


if __name__ == "__main__":
    main()






