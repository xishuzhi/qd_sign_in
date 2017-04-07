#-*- coding：utf-8 -*-
from threading import Thread
import os
import qd_func
import qd_QDReader

class downloadbook(Thread):
    def __init__(self,book_name,book_volumes,dir_path,qd = qd_func):
        Thread.__init__(self)
        self.book_name = book_name
        self.book_volumes = book_volumes
        self.dir_path = dir_path
        self.qd = qd
    def run(self):
        if not os.path.exists(self.dir_path):
            os.mkdir(self.dir_path)
        print('start download <%s>' % self.book_name )
        for i in self.book_volumes:
            #print(i)
            v_name = i['name']
            v_url = i['url']
            f_name = self.dir_path+'\\'+self.qd.replace_file_path(v_name)+'.txt'
            if os.path.exists(f_name) and os.path.getsize(f_name) > 100:
                pass
            else:
                tital, text, html = self.qd.get_volume(v_url)
                self.qd.save_file(f_name,text)
                self.qd.save_file(f_name+'.html',html)
        print('download <%s> fin' % self.book_name )

class downloadbook_by_json(Thread):
    def __init__(self,book_name,book_volumes_json,book_info_json,dir_path,qdf = qd_func,qdr=qd_QDReader):
        Thread.__init__(self)
        self.book_name = book_name
        self.book_volumes_json = book_volumes_json
        self.book_info_json = book_info_json
        self.dir_path = dir_path
        self.qd_func = qdf
        self.qd_QDReader = qdr
    def run(self):
        self.dir_path = qd_func.path_format(self.dir_path)
        if not os.path.exists(self.dir_path):
            os.mkdir(self.dir_path)
        print('start download <%s>' % self.book_name )
        qd_func.save_file(self.dir_path+'\\'+'info_json.txt',str(self.book_info_json))
        self.book_volumes_json.sort(key=lambda x:(x['count'],-x['count']))
        qd_func.save_file(self.dir_path + '\\' + 'volumes_json.txt', str(self.book_volumes_json))
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
            f_name = qd_func.path_format(f_name)
            file_list.append(f_name)
            i_name = self.dir_path + '\\book_info.txt'
            i_name = qd_func.path_format(i_name)
            info_str += '%s.txt ---> %s\n' % (str(v_cid),v_name)
            if os.path.exists(f_name) and os.path.getsize(f_name) > 0:
                #print('pass <%s> ---> %s' % (self.book_name,v_name))
                pass
            else:
                tital, text, html = self.qd_func.get_volume(v_url)
                print('download <%s> ---> %s' % (self.book_name,tital))
                self.qd_func.save_file(f_name,text)
                isNew = True
                if os.path.exists('save_html.config'):
                    self.qd_func.save_file(f_name+'.html',html)
        self.qd_func.save_file(i_name, info_str)
        joinFilePath = self.dir_path+'\\'+self.book_name+'.txt'
        joinFilePath = qd_func.path_format(joinFilePath)
        if isNew:
            qd_QDReader.join_text(joinFilePath,file_list);
            print('download <%s> fin,join file to %s' % (self.book_name,joinFilePath))
        else:
        #print(file_list)
            print('download <%s> fin' % (self.book_name))


def start_by_id(book_id):
    book_info_data, book_info_json = qd_QDReader.getBookVolumeInfoJson(book_id)
    book_name = book_info_json['Data']['BookName']
    book_path = qd_func.getPath()+'\\'+book_name
    book_path = qd_func.path_format(book_path)
    t = downloadbook_by_json(book_name, book_info_data, book_info_json, book_path)
    t.start()
    t.join()


def start_xm():
    # r = 'https://vipreader.qidian.com/chapter/%s/%s'
    thisPath = qd_func.getPath()
    book_id_list = qd_QDReader.get_limit_list()
    #print(book_id_list)
    tasks = []
    for info in book_id_list:
        book_name = info['name']
        book_id = info['id']
        book_url = info['url']
        book_path = thisPath+'\\'+book_name
        book_info_data, book_info_json = qd_QDReader.getBookVolumeInfoJson(book_id)
        # print('name=%s,id=%s,url=%s,path=%s,list=%s' % (book_name,book_id,book_url,book_path,book_info_list))
        # print(book_info_list)
        t = downloadbook_by_json(book_name,book_info_data,book_info_json,book_path)
        t.start()
        tasks.append(t)
    for task in tasks:
        if task.isAlive():
            task.join()

def menu():
    #os.popen('cls')
    #os.system('cls')
    print ('输入书籍ID下载：')
    print('输f下载当前限免书籍：')
    print ('x. 退出')
    selection = input('输入书籍ID：')
    return selection
def start_main():
    try:
        while True:
            selection = menu()
            if selection.isdigit() and int(selection) > 0:
                start_by_id(selection)
            elif selection == 'f' or selection == 'F':
                start_xm()
                break
            elif selection == 'x' or selection == 'X':
                break
            else:
                print('输入错误！')
        print ('exit')
    except Exception as e:
        print ('Error: %s,%s' % (selection,e))
    pass


def main():
    if os.path.exists('autodownload.config'):
        start_xm()
    else:
        start_main()
if __name__ == "__main__":
    main()
