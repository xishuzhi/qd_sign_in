import urllib
from urllib import request
import gzip
import json
import os

#获取书籍信息和目录的JSON
def getBookInfoData(bookID):
    url = 'http://4g.if.qidian.com/Atom.axd/Api/Book/GetChapterList?BookId=%s' % bookID
    request = urllib.request.Request(url)
    request.add_header('Accept-encoding', 'gzip')
    request.add_header('User-Agent', 'Mozilla QDReaderAndroid/6.2.0/232/qidian/000000000000000')

    response = urllib.request.urlopen(request)
    #print(response.read())
    data = response.read()
    #json_str = json.dumps(t)
    #print(response.info())
    html = gzip.decompress(data).decode("utf-8")
    #print(html)
    return html



def getTextData(bookID,ChepterID):
    url = 'http://4g.if.qidian.com/Atom.axd/Api/Book/GetContent?BookId=%s&ChapterId=%s' % (bookID,ChepterID)
    request = urllib.request.Request(url)
    request.add_header('Accept-encoding', 'gzip')
    request.add_header('User-Agent', 'Mozilla QDReaderAndroid/6.2.0/232/qidian/000000000000000')
    response = urllib.request.urlopen(request)
    data = response.read()
    html = gzip.decompress(data).decode("utf-8")
    #print(html)
    return html

def loadData(url):
    url = 'http://4g.if.qidian.com/Atom.axd/Api/Book/GetContent?BookId=1005194988&ChapterId=1005194988'
    request = urllib.request.Request(url)
    request.add_header('Accept-encoding', 'gzip')
    request.add_header('User-Agent', 'Mozilla QDReaderAndroid/6.2.0/232/qidian/000000000000000')
    # request.add_header('Content-Type', 'application/x-www-form-urlencoded')
    # request.add_header('bookId', '1005194988&bookmarkid=&delebmid=&type=0')
    # request.add_header('Content-Length', '46')
    # request.add_header('Connection', 'Keep-Alive')
    response = urllib.request.urlopen(request)
    data = response.read()
    #print(data)
    html = gzip.decompress(data).decode("utf-8")
    print(html[0])

    return html

#替换字符串
def replace_text(path):
    path = path.replace('\\r', '\r')
    path = path.replace('\\n', '\n')
    return path

def menu():
    #os.popen('cls')
    #os.system('cls')
    print ('输入书籍ID下载：')
    print('输f下载当前限免书籍：')
    print ('x. 退出')
    selection = input('输入书籍ID：')
    return selection
def process(path):
    for f in os.listdir(path):
        fin = open(path+"/"+f,"r")
        #print(fin.read())
        fin.close()
def main():
    try:
        while True:
            selection = menu()
            if selection.isdigit() and int(selection) > 0:
                n,l = start(selection)
                while True:
                    s = input('是否合并？（y/n）')
                    if s == 'y':
                        with open(n+'.txt','w') as f:
                            for i in l:
                                if os.path.exists(i):
                                    with open(i,'r') as a:
                                        f.write(a.read())
                                        f.write('\n')
                                        f.write('\n')
                                        a.close()
                            f.close()
                        print('合并完成')
                        break
                    else:
                        print('取消合并')
                        break

            elif selection == 'f' or selection == 'F':
                xm = get_limit_list()
                for i in xm:
                    start(i['id'])
                break
            elif selection == 'x' or selection == 'X':
                break
            else:
                print('输入错误！')
        print ('exit')
    except Exception as e:
        print ('Error: %s,%s' % (selection,e))
    pass
def start(id = 0):
    thisPath = os.getcwd()
    book_ID = id
    print('开始下载:%s' % book_ID)
    book_info_string = getBookInfoData(book_ID)
    book_info_json = json.loads(book_info_string)
    #print(book_info_json)
    book_info_data = book_info_json['Data']
    book_name = book_info_data['BookName']
    book_author = book_info_data['Author']
    book_chapters = book_info_data['Chapters']
    print(book_name)
    print(book_author)
    print(len(book_chapters))
    chapters_list = []
    for i in book_chapters:
        if i['v'] == 0:
            chapters_name = i['n']
            chapters_id = i['c']
            chapters_list.append({'name':chapters_name, 'id':chapters_id})
            #print("name:%s,id=%s" % (chapters_name, chapters_id))
    book_path = thisPath + '\\' + book_name
    all_book_list = []
    if not os.path.exists(book_name):
        os.mkdir(book_name)
    chapters_count = 0
    out_put = "书名;%s,作者:%s,ID:%s\n" % (book_name, book_author, book_ID)
    for l in chapters_list:
        n = l['name']
        c = l['id']
        cn = "C_%s.txt" % (str(chapters_count).zfill(5))
        p = "%s\\%s" % (book_path,cn)
        all_book_list.append(p)
        if os.path.exists(p) and os.path.getsize(p) > 100:
            out_put += '[P]%s\t(%s)\t%s size=%s\n' % (n, c, cn,os.path.getsize(p))
            pass
        else:
            t = getTextData(book_ID, c)
            t_json = json.loads(t)
            if t_json['Message'] == '成功' and chapters_count > 0:
                with open(p, 'w') as f:
                    f.write(n)
                    f.write('\n')
                    if chapters_count == 0:
                        pass
                        # bq = t_json['Data']
                        # print(type(bq[i]))
                        # for i in bq:
                        #     if type(bq[i]) == 'str' or type(bq[i]) == 'int':
                        #         f.write(str(bq[i]))
                        #         f.write('\n')
                        #         print(bq[i])
                    else:
                        f.write(replace_text(t_json['Data']))
                    f.close()
                out_put += '[D]%s\t(%s)\t%s\n' % (n, c, cn)
            else:
                out_put += '[E]%s\t(%s)\t%s\n' % (n, c, cn)
        chapters_count += 1
    info_path = book_path + '\\' + 'info.txt'
    with open(info_path, 'w') as f:
        f.write(out_put)
        f.close()
    print('下载《%s》完成' % book_name)
    return book_name , all_book_list

from bs4 import  BeautifulSoup
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
        id_link = i.h4.a['href']
        id = id_link.split('/')[-1]
        #print(id_link.split('/')[-1])
        data = {'name':i.h4.get_text(),'url':'http:' + id_link+"#Catalog",'id':id}
        book.append(data)
    #print(book)
    return book

if __name__ == '__main__':
    main()

