
from bs4 import BeautifulSoup
from urllib import request
import chardet
import os
import sys
sys_code = sys.getfilesystemencoding()

url = "https://f.qidian.com/"


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
        fp = request.urlopen(url,timeout=300)
        #fp = request.urlopen(request.Request(url, headers = config.QD_HEADER), None)
    except Exception as e:
        print(e)
        print('页面打开失败：[%s]' % url)
        return "404"
    html = fp.read()  # python3.x read the html as html code bytearray
    fp.close()
    codedetect = chardet.detect(html[0:100])['encoding']
    if codedetect == "GB2312":
        html = html.decode('gbk')
    elif codedetect == "utf-8":
        html = html.decode('utf-8')
    return html
#保持章节和内容到文件
def save_volume(url,filePath):
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
                f.write(book_data.get_text().encode('utf-8'))
                f.close()
        # with open(filePath+'.xhtml', 'wb') as fx:
        #     if fx:
        #         fx.write(book_info.get_text().encode('utf-8'))
        #         fx.write(book_data.encode('utf-8'))
        #         fx.close()
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
    #url = "http://book.qidian.com/info/1004289255#Catalog"
    # fp = request.urlopen(url)
    # html = fp.read();
    try:
        html = get_html(url)
        metaSoup = BeautifulSoup(html, "html.parser")
        volume_list = metaSoup.find('div', attrs={'class': 'volume-wrap'}).findAll('li')
        #print(volume_list)
        v_list = []
        for i in volume_list:
            #print("章节名：%s , 链接：%s" % (i.get_text(),i.a['href']))
            d = {'name':i.get_text(),'url':'http:'+i.a['href']}
            v_list.append(d)
        return v_list
    except:
        print('error url = %s'% url)
        if count < 5:
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
    path = path.replace('?', '-')
    return path

if __name__ == "__main__":
    #获取当前路径
    print(os.getcwd())
    thisPath = os.getcwd()

    basename = os.path.splitext(os.path.basename(__file__))[0]

    #获取所有限免书籍列表
    limit_list = get_limit_list()

    count_book = 0
    log_string = ''
    for limit in limit_list:
        book_name = limit['name']
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

                    continue
            else:
                volume_name = save_volume(v_url,path).strip().lstrip()

                print('\t\tdownlaod:<%s>:%s : %s' % (v_name,volume_name.encode(sys_code),v_url))
            count_volume += 1
        count_book += 1
        print("finished book_name = %s" % (book_name))

    print('all over !!!')