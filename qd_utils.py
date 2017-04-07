#-*- coding：utf-8 -*-
from urllib import request
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import os
import gzip
import json

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
    t = make_dict('ａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕｖｗｘｙｚＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺ１２３４５６７８９０，．！?!\n', 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890，。！？！ ')
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
    path = path.replace('|', '_')
    path = path.replace(':', '：')
    path = path.strip()
    path = path.lstrip()
    return path
#从免费书列表中获取限免书籍信息 return{'name':书名,'url':'https://book.qidian.com/info/0000000#Catalog",'id':书ID}
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
        id_link = i.h4.a['href']
        id = id_link.split('/')[-1]
        #print(id_link.split('/')[-1])
        data = {'name':i.h4.get_text(),'url':'http:' + id_link+"#Catalog",'id':id}
        book.append(data)
    #print(book)
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
        req = request.Request(url)
        req.add_header('Accept-encoding', 'gzip,deflate,sdch')
        #req.add_header('User-Agent', 'Mozilla QDReaderAndroid/6.2.0/232/qidian/000000000000000')
        req.add_header('User-Agent','Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3033.0 Safari/537.36')
        # 返回页面内容
        doc = request.urlopen(req).read() # python3.x read the html as html code bytearray
        # 解码
        try:
            html = gzip.decompress(doc).decode("utf-8")
            #print('返回gzip格式的文件')
        except:
            html = doc.decode("utf-8")
            #print('返回正常格式的文件')
    except Exception as e:
        print('页面打开失败：[%s] error：%s' % (url,e))
        if(count > 5):
            return '404'
        return get_html(url,count+1)
    return html
#用浏览器打开网页获得源码
def get_html_by_browser(url):
    browser = webdriver.Chrome()
    browser.get(url)
    time.sleep(5)
    #browser.implicitly_wait(10)
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
        metaSoup = BeautifulSoup(ht,"html.parser") #BeautifulSoup(ht, "html.parser")
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
        htm = book_data.prettify()
        htm = htm.replace('<p>\n','<p>  ')
        html = src_text % (v_n, v_n, htm)
        tital = replace_file_path(v_n)
    except:
        print("except error")
    finally:
        #return book_info.get_text().encode('utf-8')
        return tital,text,html
def path_win(path):
    path =  path.replace('/', '\\')
    if path[:-1] == '\\':
        path = path[0:-1]
    return path
def path_linux(path):
    path =  path.replace('\\', '/')
    if path[:-1] == '/':
        path = path[0:-1]
    return path
def path_format(path):
    if os.name == 'nt':
        path = path_win(path)
    elif os.name == 'Android' or 'posix':
        path = path_linux(path)
    return path
def getPath():
    path = './'
    if os.name == 'nt':
        path = os.getcwd()
    elif os.name == 'Android' or 'posix':
        path = os.path.dirname(__file__)
        if path == './':
            path = '/storage/emulated/0/qpython/scripts3/projects3/qidian'
    return path
def save_file(path,data):
    try:
        path = path_format(path)
        #data = data.replace('\ue844',' ')
        with open(path,'w', encoding='utf-8') as f:
            f.write(str(data))
            f.close()
            return True
    except Exception as e:
        print('error:file(%s):%s'% (path,e))
        return False
        pass
def open_file(path):
    try:
        path = path_format(path)
        with open(path,'r', encoding='utf-8') as f:
            data = f.read()
            f.close()
            return data;
    except Exception as e:
        print('error:file(%s):%s'% (path,e))
        return ''
        pass
def save_gzip(path, data):
    try:
        path = path_format(path)
        content = str(data).encode('utf-8')
        with gzip.open(path, 'wb') as f:
            f.write(content)
            f.close()
            return True
    except Exception as e:
        print('save_gzip error:file(%s):%s' % (path, e))
        return False
        pass
def open_gzip(path):
    try:
        with gzip.open(path, 'rb') as f:
            data = f.read().decode('utf-8')
            f.close
            return data
    except Exception as e:
        print('open_gzip error file:(%s);%s' % (path,e))
        return ''
#获取书籍信息和目录的JSON
def getBookInfoData(bookID):
    url = 'http://4g.if.qidian.com/Atom.axd/Api/Book/GetChapterList?BookId=%s' % bookID
    req = request.Request(url)
    req.add_header('Accept-encoding', 'gzip')
    req.add_header('User-Agent', 'Mozilla QDReaderAndroid/6.2.0/232/qidian/000000000000000')

    response = request.urlopen(req)
    #print(response.read())
    data = response.read()
    #json_str = json.dumps(t)
    #print(response.info())
    html = gzip.decompress(data).decode("utf-8")
    #print(html)
    json_data =  json.loads(html)
    return json_data
#获取章节详细信息 return [{'v_vip': 0, 'v_cid': 0000000, 'v_name': '章节名', 'v_url': 'https://vipreader.qidian.com/chapter/书ID_id/章节ID_cid'}, ]
def getBookVolumeInfoJson(bookID):
    book_id = bookID
    book_info_json = getBookInfoData(book_id)
    Data = book_info_json['Data']
    Volumes = Data['Volumes']
    Chapters = Data['Chapters']
    book_info_data = []
    count = 0
    for c in Chapters:
        volume_name = c['n']
        volume_cid = c['c']
        volume_vip = c['v']
        volume_url = 'https://vipreader.qidian.com/chapter/%s/%s' % (book_id, volume_cid)
        if volume_cid > 0:
            book_info_data.append(
                {'v_name': volume_name, 'v_cid': volume_cid, 'v_vip': volume_vip, 'v_url': volume_url,'count':count})
        count += 1
            # print('章节名：%s，章节ID：%s，vip：%s' % (volume_name,volume_cid,volume_vip))
    #print(book_info_data)
    return book_info_data,book_info_json
#合并文本
def join_text(name,file_list):
    try:
        with open(name, 'w',encoding='utf-8') as f:
            for i in file_list:
                t = path_format(str(i))
                if os.path.exists(t):
                    with open(t, 'r',encoding='utf-8') as a:
                        f.write(a.read())
                        f.write('\n')
                        f.write('\n')
                        a.close()
                elif os.path.exists(t+'.gz'):
                    with gzip.open(t+'.gz', 'rb') as a:
                        data = a.read().decode('utf-8')
                        f.write(data)
                        f.write('\n')
                        f.write('\n')
                        a.close
            f.close()
    except Exception as e:
        print('join_text_error : %s : %s' % (f,e))
        pass
#获取客户端形式的的JSON结果，适用于免费章节
def getTextData(bookID,ChepterID):
    url = 'http://4g.if.qidian.com/Atom.axd/Api/Book/GetContent?BookId=%s&ChapterId=%s' % (bookID,ChepterID)
    req = request.Request(url)
    req.add_header('Accept-encoding', 'gzip')
    req.add_header('User-Agent', 'Mozilla QDReaderAndroid/6.2.0/232/qidian/000000000000000')
    res = request.urlopen(req)
    data = res.read()
    html = gzip.decompress(data).decode("utf-8")
    #print(html)
    result = json.loads(html)
    if(result['Message']) == '失败':
        print("error:%s" % url)
        return ''
    return result


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
    # ａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕｖｗｘｙｚ
    # ＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺ
    #
    # abcdefghijklmnopqrstuvwxyz
    # ABCDEFGHIJKLMNOPQRSTUVWXYZ