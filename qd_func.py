from urllib import request
from bs4 import BeautifulSoup
from selenium import webdriver
import time


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
#替换字符串，路径或文件名
def replace_text(text):
    t = make_dict('１２３４５６７８９０，．！？/\\*?!\n', '1234567890，。！？___？！ ')
    text = text.translate(t)
    text = text.strip()
    text = text.lstrip()
    return text
#替换标题不用做路径和文件名
def replace_title(text):
    t = make_dict('１２３４５６７８９０，．！?!\n', '1234567890，。！？！ ')
    text = text.translate(t)
    text = text.strip()
    text = text.lstrip()
    return text
#替换字符串
def replace_file_path(path):
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

#从免费书列表中获取限免书籍信息 return{'name':书名,'url':'https://book.qidian.com/info/0000000#Catalog"}
def get_limit_list():
    fp = request.urlopen("https://f.qidian.com/")
    html = fp.read()
    metaSoup = BeautifulSoup(html, "html.parser")
    limit_list = metaSoup.find('div', attrs={'id': 'limit-list'})
    book_info_list = limit_list.findAll('div', attrs={'class': 'book-mid-info'})
    book = []
    for i in book_info_list:
        data = {'name':i.h4.get_text(),'url':'http:' + i.h4.a['href']+"#Catalog"}
        book.append(data)
    return book

#从书页源码中获取书名，作者，总章节数量，return 书名，作者，章节数量
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
#输入id获取信息，return{'name':书名,'url':'https://book.qidian.com/info/0000000#Catalog"}
def get_book_by_id(id):
    url = 'https://book.qidian.com/info/%s'% id
    html = get_html(url)
    if not html == '404':
        name,actor,count = get_book_info(html)
    else:
        name = 'None'
    book = [{'name':name,'url':url+"#Catalog"}]
    return book
#打开链接获取页面源码，return utf-8编码的网页源码
def get_html(url,count=0):
    try:
        fp = request.urlopen(url)
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
    #time.sleep(5)
    browser.implicitly_wait(10)
    html_source = browser.page_source
    browser.quit()
    return html_source
#从章节目录中提取章节名和章节链接 return [{'name':章节名,'url':章节连接},]，总章节数量
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

#获取章节内容,return 章节名，txt文本，html文本
def get_volume(url):
    ht = get_html(url)
    src_text = """
    <?xml version="1.0" encoding="utf-8"?>
    <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"
      "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">

    <html xmlns="http://www.w3.org/1999/xhtml">
    <head>
    <title>%s</title>
    </head>
    <body>
    <h1>%s</h1>
    <div>
    %s
    </div>
    <div><br/></div>
    </body>
    </html>
    """
    try:
        metaSoup = BeautifulSoup(ht, "html.parser")
        book_info = metaSoup.find('h3', attrs={'class': 'j_chapterName'})
        book_data = metaSoup.find('div', attrs={'class': 'read-content j_readContent'})
        # print(book_info)
        # print(book_data)
        text = ''
        html = ''
        tital = ''
        volume_name = book_info.get_text()
        volume_data = book_data.get_text()
        text += volume_name
        text += (volume_data.replace('　　', '\n　　'))
        text = replace_title(text)
        v_n = replace_title(volume_name)
        htm = str(book_data.prettify())
        html = src_text % (v_n, v_n, htm)
        tital = replace_file_path(v_n)
    except:
        print("except error")
    finally:
        #return book_info.get_text().encode('utf-8')
        return tital,text,html

def save_file(path,data):
    try:
        with open(path,'w') as f:
            f.write(str(data))
            f.close()
    except Exception as e:
        print('error:%s'% e)
        pass


if __name__ == "__main__":
    pass
    # #测试，根据id获取书籍名称和目录章节
    # print(get_book_by_id(1005188549))
    # #测试，从限免章节页面获取书籍名称和目录章节
    # print(get_limit_list())
    # #测试，用浏览器打开目录，获取书名作者总章节
    # print(get_book_info(get_html_by_browser('http://book.qidian.com/info/3600493#Catalog')))
    # 获取书籍的章节和连接
    # print(get_volume_list('http://book.qidian.com/info/3600493#Catalog'))
    # tital, text, html= get_volume('http://read.qidian.com/chapter/mXVR4wuK70o1/EMQ5k8jKRMwex0RJOkJclQ2')
    # print(text)
    # save_file('t.txt',text)
    # save_file('t.txt.xhtml', html)