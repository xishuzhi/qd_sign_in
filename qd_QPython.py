from qd_utils import *
from threading import Thread


class downloadbook_by_json(Thread):
    def __init__(self,book_name,book_volumes_json,book_info_json,dir_path):
        Thread.__init__(self)
        self.book_name = book_name
        self.book_volumes_json = book_volumes_json
        self.book_info_json = book_info_json
        self.dir_path = dir_path

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
    def __init__(self,book_name,book_volumes_json,book_info_json,dir_path):
        Thread.__init__(self)
        self.book_name = book_name
        self.book_volumes_json = book_volumes_json
        self.book_info_json = book_info_json
        self.dir_path = dir_path

    def run(self):
        self.dir_path = path_format(self.dir_path)
        if not os.path.exists(self.dir_path):
            os.mkdir(self.dir_path)
        print('start download <%s>' % self.book_name )
        #save_file(self.dir_path+'\\'+'info_json.txt',str(self.book_info_json))
        #save_file(self.dir_path + '\\' + 'volumes_json.txt', str(self.book_volumes_json))

        if os.path.exists(self.dir_path+'\\'+'info_json.txt'):
            if save_gzip(self.dir_path + '\\' + 'info_json.txt.gz', str(self.book_info_json)):
                os.remove(self.dir_path+'\\'+'info_json.txt')
        self.book_volumes_json.sort(key=lambda x:(x['count'],-x['count']))
        if os.path.exists(self.dir_path + '\\' + 'volumes_json.txt'):
            if save_gzip(self.dir_path + '\\' + 'volumes_json.txt.gz', str(self.book_volumes_json)):
                os.remove(self.dir_path + '\\' + 'volumes_json.txt')

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
            gz_name = self.dir_path + '\\' + str(v_cid) + '.txt.gz'
            gz_html = self.dir_path + '\\' + str(v_cid) + '.txt.html.gz'
            f_name = path_format(f_name)
            gz_name = path_format(gz_name)
            gz_html = path_format(gz_html)
            file_list.append(f_name)
            i_name = self.dir_path + '\\book_info.txt'
            i_name = path_format(i_name)
            info_str += '%s.txt ---> %s\n' % (str(v_cid),v_name)
            if os.path.exists(f_name) and os.path.getsize(f_name) > 100:
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
                pass
            elif os.path.exists(gz_name) and os.path.getsize(gz_name) > 100:
                pass
            else:
                tital, text, html = get_volume(v_url)
                print('download <%s> ---> %s' % (self.book_name,tital))
                #save_file(f_name,text)
                save_gzip(gz_name,text)
                isNew = True
                if os.path.exists('save_html.config'):
                    #save_file(f_name+'.html',html)
                    save_gzip(gz_html,html)

        #save_file(i_name, info_str)
        save_gzip(i_name+'.gz', info_str)
        joinFilePath = self.dir_path+'\\'+self.book_name+'.txt'
        joinFilePath = path_format(joinFilePath)
        if isNew:
            #join_text(joinFilePath,file_list)
            join_text_gz(joinFilePath+'.gz',file_list)
            print('download <%s> fin,join file to %s' % (self.book_name,joinFilePath+'.gz'))
        if os.path.exists(joinFilePath):
            if save_gzip(joinFilePath+'.gz',open_file(joinFilePath)):
                os.remove(joinFilePath)
        else:
            print('download <%s> fin' % (self.book_name))

def start_by_id(book_id):
    book_info_data, book_info_json = getBookVolumeInfoJson(book_id)
    book_name = book_info_json['Data']['BookName']
    book_path = getPath()+'\\'+book_name
    book_path = path_format(book_path)
    #t = downloadbook_by_json(book_name, book_info_data, book_info_json, book_path)
    t = downloadbook_to_gzip(book_name, book_info_data, book_info_json, book_path)
    t.start()
    t.join()


def start_xm():
    # r = 'https://vipreader.qidian.com/chapter/%s/%s'
    thisPath = getPath()
    book_id_list = get_limit_list()
    #print(book_id_list)
    tasks = []
    for info in book_id_list:
        book_name = info['name']
        book_id = info['id']
        book_url = info['url']
        book_path = thisPath+'\\'+book_name
        book_info_data, book_info_json = getBookVolumeInfoJson(book_id)
        # print('name=%s,id=%s,url=%s,path=%s,list=%s' % (book_name,book_id,book_url,book_path,book_info_list))
        # print(book_info_list)
        t = downloadbook_to_gzip(book_name,book_info_data,book_info_json,book_path)
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

