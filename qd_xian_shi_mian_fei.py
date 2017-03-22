
from bs4 import BeautifulSoup
from urllib import request
from selenium import webdriver
import chardet
import os
import sys
import time
sys_code = sys.getfilesystemencoding()

url = "https://f.qidian.com/"

SAVE_TYPE_TEXT_NOWARP = 0
SAVE_TYPE_TEXT_WARP = 1
SAVE_TYPE_TEXT_NOWARP_XHTML = 2
SAVE_TYPE_TEXT_WARP_XHTML = 3

#从免费书列表中获取限免书籍信息
def get_limit_list():
    fp = request.urlopen("https://f.qidian.com/")
    html = fp.read();
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
def get_html_by_browser(url):
    browser = webdriver.Chrome()
    browser.get(url)
    time.sleep(10)
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
                f.write(book_info.get_text().encode('utf-8'))
                if type == SAVE_TYPE_TEXT_NOWARP:
                    f.write(book_data.get_text().encode('utf-8'))
                if type == SAVE_TYPE_TEXT_WARP:
                    text = book_data.get_text()
                    text = text.replace('　　', '\n　　')
                    f.write(text.encode('utf-8'))
                f.close()
        if type == SAVE_TYPE_TEXT_NOWARP_XHTML or type == SAVE_TYPE_TEXT_WARP_XHTML:
            with open(filePath+'.xhtml', 'wb') as fx:
                if fx:
                    fx.write(book_info.get_text().encode('utf-8'))
                    fx.write(book_data.encode('utf-8'))
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
        # # 查找章节数量
        # catalogCount = metaSoup.find('li', attrs={'class': 'j_catalog_block'}).i
        # count = catalogCount.get_text()
        # count = count[1:-2]
        volume_wrap = metaSoup.findAll('div', attrs={'class': 'volume-wrap'})
        v_list = []
        for li in volume_wrap:
            volume_list = li.findAll('li')
            #print(volume_list)
            for i in volume_list:
                #print("章节名：%s , 链接：%s" % (i.get_text(),i.a['href']))
                d = {'name':i.get_text(),'url':'http:'+i.a['href']}
                v_list.append(d)
        if len(v_list) == 0 and count == 0:
            #print("count="+str(count))
            return get_volume_list(url, count + 1)
        return v_list
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

def escape_file_path(path):
    path = path.replace('/', '-')
    path = path.replace('\\', '-')
    path = path.replace('*', '-')
    path = path.replace('?', '？')
    return path

if __name__ == "__main__":
    #get_html_by_browser("https://book.qidian.com/info/1003383443#Catalog")
    #获取当前路径
    print(os.getcwd())
    thisPath = os.getcwd()
    download_type = SAVE_TYPE_TEXT_NOWARP
    config_file_path = thisPath+'\\'+'qd_download_type.config'
    if(os.path.exists(config_file_path)):
        with open(config_file_path) as f:
            data = f.read();
            try:
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

    basename = os.path.splitext(os.path.basename(__file__))[0]

    #获取所有限免书籍列表
    limit_list = get_limit_list()

    count_book = 0
    log_string = ''
    for limit in limit_list:
        book_name = escape_file_path(limit['name'])
        bool_url = limit['url']
        book_path = thisPath+ '\\' + book_name
        if not os.path.exists(book_name):
            os.mkdir(book_name)
        book_info = get_volume_list(bool_url)
        print("start book_name = %s,id=%s,url=%s" % (book_name,str(count_book),bool_url))

        count_volume = 0
        for book in book_info:
            v_name = book['name']
            v_url = book['url']
            path = '%s\\%s_%s.txt' % (book_path,str(count_book),str(count_volume))
            if os.path.exists(path):
                if os.path.getsize(path) > 0:
                    print('%s exists continue : %s' % (path,v_url))
                    count_volume += 1
                    continue
            else:
                volume_name = save_volume(v_url,path,download_type).strip().lstrip()
                print('  downlaod:<%s>:%s : %s' % (book_name.replace('\n', ''),volume_name.decode('utf-8'),v_url))
            count_volume += 1
        count_book += 1
        print("finished book_name = %s" % (book_name))

    print('all over !!!')