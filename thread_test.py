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
        if not os.path.exists(self.dir_path):
            os.mkdir(self.dir_path)
        print('start download <%s>' % self.book_name )
        qd_func.save_file(self.dir_path+'\\'+'info_json.txt',str(self.book_info_json))
        self.book_volumes_json.sort(key=lambda x:(x['count'],-x['count']))
        qd_func.save_file(self.dir_path + '\\' + 'volumes_json.txt', str(self.book_volumes_json))
        info_str = self.book_name+'\n'
        file_list = []
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
                if os.path.exists('save_html.config'):
                    self.qd_func.save_file(f_name+'.html',html)
        self.qd_func.save_file(i_name, info_str)
        joinFilePath = self.dir_path+'\\'+self.book_name+'.txt'
        joinFilePath = qd_func.path_format(joinFilePath)
        qd_QDReader.join_text(joinFilePath,file_list);
        #print(file_list)
        print('download <%s> fin,join file to %s' % (self.book_name,joinFilePath))





def main():
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






if __name__ == "__main__":
    main()
    # # l = qd_QDReader.getBookVolumeInfoJson(3656301)
    # #print(l)
    # # str = '\ue844'
    # #https://vipreader.qidian.com/chapter/1001375918/343107854
    # # print(str)
    # tital, text, html = qd_func.get_volume('https://read.qidian.com/chapter/TXY5K4Ri046t-wSl2uB4dQ2/b-OnWqsDpEG2uJcMpdsVgA2')
    # #\u3000
    # print(html)
    # qd_func.save_file('test.html',html)
    # if html.find('　') > 0:
    #     print('hehe')
    # # for x in range(0xff01, 0xff7f):
    # #     print(x)
    # # _tbl = dict((x, x - 0xff00 + 0x20) for x in range(0xff01, 0xff7f))
    # # print(_tbl)