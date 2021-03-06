from qd_utils import *
from threading import Thread
from sys import exit

class downloadbook_by_json(Thread):
    def __init__(self,book_name,book_volumes_json,book_info_json,dir_path,is_free_limit=-1):
        Thread.__init__(self)
        self.book_name = book_name
        self.book_volumes_json = book_volumes_json
        self.book_info_json = book_info_json
        self.dir_path = dir_path
        self.is_free_limit = is_free_limit

    def run(self):
        self.dir_path = path_format(self.dir_path)
        if not os.path.exists(self.dir_path):
            os.mkdir(self.dir_path)
        print('start download <%s>' % self.book_name )
        save_file(self.dir_path+'\\'+'info_json.txt',str(self.book_info_json))
        self.book_volumes_json.sort(key=lambda x:(x['count'],-x['count']))
        save_file(self.dir_path + '\\' + 'volumes_json.txt', str(self.book_volumes_json))
        info_str = self.book_name+'\n'
        file_list = []
        isNew = False
        for i in self.book_volumes_json:
            #{'v_name': volume_name, 'v_cid': volume_cid, 'v_vip': volume_vip, 'v_url': volume_url}
            #print(i)
            v_name = i['v_name']
            v_url = i['v_url']
            v_cid = i['v_cid']
            #f_name = self.dir_path+'\\'+self.qd_func.replace_file_path(v_name)+'.txt'
            f_name = self.dir_path + '\\' + str(v_cid) + '.txt'
            f_name = path_format(f_name)
            file_list.append(f_name)
            i_name = self.dir_path + '\\book_info.txt'
            i_name = path_format(i_name)
            info_str += '%s.txt ---> %s\n' % (str(v_cid),v_name)
            if os.path.exists(f_name) and os.path.getsize(f_name) > 0:
                #print('pass <%s> ---> %s' % (self.book_name,v_name))
                pass
            else:
                tital, text, html = get_volume(v_url)
                print('download <%s> ---> %s' % (self.book_name,tital))
                save_file(f_name,text)
                isNew = True
                if os.path.exists('save_html.config'):
                    save_file(f_name+'.html',html)
        save_file(i_name, info_str)
        joinFilePath = self.dir_path+'\\'+self.book_name+'.txt'
        joinFilePath = path_format(joinFilePath)
        if isNew:
            join_text(joinFilePath,file_list);
            print('download <%s> fin,join file to %s' % (self.book_name,joinFilePath))
        else:
        #print(file_list)
            print('download <%s> fin' % (self.book_name))

class downloadbook_to_gzip(Thread):
    def __init__(self,book_name,book_volumes_json,book_info_json,dir_path,is_free_limit=-1):
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
        print('start download <%s>' % self.book_name )
        #save_file(self.dir_path+'\\'+'info_json.txt',str(self.book_info_json))
        #save_file(self.dir_path + '\\' + 'volumes_json.txt', str(self.book_volumes_json))
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
        isNew = False
        for i in self.book_volumes_json:
            #{'v_name': volume_name, 'v_cid': volume_cid, 'v_vip': volume_vip, 'v_url': volume_url}
            #print(i)
            v_name = i['v_name']
            v_url = i['v_url']
            v_cid = i['v_cid']
            v_vip = str(i['v_vip'])
            #print('v_vip = %s,type=%s'% (v_vip,type(v_vip)))
            #f_name = self.dir_path+'\\'+self.qd_func.replace_file_path(v_name)+'.txt'
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
                info_str += '%s.txt ---> %s (VIP)\n' % (str(v_cid),v_name)
            else:
                info_str += '%s.txt ---> %s\n' % (str(v_cid), v_name)
            if os.path.exists(f_name) and os.path.getsize(f_name) > 100 or os.path.exists(f_name+'.html') and os.path.getsize(f_name+'.html') > 100:
                #print('pass <%s> ---> %s' % (self.book_name,v_name))
                text_data = open_file(f_name)
                # 检查txt文件
                if len(text_data) > 0:
                    if save_gzip(gz_name,text_data):
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
                #print('is_free_limit = %s' % self.is_free_limit)
                pass
            else:
                tital, text, html = get_volume(v_url)
                print('download <%s> ---> %s' % (self.book_name,tital))
                #save_file(f_name,text)
                save_gzip(gz_name,text)
                isNew = True
                if os.path.exists('savehtml.config') or os.path.exists('save_html.config'):
                    #save_file(f_name+'.html',html)
                    save_gzip(gz_html,html)

        #save_file(i_name, info_str)
        if os.path.exists(i_name):
            os.remove(i_name)
        save_gzip(i_name+'.gz', info_str)
        joinFilePath = self.dir_path+'\\'+self.book_name+'.txt'
        joinFilePath = path_format(joinFilePath)
        if isNew or not os.path.exists(joinFilePath+'.gz'):
            #join_text(joinFilePath,file_list)
            join_text_gz(joinFilePath+'.gz',file_list)
            print('download <%s> fin,join file to %s' % (self.book_name,joinFilePath+'.gz'))
        # 没有更新但是有txt文件存在，打包删除txt
        if os.path.exists(joinFilePath):
            if save_gzip(joinFilePath+'.gz',open_file(joinFilePath)):
                os.remove(joinFilePath)
        else:
            print('download <%s> fin' % (self.book_name))

import zipfile
class downloadbook_to_zip(Thread):
    def __init__(self,book_name,book_volumes_json,book_info_json,dir_path,is_free_limit=-1):
        Thread.__init__(self)
        self.book_name = book_name
        self.book_volumes_json = book_volumes_json
        self.book_info_json = book_info_json
        self.dir_path = dir_path
        self.is_free_limit = str(is_free_limit)
        self.zip = None
    def run(self):
        self.dir_path = path_format(self.dir_path)
        zipFilePath = self.dir_path + '\\' + self.book_name + '.zip'
        if not os.path.exists(self.dir_path):
            os.mkdir(self.dir_path)
            self.zip = zipfile.ZipFile(zipFilePath, 'w')
        else:
            self.zip = zipfile.ZipFile(zipFilePath, 'a')
        if self.zip == None:
            pass
        namelist = self.zip.namelist()
        if 'f1.txt' in namelist:
            print('find f1.txt')
        print('start download <%s>' % self.book_name )
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
        isNew = False
        for i in self.book_volumes_json:
            v_name = i['v_name']
            v_url = i['v_url']
            v_cid = i['v_cid']
            v_vip = str(i['v_vip'])
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
                info_str += '%s.txt ---> %s (VIP)\n' % (str(v_cid),v_name)
            else:
                info_str += '%s.txt ---> %s\n' % (str(v_cid), v_name)
            if os.path.exists(f_name) and os.path.getsize(f_name) > 100 or os.path.exists(f_name+'.html') and os.path.getsize(f_name+'.html') > 100:
                text_data = open_file(f_name)
                # 检查txt文件
                if len(text_data) > 0:
                    if save_gzip(gz_name,text_data):
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
                #print('is_free_limit = %s' % self.is_free_limit)
                pass
            else:
                tital, text, html = get_volume(v_url)
                print('download <%s> ---> %s' % (self.book_name,tital))

                save_gzip(gz_name,text)
                isNew = True
                if os.path.exists('savehtml.config') or os.path.exists('save_html.config'):

                    save_gzip(gz_html,html)

        #save_file(i_name, info_str)
        if os.path.exists(i_name):
            os.remove(i_name)
        save_gzip(i_name+'.gz', info_str)
        joinFilePath = self.dir_path+'\\'+self.book_name+'.txt'
        joinFilePath = path_format(joinFilePath)
        if isNew or not os.path.exists(joinFilePath+'.gz'):
            #join_text(joinFilePath,file_list)
            join_text_gz(joinFilePath+'.gz',file_list)
            print('download <%s> fin,join file to %s' % (self.book_name,joinFilePath+'.gz'))
        # 没有更新但是有txt文件存在，打包删除txt
        if os.path.exists(joinFilePath):
            if save_gzip(joinFilePath+'.gz',open_file(joinFilePath)):
                os.remove(joinFilePath)
        else:
            print('download <%s> fin' % (self.book_name))

def start_by_id(book_id):
    book_info_data, book_info_json, is_free_limit = getBookVolumeInfoJson(book_id)
    if book_info_json['Message'] == '成功':
        book_name = book_info_json['Data']['BookName']
        book_path = getPath()+'\\'+book_name
        book_path = path_format(book_path)
        #t = downloadbook_by_json(book_name, book_info_data, book_info_json, book_path)
        t = downloadbook_to_gzip(book_name, book_info_data, book_info_json, book_path,is_free_limit)
        t.start()
        t.join()


def start_by_id_list(book_id_list,block = 6):
    tasks = []
    thread_run = []
    for id in book_id_list:
        pass
        book_info_data, book_info_json, is_free_limit = getBookVolumeInfoJson(id)
        book_name = book_info_json['Data']['BookName']
        book_path = getPath()+'\\'+book_name
        book_path = path_format(book_path)
        t = downloadbook_to_gzip(book_name, book_info_data, book_info_json, book_path,is_free_limit)
        tasks.append(t)
    while len(thread_run) > 0 or len(tasks) > 0:
        if len(thread_run) < block and len(tasks) > 0:
            task = tasks.pop()
            thread_run.append(task)
            task.start()
        for i in thread_run:
            if not i.isAlive():
                thread_run.remove(i)
def start_by_list_file():
    path = getPath()+'\\list.txt'
    list_path = path_format(path)
    print('查找%s文件' % list_path)
    if os.path.exists(list_path):
        txt = open_file(list_path)
        id_list = parse_id_str(txt)
        start_by_id_list(id_list)
    else:
        print('找不到list.txt文件')

def parse_id_str(txt):
    id_list = []
    if len(txt) > 0:
        list = txt.split('\n')
        list2 = txt.split(',')
        for i in list:
            if i.isdigit() and int(i) > 0:
                id_list.append(i)
        for j in list2:
            if j.isdigit() and int(j) > 0:
                id_list.append(j)
    return id_list


def start_xm():
    # r = 'https://vipreader.qidian.com/chapter/%s/%s'
    thisPath = getPath()
    #book_id_list = get_limit_list()
    book_id_list = get_limit_list_from_qidian()
    #print(book_id_list)
    tasks = []
    for info in book_id_list:
        book_name = info['name']
        book_id = info['id']
        book_url = info['url']
        book_path = thisPath+'\\'+book_name
        #整理过的的json，原始json，是否限免
        book_info_data, book_info_json, is_free_limit = getBookVolumeInfoJson(book_id)
        # print('name=%s,id=%s,url=%s,path=%s,list=%s' % (book_name,book_id,book_url,book_path,book_info_list))
        # print(book_info_list)
        t = downloadbook_to_gzip(book_name, book_info_data, book_info_json, book_path, is_free_limit)
        t.start()
        tasks.append(t)
    for task in tasks:
        if task.isAlive():
            task.join()

def menu():
    #os.popen('cls')
    #os.system('cls')
    print('输入书籍ID下载：')
    print('输入多个ID下载，以,分隔：')
    print('输f下载当前限免书籍：')
    print('输t定时下载限免书籍')
    print('输l下载list.txt中的书籍：')
    print('x. 退出')
    selection = input('输入书籍ID：')
    return selection

def start_main():
    try:
        while True:
            selection = menu()
            s_l = str(selection).split(',')
            if selection.isdigit() and int(selection) > 0:
                start_by_id(selection)
            elif selection == 'f' or selection == 'F':
                start_xm()
            elif selection == 't' or selection == 'T':
                while True:
                    start_xm()
                    print('sleep 7200秒')
                    time.sleep(7200)
                    os.system('cls')
            elif selection == 'l' or selection == 'L':
                start_by_list_file()
            elif selection == 'x' or selection == 'X':
                exit(0)
            elif len(s_l) > 0:
                id_list = []
                for i in s_l:
                    if i.isdigit() and int(i) > 0:
                        id_list.append(i)
                start_by_id_list(id_list)
            else:
                print('输入错误！')
        print ('exit')
    except Exception as e:
        print ('Error: %s,%s' % (selection,e))
        return start_main()
    finally:
        pass


class start_xm_thread(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        start_xm()


def main():
    if os.path.exists('autodownload.config') or os.path.exists('auto_download.config'):
        start_xm()
        start_main()
    elif os.path.exists('t.config'):
        t = start_xm_thread()
        while True:
            # start_xm()
            if not t.isAlive():
                t.start()
                t.join()
                print('sleep 7200秒')
                time.sleep(7200)
                os.system('cls')
    else:
        start_main()
if __name__ == "__main__":
    main()
    # print(get_limit_list_from_qidian())
    # book_info_data, book_info_json, is_free_limit = getBookVolumeInfoJson(1004927985)
    # print(book_info_data)
    #print(book_info_json)
    #print(book_info_data)


