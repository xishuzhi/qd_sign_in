from qd_utils import *
from bs4 import BeautifulSoup
from threading import Thread
import requests
import re
import html
from html.parser import HTMLParser

class td(Thread):
    def __init__(self, book_name,url,dir_path):
        Thread.__init__(self)
        self.book_name = book_name
        self.url = url
        self.dir_path = dir_path
    def run(self):
        try:
            file_path = self.dir_path+'\\'+ replace_file_path(self.book_name)+'.txt'
            if os.path.exists(file_path) and os.path.getsize(file_path) > 40:
                #print('pass : %s')
                pass
            else:
                txt = get_text(self.url)
                if len(txt) > 0 and txt != '404':
                    str = self.book_name
                    str += '\n'
                    str += replace_str(txt)
                    if len(str) > len(self.book_name):
                        print('download<%s>:%s , %s' % (self.book_name, self.url, file_path))
                        save_file(file_path, str)
                    else:
                        print('error<%s>:%s , %s' % (self.book_name, self.url, file_path))

        except Exception as e:
            print(e)

def main_t():
    l = get_book_list()
    path = getPath() + '\\se'
    tasks = []
    count = 0
    for i in l:
        # print(i)
        name = i['name']
        url = i['url']
        tasks.append(td(name,url,path))
        count+=1
    #print('count='+str(count))

    blocks = 5
    task_index = 0
    threads = []

    while len(tasks) > 0 or len(threads) > 0:
        #print('tasks=%d,threads=%d' %(len(tasks),len(threads)))
        if len(threads) < blocks and len(tasks) > 0:
            t = tasks.pop()
            t.start()
            threads.append(t)
            task_index += 1;
        for i in threads:
            if not i.isAlive():
                threads.remove(i)
                #break

def set_url_list():
    url = 'http://www.55rere.com/se/dushijiqing/index.html'
    url2 = 'http://www.55rere.com/se/dushijiqing/index_%s.html'
    url_list = []
    url_list.append(url)
    for i in range(2,226):
        url_list.append(url2 % i)
    # #print(url_list)
    return url_list

def main():
    l = get_book_list()
    path = getPath()+'\\se'
    tasks = []
    for i in l:
        #print(i)
        name = i['name']
        url = i['url']
        file_path = path+'\\'+replace_file_path(name)+'.txt'
        file_path = path_format(file_path)
        try:
            if os.path.exists(file_path):
                pass
            else:
                print('download<%s>:%s , %s' % (name, url, file_path))
                txt = get_text(url)
                if len(txt) > 0 and txt != '404':
                    str = name
                    str += '\n'
                    str += replace_str(txt)
                    save_file(file_path, str)
        except Exception as e:
            print(e)

def main2():
    print('start')
    url_list = set_url_list()
    u_l = []
    u_s = ''
    count = 0
    path = getPath() + '\\se'
    if not os.path.exists(path):
        os.mkdir(path)
    for url in url_list:
        f = path + '\\' + str(count) + '.txt'
        if os.path.exists(f):
            print('跳过：%s'%f)
            pass
        else:
            html = get_html(url)
            #print(url)
            try:
                bs = BeautifulSoup(html, 'html.parser')
                textList = bs.find('ul', attrs={'class': 'textList'}).findAll('a')
                #print(textList)
                for i in textList:
                    s = 'tital=%s,url = http://www.55rere.com%s'%(i['title'],i['href'])
                    u_s+=s
                    u_s += '\n'
                    print(s)
                    u_l.append(s)
                print(f)
                save_file(f,u_s)
                u_s = ''
            except Exception as e:
                print(e)
        count += 1
    print('+1')

def get_book_list():
    d = open_file(getPath()+'\\se\\all.txt')#r'D:\code\PyCharm\qd_sign_in\se\all.txt'
    #print(d)
    dd = d.split('\n')
    book_list = []
    for line in dd:
        # print(line)
        if len(line) > 0:
            s = line.split(',')
            if len(s) == 2:
                book_list.append({'name': s[0][6:], 'url': s[1][6:]})
            elif len(s) == 3:
                n = s[0][6:]+s[1]
                book_list.append({'name': n, 'url': s[2][6:]})
    #print(book_list)
    return book_list

def join_text_all():
    path = getPath()+'\\se\\all.txt'
    print(path)
    u = []
    for i in range(0,225):
        f = '%s\\se\\%s.txt'% (getPath(),str(i))
        print(f)
        u.append(f)
    join_text(path,u)

def get_html_se(url,count=0):
    try:
        req = request.Request(url)
        req.add_header('Accept-encoding', 'gzip,deflate,sdch')
        req.add_header('Accept-Language', 'zh-CN,zh;q=0.8')
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
        return get_html_se(url,count+1)
    return html

def post_get(url):
    pass
    headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
               'Accept-Encoding': 'gzip, deflate, compress',
               'Accept-Language': 'en-us;q=0.5,en;q=0.3',
               'Cache-Control': 'max-age=0',
               'Connection': 'keep-alive',
               'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0'}
    r = requests.get(url,timeout=60)
    # print(r.headers['content-type'])
    # print(r.encoding)
    # print(r.text.encode(r.encoding).decode('utf-8'))
    return r.text.encode(r.encoding).decode('utf-8')

def get_text(url):
    #html = get_html_se(url)
    html = post_get(url)
    #print(html)
    try:
        bs = BeautifulSoup(html, 'html.parser')
        textList = bs.find('div', attrs={'class': 'novelContent'})
        print(textList)
        txt = textList.get_text()
        print(len(txt))
        if len(txt) < 100:
            textP = bs.find_all('p')
            txt = ''
            for i in textP:
                #print(i.string)
                txt += i.string
                txt += '\n'
        else:
            print('get_text:'+txt)
        print(len(txt))
        if len(txt) < 100:
            txt = html
            p_s = txt.find('''<div class="novelContent">''')
            p_e = -1
            if p_s > 0:
                txt = txt[p_s:]
                #print(txt)
                p_e = txt.find('</div>')
                if p_e > 0:
                    txt = txt[:p_e+6]
                    print('0000000000000000')
                    url_re = re.compile(r'<.+?>')
                    results = re.findall(url_re, txt)
                    a = list({re.sub('\d', '', i): i for i in results}.values())
                    tab = dict((x, '') for x in a)
                    txt_list = txt.split('\n')
                    #print(txt_list)
                    xx=''
                    for i in txt_list:
                        for j in a:
                            #print(i.replace(j,''))
                            xx+=i.replace(j,'')
                    print(xx)
                    # for result in results:
                    #     #print(result)
                    #     txt.replace(result,'')
                    #     print(txt)
        else:
            print('p:' + txt)
        return txt
    except Exception as e:
        print(e)
def replace_str(text):
    t = make_dict('ａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕｖｗｘｙｚＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺ１２３４５６７８９０', 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890')
    text = text.translate(t)
    text = text.strip()
    text = text.lstrip()
    return text


if __name__ == "__main__":
    pass
    #main_t()
    #post_get('http://www.55rere.com/se/dushijiqing/20110212/1480.html')
    #print(get_text('http://www.55rere.com/se/dushijiqing/525368.html'))
    t = get_text('http://www.55rere.com/se/dushijiqing/526913.html')
    #print(t)



