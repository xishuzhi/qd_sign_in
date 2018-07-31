# -*- coding：utf-8 -*-
from urllib import request
from bs4 import BeautifulSoup
import time
import os
import gzip
import json
from threading import Thread


# 制作字符替换字典
def make_dict(s_in, s_out):
    d = dict()
    if len(s_in) <= len(s_out):
        l = len(s_in)
        for i in range(l):
            d.update(str.maketrans(s_in[i], s_out[i]))
    else:
        l = len(s_out)
        for i in range(l):
            if i < l:
                d.update(str.maketrans(s_in[i], s_out[i]))
            else:
                d.update(str.maketrans(s_in[i], ''))
    return d


# 替换字符串，路径或文件名
def replace_text(text):
    t = make_dict('１２３４５６７８９０，．！？/\\*?!\n', '1234567890，。！？___？！ ')
    text = text.translate(t)
    text = text.strip()
    text = text.lstrip()
    return text


# 替换标题不用做路径和文件名
def replace_title(text):
    t = make_dict('ａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕｖｗｘｙｚＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺ１２３４５６７８９０，．！?!\n',
                  'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890，。！？！ ')
    text = text.translate(t)
    text = text.strip()
    text = text.lstrip()
    return text


# 替换字符串
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


def path_win(path):
    path = path.replace('/', '\\')
    if path[:-1] == '\\':
        path = path[0:-1]
    return path


def path_linux(path):
    path = path.replace('\\', '/')
    if path[:-1] == '/':
        path = path[0:-1]
    return path


def path_format(path):
    if os.name == 'nt':
        path = path_win(path)
    elif os.name == 'Android' or os.name == 'posix':
        path = path_linux(path)
    return path


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
        print('open_gzip error file:(%s);%s' % (path, e))
        return ''


def save_file(path, data):
    try:
        path = path_format(path)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(str(data))
            f.close()
            return True
    except Exception as e:
        print('error:file(%s):%s' % (path, e))
        return False
        pass


def open_file(path):
    try:
        path = path_format(path)
        with open(path, 'r', encoding='utf-8') as f:
            data = f.read()
            f.close()
            return data
    except Exception as e:
        print('error:file(%s):%s' % (path, e))
        return ''
        pass


# 打开链接获取页面源码，return utf-8编码的网页源码
def get_html(url, count=0):
    try:
        req = request.Request(url)
        req.add_header('Accept-encoding', 'gzip,deflate,sdch')
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3033.0 Safari/537.36')
        # 返回页面内容
        doc = request.urlopen(req).read()  # python3.x read the html as html code bytearray
        # 解码
        try:
            html = gzip.decompress(doc).decode("utf-8")
            # print('返回gzip格式的文件')
        except IOError:
            html = doc.decode("utf-8")
            # print('返回正常格式的文件')
    except Exception as e:
        print('页面打开失败：[%s] error：%s' % (url, e))
        if count > 5:
            return '404'
        return get_html(url, count + 1)
    return html


# 获取章节内容,return 章节名，txt文本，html文本
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
        meta_soup = BeautifulSoup(ht, "html.parser")  # BeautifulSoup(ht, "html.parser")
        book_info = meta_soup.find('h3', attrs={'class': 'j_chapterName'})
        book_data = meta_soup.find('div', attrs={'class': 'read-content j_readContent'})
        text = ''
        html = ''
        title = ''
        volume_name = book_info.get_text()
        volume_data = book_data.get_text()
        text += volume_name
        text += (volume_data.replace('　　', '\n　　'))
        text = replace_title(text)
        v_n = replace_title(volume_name)
        htm = book_data.prettify()
        htm = htm.replace('<p>\n', '<p>  ')
        html = src_text % (v_n, v_n, htm)
        title = replace_file_path(v_n)
    except:
        print("except error")
    finally:
        # return book_info.get_text().encode('utf-8')
        return title, text, html


def join_text_gz(name, file_list):
    try:
        with gzip.open(name, 'w') as f:
            for i in file_list:
                t = path_format(str(i))
                if os.path.exists(t):
                    with open(t, 'r', encoding='utf-8') as a:
                        txt = a.read() + '\n\n'
                        f.write(txt.encode('utf-8'))
                        a.close()
                elif os.path.exists(t + '.gz'):
                    with gzip.open(t + '.gz', 'rb') as a:
                        txt = a.read().decode('utf-8') + '\n\n'
                        f.write(txt.encode('utf-8'))
                        a.close
            f.close()
    except Exception as e:
        print('join_text_error : %s : %s' % (f, e))
        pass


def get_path():
    path = './'
    if os.name == 'nt':
        path = os.getcwd()
    elif os.name == 'Android' or 'posix':
        path = os.path.dirname(__file__)
        if path == './':
            path = '/storage/emulated/0/qpython/scripts3/projects3/qidian'
    return path


def get_limit_list_from_qidian():
    fp = request.urlopen("https://www.qidian.com/free")
    html = fp.read()
    meta_soup = BeautifulSoup(html, "html.parser")
    # print(metaSoup)

    book_img_text = meta_soup.find('div', attrs={'class': 'book-img-text'})
    limit_list = book_img_text.find_all('h4')

    book = []
    for i in limit_list:
        book_id = i.a['data-bid']
        n = i.a.text
        data = {'name': n, 'url': 'https://book.qidian.com/info/' + book_id + "#Catalog", 'id': book_id}
        book.append(data)
    # print(book)
    return book


# 获取书籍信息和目录的JSON
def get_book_info_data(book_id):
    url = 'http://4g.if.qidian.com/Atom.axd/Api/Book/GetChapterList?BookId=%s' % book_id
    req = request.Request(url)
    req.add_header('Accept-encoding', 'gzip')
    req.add_header('User-Agent', 'Mozilla/mobile QDReaderAndroid/6.6.6/269/qidian/000000000000000')
    response = request.urlopen(req)
    data = response.read()
    html = gzip.decompress(data).decode("utf-8")
    json_data = json.loads(html)
    return json_data


# 整理过的的json，原始json，是否限免
# 获取章节详细信息 return [{'v_vip': 0, 'v_cid': 0000000, 'v_name': '章节名', 'v_url': 'https://vipreader.qidian.com/chapter/书ID_id/章节ID_cid'}, ]
def get_book_volume_info_json(book_id):
    book_info_json = get_book_info_data(book_id)
    if book_info_json['Message'] == '成功':
        Data = book_info_json['Data']
        # volumes = Data['Volumes']
        chapters = Data['Chapters']
        is_free_limit = Data['IsFreeLimit']
        book_info_data = []
        count = 0
        for c in chapters:
            volume_name = c['n']
            volume_cid = c['c']
            volume_vip = c['v']
            volume_url = 'https://vipreader.qidian.com/chapter/%s/%s' % (book_id, volume_cid)
            if volume_cid > 0:
                book_info_data.append(
                    {'v_name': volume_name, 'v_cid': volume_cid, 'v_vip': volume_vip, 'v_url': volume_url,
                     'count': count})
            count += 1
            # print('章节名：%s，章节ID：%s，vip：%s' % (volume_name,volume_cid,volume_vip))
        # print(book_info_data)
        return book_info_data, book_info_json, is_free_limit
    else:
        print('ID=%s的书籍不存在！' % book_id)
    return [], book_info_json, ''


class DownloadBook(Thread):
    def __init__(self, book_name, book_volumes_json, book_info_json, dir_path, is_free_limit=-1):
        Thread.__init__(self)
        self.book_name = book_name
        self.book_volumes_json = book_volumes_json
        self.book_info_json = book_info_json
        self.dir_path = dir_path
        self.is_free_limit = str(is_free_limit)

    def run(self):
        self.dir_path = path_format(self.dir_path)
        if not os.path.exists(self.dir_path):
            os.mkdir(self.dir_path)
        print('start download <%s>' % self.book_name)
        f_info = path_format(self.dir_path+'\\'+'info_json.txt')
        f_volumes = path_format(self.dir_path + '\\' + 'volumes_json.txt')
        if os.path.exists(f_info):
            os.remove(f_info)
        if os.path.exists(f_volumes):
            os.remove(f_volumes)
        self.book_volumes_json.sort(key=lambda x: (x['count'], -x['count']))
        save_gzip(f_info+'.gz', str(self.book_info_json))
        save_gzip(f_volumes+'.gz', str(self.book_volumes_json))
        info_str = self.book_name+'\n'
        file_list = []
        is_new = False
        for i in self.book_volumes_json:
            # {'v_name': volume_name, 'v_cid': volume_cid, 'v_vip': volume_vip, 'v_url': volume_url}
            # print(i)
            v_name = i['v_name']
            v_url = i['v_url']
            v_cid = i['v_cid']
            v_vip = str(i['v_vip'])
            # print('v_vip = %s,type=%s'% (v_vip,type(v_vip)))
            f_name = self.dir_path + '\\' + str(v_cid) + '.txt'
            gz_name = self.dir_path + '\\' + str(v_cid) + '.txt.gz'
            gz_html = self.dir_path + '\\' + str(v_cid) + '.txt.html.gz'
            f_name = path_format(f_name)
            gz_name = path_format(gz_name)
            gz_html = path_format(gz_html)
            file_list.append(f_name)
            i_name = self.dir_path + '\\book_info.txt'
            i_name = path_format(i_name)
            if v_vip == '1':
                info_str += '%s.txt ---> %s (VIP)\n' % (str(v_cid), v_name)
            else:
                info_str += '%s.txt ---> %s\n' % (str(v_cid), v_name)
            if os.path.exists(f_name) and os.path.getsize(f_name) > 100 \
                    or os.path.exists(f_name+'.html') and os.path.getsize(f_name+'.html') > 100:
                # print('pass <%s> ---> %s' % (self.book_name,v_name))
                text_data = open_file(f_name)
                # 检查txt文件
                if len(text_data) > 0:
                    if save_gzip(gz_name, text_data):
                        os.remove(f_name)
                # 检查html文件
                if os.path.exists(f_name + '.html'):
                    html_data = open_file(f_name + '.html')
                    if len(html_data) > 0:
                        if save_gzip(gz_html, html_data):
                            os.remove(f_name + '.html')
                    else:
                        os.remove(f_name + '.html')
                pass
            elif os.path.exists(gz_name) and os.path.getsize(gz_name) > 50:
                pass
            elif self.is_free_limit == '-1' and v_vip == '1':
                # print('is_free_limit = %s' % self.is_free_limit)
                pass
            else:
                title, text, html = get_volume(v_url)
                print('download <%s> ---> %s' % (self.book_name, title))
                # save_file(f_name,text)
                save_gzip(gz_name, text)
                is_new = True
                if os.path.exists('savehtml.config') or os.path.exists('save_html.config'):
                    # save_file(f_name+'.html',html)
                    save_gzip(gz_html, html)

        # save_file(i_name, info_str)
        if os.path.exists(i_name):
            os.remove(i_name)
        save_gzip(i_name+'.gz', info_str)
        join_file_path = path_format(self.dir_path+'\\'+self.book_name+'.txt')
        if is_new or not os.path.exists(join_file_path+'.gz'):
            join_text_gz(join_file_path+'.gz', file_list)
            print('download <%s> fin,join file to %s' % (self.book_name, join_file_path+'.gz'))
        # 没有更新但是有txt文件存在，打包删除txt
        if os.path.exists(join_file_path):
            if save_gzip(join_file_path+'.gz',open_file(join_file_path)):
                os.remove(join_file_path)
        else:
            print('download <%s> fin' % self.book_name)


def start_xm():

    this_path = get_path()

    book_id_list = get_limit_list_from_qidian()

    tasks = []
    for info in book_id_list:
        book_name = info['name']
        book_id = info['id']

        book_path = this_path+'\\'+book_name
        # 整理过的的json，原始json，是否限免
        book_info_data, book_info_json, is_free_limit = get_book_volume_info_json(book_id)

        t = DownloadBook(book_name, book_info_data, book_info_json, book_path, is_free_limit)
        t.start()
        tasks.append(t)
    for task in tasks:
        if task.isAlive():
            task.join()


def main():
    while True:
        start_xm()
        print('sleep 7200秒')
        time.sleep(7200)
        os.system('cls')

if __name__ == "__main__":
    main()
