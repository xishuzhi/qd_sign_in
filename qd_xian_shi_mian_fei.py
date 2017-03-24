
from bs4 import BeautifulSoup
from urllib import request
from selenium import webdriver
import chardet
import os
import sys
import getopt
import time
import logging
from logging import handlers
import datetime
sys_code = sys.getfilesystemencoding()

url = "https://f.qidian.com/"

SAVE_TYPE_TEXT_NOWARP = 0
SAVE_TYPE_TEXT_WARP = 1
SAVE_TYPE_TEXT_NOWARP_XHTML = 2
SAVE_TYPE_TEXT_WARP_XHTML = 3

Logger = None

#从免费书列表中获取限免书籍信息
def get_limit_list():
    fp = request.urlopen("https://f.qidian.com/")
    html = fp.read()
    metaSoup = BeautifulSoup(html, "html.parser")
    # print(metaSoup)
    limit_list = metaSoup.find('div', attrs={'id': 'limit-list'})
    # print(limit_list)
    book_info_list = limit_list.findAll('div', attrs={'class': 'book-mid-info'})
    book = []
    for i in book_info_list:
        data = {'name':i.h4.get_text(),'url':'http:' + i.h4.a['href']+"#Catalog"}
        book.append(data)
    print(book)
    return book

def get_book_info(text):
    if text:
        #打开网页转为系统编码
        data = text
        name=actor=count=''
        try:
            #转换为系统编码后给bs4解析
            metaSoup = BeautifulSoup(data, "html.parser")
    #查找   #查找书籍信息
            book_info = metaSoup.find('div', attrs={'class':'book-info'})
            if book_info == None:
                err = metaSoup.find('div', attrs={'class':'error-text fl'})
                if err != None:
                    print(err.get_text())
                return "","",""
    #书名   #获取书名字符串
            name = book_info.h1.em.get_text()
            #print(book_info.h1.em.get_text())
    #作者   #获取作者字符串
            #print(book_info.h1.a.get_text())
            actor = book_info.h1.a.get_text()
    #查找   #查找章节数量
            catalogCount = metaSoup.find('li', attrs={'class':'j_catalog_block'}).i
    #总章节 #获取总章节数量
            #print(catalogCount.get_text())
            count = catalogCount.get_text()
            count = count[1:-2]
            #info_text = u'书名：%s，作者：%s，总章节：%s' % name,actor,count
            #info_text = name + actor + count
            #info_text = '书名：{0}，作者：{1}，总章节：{2}'.format(name.encode('utf-8'),actor.encode('utf-8'),count.encode('utf-8'))
            info_text = '书名：{0}，作者：{1}，总章节：{2}'.format(name, actor, count)
            #print(info_text)
            ##获取书名标签Tag
            #print(book_info.h1.em.prettify('utf-8'))
            #保存书名时需要转换为系统编码
            #saveText(book_info.h1.em.prettify(sys_code))
            #saveText(info_text,"info.txt")
            #return name.encode('utf-8'),actor.encode('utf-8'),count.encode('utf-8')
        except :
            print("error")
        return name, actor, count

def get_book_by_id(id):
    url = 'https://book.qidian.com/info/%s'% id
    fp = request.urlopen(url)
    html = fp.read()
    name,actor,count = get_book_info(html)
    book = [{'name':name,'url':url+"#Catalog"}]
    return book
#打开链接获取页面源码
def get_html(url,count=0):
    try:
        fp = request.urlopen(url)
        # req = request.Request(url)
        # fp = request.urlopen(req)
        html = fp.read()  # python3.x read the html as html code bytearray
    except Exception as e:
        print(e)
        print('页面打开失败：[%s]' % url)
        if(count > 5):
            return '404'
        return get_html(url,count+1)
    html = html.decode('utf-8')
    fp.close()
    return html
#用浏览器打开网页获得源码
def get_html_by_browserIe(url):
    thisPath = os.getcwd()
    iedriver = thisPath + "\\IEDriverServer.exe"
    html_source = ''
    if not os.path.exists(iedriver):
        print("no IEDriverServer")
    os.environ["webdriver.ie.driver"] = iedriver
    browser = webdriver.Ie(iedriver)
    try:
        browser.get(url)
        time.sleep(5)
        html_source = browser.page_source
        print('open')
    except:
        print('wenti')
        pass
    finally:
        browser.quit()
        print('finally')
        print(html_source)
        return html_source
#用浏览器打开网页获得源码
def get_html_by_browser(url):
    browser = webdriver.Chrome()
    browser.get(url)
    time.sleep(5)
    html_source = browser.page_source
    browser.quit()
    return html_source
#保存章节和内容到文件,ytpe 为保存方式
def save_volume(url,filePath,type=SAVE_TYPE_TEXT_NOWARP):
    ht = get_html(url)
    # ht = get_html("http://vipreader.qidian.com/chapter/3155120/54155582")
    # print(ht)
    try:
        metaSoup = BeautifulSoup(ht, "html.parser")
        book_info = metaSoup.find('div', attrs={'class': 'text-wrap'}).find('h3', attrs={'class': 'j_chapterName'})
        book_data = metaSoup.find('div', attrs={'class': 'read-content j_readContent'})
        #print(book_info.get_text())
        #print(book_data.get_text())
        with open(filePath, 'wb') as f:
            if f:
                volume_name = book_info.get_text().encode('utf-8')
                text = book_data.get_text()
                f.write(volume_name)
                if type == SAVE_TYPE_TEXT_NOWARP:
                    f.write(text.encode('utf-8'))
                if type == SAVE_TYPE_TEXT_WARP or type == SAVE_TYPE_TEXT_NOWARP_XHTML or type == SAVE_TYPE_TEXT_WARP_XHTML:
                    text = text.replace('　　', '\n　　')
                    f.write(text.encode('utf-8'))
                f.close()
        if type == SAVE_TYPE_TEXT_NOWARP_XHTML or type == SAVE_TYPE_TEXT_WARP_XHTML:
            with open(filePath+'.xhtml', 'wb') as fx:
                if fx:
                    fx.write(volume_name)
                    html = book_data.prettify('utf-8')
                    #html = html.replace('<div class="read-content j_readContent">', '\n').replace('</div>', '')
                    fx.write(html)
                    fx.close()
    except OSError as err:
        print("OSError:"+err)
    except IOError as err:
        print("IOError:" + err)
    except Exception as err:
        print("Exception:" + err)
    except:
        print("except error")
    finally:
        return book_info.get_text().encode('utf-8')
#从章节目录中提取章节名和章节链接
def get_volume_list(url='',count=0):
    try:
        html = ''
        if count==0:
            html = get_html(url)
        elif count==1:
            html = get_html_by_browser(url)
        metaSoup = BeautifulSoup(html, "html.parser")
        # 查找章节数量
        catalogCount = metaSoup.find('li', attrs={'class': 'j_catalog_block'}).i
        v_count = catalogCount.get_text()
        v_count = v_count[1:-2]
        volume_wrap = metaSoup.findAll('div', attrs={'class': 'volume-wrap'})
        v_list = []
        v_v = 0
        v_volume = {}

        for li in volume_wrap:
            volume_list = li.findAll('li')
            #print(volume_list)
            l_tmp = []
            for i in volume_list:
                #print("章节名：%s , 链接：%s" % (i.get_text(),i.a['href']))
                d = {'name':i.get_text(),'url':'http:'+i.a['href']}
                v_list.append(d)
                l_tmp.append(d)
            v_volume[v_v] = l_tmp
            v_v += 1

        if len(v_list) == 0 or len(v_list) < int(v_count) and count == 0:
            #print("count="+str(count))
            return get_volume_list(url, count + 1)

        return v_list,v_volume
    except:
        print('error url = %s'% url)
        if count == 0:
            return get_volume_list(url,count+1)
        else:
            print("write to file!")
            with open(metaSoup.title.get_text()+'.log', 'wb') as f:
                if f:
                    f.write(metaSoup.prettify('utf-8'))
                    f.close()
            return []
#制作字符替换字典
def make_dict(s_in,s_out):
    d = dict()
    if len(s_in) <= len(s_out):
        l = len(s_in)
        for i in range(l):
            d.update(str.maketrans(s_in[i],s_out[i]))
    else:
        l = len(s_out)
        for i in range(l):
            if i < l:
                d.update(str.maketrans(s_in[i],s_out[i]))
            else:
                d.update(str.maketrans(s_in[i], ''))
    return d
#替换字符串
def replace_text(text):
    t = make_dict('１２３４５６７８９０，．！？/\\*?!\n', '1234567890，。！？___？！ ')
    text = text.translate(t)
    text = text.strip()
    text = text.lstrip()
    return text
#替换字符串
def escape_file_path(path):
    path = path.replace('/', '-')
    path = path.replace('\\', '-')
    path = path.replace('*', '-')
    path = path.replace('?', '？')
    path = path.replace('!', '！')
    path = path.replace('\n', '')
    path = path.replace('', ' ')
    path = path.strip()
    path = path.lstrip()
    return path
#获得日志实例
def GetLogger(level=logging.INFO):
    '''Set up logging'''
    global Logger
    if Logger == None:
        script_path = os.getcwd()
        log_path = '%s,%s,%s'% (script_path,os.sep,'qd.log')
        log_file = 'qd.log'
        Logger = logging.getLogger('QD')
        Logger.setLevel(level)
        __logHandler__ = logging.handlers.RotatingFileHandler(log_file,maxBytes=10485760,backupCount=10)
        __formatter__ = logging.Formatter("%(asctime)s_%(levelname)s:%(message)s")
        __logHandler__.setFormatter(__formatter__)
        Logger.addHandler(__logHandler__)
    return Logger
#写日志
def write_log(text):
    L = GetLogger()
    print(text)
    L.info(text)
#按分卷下载
def save_by_volume(book_volume,book_name='',download_path='',download_type=SAVE_TYPE_TEXT_NOWARP):
    log_string = '\n\n\n'
    for volume in book_volume:
        count_volume = 1
        for book in book_volume[volume]:
            #print(i)
            if type(book) == type({}):
                if 'name' in book and 'url' in book:
                    #print('name = %s,url = %s' % (replace_text(book['name']), book['url']))
                    v_name = replace_text(book['name'])
                    v_url = book['url']
                    v_filename = "%s_%s" % (str(volume).zfill(2),str(count_volume).zfill(5))
                    # path = '%s\\%s_%s.txt' % (book_path,str(count_book),str(count_volume))
                    full_path = '%s\\%s.txt' % (download_path, v_filename)
                    if os.path.exists(full_path) and os.path.getsize(full_path) > 100:
                        #print('%s exists continue : %s' % (path,'continue'))
                        #write_log('%s exists continue : %s' % (path, v_url))
                        count_volume += 1
                        log_string += '[P]<%s>:%s.txt -> %s,' % (replace_text(book_name), v_filename, v_name)
                        continue
                    else:
                        volume_name = save_volume(v_url, full_path, download_type)
                        volume_name = replace_text(volume_name.decode('utf-8'))
                        # print('  downlaod:<%s>:%s : %s' % (book_name.replace('\n', ''),volume_name.decode('utf-8'),v_url))
                        write_log('  downlaod:<%s>:%s -> %s: %s' % (book_name.replace('\n', ''), volume_name, v_filename + '.txt', v_url))
                        log_string += '[D]<%s>:%s.txt -> %s,' % (replace_text(book_name),v_filename,volume_name)
                    count_volume += 1
    log_string += '\n\n\n'
    if os.path.isdir(download_path):
        try:
            with open(download_path + '\\list.txt', 'w') as f:
                t = log_string
                t = t.replace(',','\n')
                f.write(t)
        except:
            pass
        finally:
            f.close()
    return log_string

#main
def main(argv):
    book_id = []
    basename = os.path.splitext(os.path.basename(__file__))[0]
    try:
        opts, args = getopt.getopt(argv, "hi:f", ["id=,list="])
    except getopt.GetoptError:
        print('%s.py -i <id>' % basename)
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('%s.py -i <id>' % basename)
            sys.exit()
        elif opt == 'f':
            print('download all Limited-time free book : https://f.qidian.com/')
        elif opt in ("-i", "--id"):
            book_id = arg
        elif opt in ("-f", "--list"):
            filename = arg
            try:
                if os.path.exists(filename):
                    with open(filename, 'r') as f:
                        for line in f.readlines():
                            if len(line) > 0 and line[0] != '#' or line[0] != '\\\\':
                                book_id.append(replace_text(line))
                elif os.path.exists('list.txt'):
                    with open('list.txt', 'r') as f:
                        for line in f.readlines():
                            if len(line) > 0 and line[0] != '#' or line[0] != '\\\\':
                                book_id.append(replace_text(line))
                else:
                    print('open list.txt failed!')
                    sys.exit(2)
            except:
                print('open list.txt failed! error!!')
                sys.exit(2)
        else:
            print('%s.py -h for help' % basename)
            sys.exit()


    write_log("start qd_xian_shi_mian_fei.py")
    # 获取当前路径
    print(os.getcwd())
    thisPath = os.getcwd()
    download_type = SAVE_TYPE_TEXT_NOWARP
    config_file_path = thisPath + '\\' + 'qd_download_type.config'
    if os.path.exists(config_file_path):
        with open(config_file_path) as f:
            try:
                data = f.read();
                # data_list = data.split('\n')
                # for line in data_list:
                #     text = line
                #     text =  text.strip().lstrip()
                #     if text.startswith('#') or len(line) < 1:
                #         continue
                #     elif text.startswith('download_type')
                data = data[data.find('download_type'):]
            except:
                print('config file error !!')
            c = data.split('=')[1].strip().lstrip()
            if c == '0':
                download_type = SAVE_TYPE_TEXT_NOWARP
            elif c == '1':
                download_type = SAVE_TYPE_TEXT_WARP
            elif c == '2':
                download_type = SAVE_TYPE_TEXT_NOWARP_XHTML
            elif c == '3':
                download_type = SAVE_TYPE_TEXT_WARP_XHTML
    else:
        s = """#\n#0 下载存为TXT不换行\n#1 下载存为TXT换行\n#2 下载存为TXT不换行，下载存为xhtml\n#3 下载存为TXT换行，下载存为xhtml\ndownload_type = 0\n[BOOK_ID_LIST]\n"""
        with open(config_file_path, 'w') as f:
            f.write(s)
            f.close()
    limit_list = []
    if len(book_id) > 0:
        for id in book_id:
            if len(id) > 0:
                l = get_book_by_id(id)
                for i in l:
                    limit_list.append(i)
    else:
        # 获取所有限免书籍列表
        limit_list = get_limit_list()
    for limit in limit_list:
        print(limit)
        book_name = replace_text(limit['name'])
        bool_url = limit['url']
        book_path = thisPath + '\\' + book_name
        if not os.path.exists(book_name):
            os.mkdir(book_name)
        book_info,book_volume = get_volume_list(bool_url)
        #print(book_volume)
        # print("start book_name = %s,id=%s,url=%s" % (book_name,str(count_book),bool_url))
        write_log("start book_name = %s,id = %s,url = %s" % (book_name, str(1), bool_url))
        result = save_by_volume(book_volume,book_name,book_path, download_type)
        # print("finished book_name = %s" % (book_name))
        write_log(result)
        write_log("finished book_name = %s" % (book_name))

# def main(book_id = 0):
#     write_log("start qd_xian_shi_mian_fei.py")
#     # 获取当前路径
#     print(os.getcwd())
#     thisPath = os.getcwd()
#     download_type = SAVE_TYPE_TEXT_NOWARP
#     config_file_path = thisPath + '\\' + 'qd_download_type.config'
#     if os.path.exists(config_file_path):
#         with open(config_file_path) as f:
#             try:
#                 data = f.read();
#                 # data_list = data.split('\n')
#                 # for line in data_list:
#                 #     text = line
#                 #     text =  text.strip().lstrip()
#                 #     if text.startswith('#') or len(line) < 1:
#                 #         continue
#                 #     elif text.startswith('download_type')
#                 data = data[data.find('download_type'):]
#             except:
#                 print('config file error !!')
#             c = data.split('=')[1].strip().lstrip()
#             if c == '0':
#                 download_type = SAVE_TYPE_TEXT_NOWARP
#             elif c == '1':
#                 download_type = SAVE_TYPE_TEXT_WARP
#             elif c == '2':
#                 download_type = SAVE_TYPE_TEXT_NOWARP_XHTML
#             elif c == '3':
#                 download_type = SAVE_TYPE_TEXT_WARP_XHTML
#     else:
#         s = """#\n#0 下载存为TXT不换行\n#1 下载存为TXT换行\n#2 下载存为TXT不换行，下载存为xhtml\n#3 下载存为TXT换行，下载存为xhtml\ndownload_type = 0\n[BOOK_ID_LIST]\n"""
#         with open(config_file_path, 'w') as f:
#             f.write(s)
#             f.close()
#     if book_id > 0:
#         limit_list = get_book_by_id(book_id)
#     else:
#         # 获取所有限免书籍列表
#         limit_list = get_limit_list()
#     for limit in limit_list:
#         book_name = escape_file_path(limit['name'])
#         bool_url = limit['url']
#         book_path = thisPath + '\\' + book_name
#         if not os.path.exists(book_name):
#             os.mkdir(book_name)
#         book_info,book_volume = get_volume_list(bool_url)
#         #print(book_volume)
#         # print("start book_name = %s,id=%s,url=%s" % (book_name,str(count_book),bool_url))
#         write_log("start book_name = %s,id = %s,url = %s" % (book_name, str(1), bool_url))
#         result = save_by_volume(book_volume,book_name,book_path, download_type)
#         # print("finished book_name = %s" % (book_name))
#         write_log(result)
#         write_log("finished book_name = %s" % (book_name))

if __name__ == "__main__":
    main(sys.argv[1:])
