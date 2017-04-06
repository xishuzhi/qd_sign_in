from threading import Thread
import os
import time
import random
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
    def __init__(self,book_name,book_volumes_json,dir_path,qdf = qd_func,qdr=qd_QDReader):
        Thread.__init__(self)
        self.book_name = book_name
        self.book_volumes_json = book_volumes_json
        self.dir_path = dir_path
        self.qd_func = qdf
        self.qd_QDReader = qdr
    def run(self):
        if not os.path.exists(self.dir_path):
            os.mkdir(self.dir_path)
        print('start download <%s>' % self.book_name )
        for i in self.book_volumes_json:
            #{'v_name': volume_name, 'v_cid': volume_cid, 'v_vip': volume_vip, 'v_url': volume_url}
            #print(i)
            v_name = i['v_name']
            v_url = i['v_url']
            f_name = self.dir_path+'\\'+self.qd_func.replace_file_path(v_name)+'.txt'
            if os.path.exists(f_name) and os.path.getsize(f_name) > 100:
                pass
            else:
                tital, text, html = self.qd_func.get_volume(v_url)
                self.qd_func.save_file(f_name,text)
                self.qd_func.save_file(f_name+'.html',html)
        print('download <%s> fin' % self.book_name )

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
    elif os.name == 'Android':
        path = path_linux(path)
    return path
def getPath():
    path = './'
    if os.name == 'nt':
        path = os.getcwd()
    elif os.name == 'Android':
        path = '/storage/emulated/0/qpython/scripts3'
    return path
# def main():
#     # thisPath = getPath()
#     # free_list = qd_func.get_limit_list()
#     # tasks = []
#     # for i in free_list:
#     #     book_name = i['name']
#     #     book_url = i['url']
#     #     print('-----------s')
#     #     book_info, book_volume = qd_func.get_volume_list(book_url)
#     #     print('book_info')
#     #     print(book_info)
#     #     # print('book_volume')
#     #     # print(book_volume)
#     #     print('-----------e')
#     #     #print(vlist)
#     #
#     #     t = downloadbook(book_name,book_info,thisPath+'\\'+book_name)
#     #     t.start()
#     #     tasks.append(t)
#     # for task in tasks:
#     #     if task.isAlive():
#     #         task.join()
#     j = qd_QDReader.getBookInfoData(1001375918)
#     print(j)
#
#
# # #print(tasks)
# # blocks = 6
# # task_count = blocks
# # task_index = 0
# # tasks = []
# # threads = []
# # for i in range(30):
# #     t = downloadbook(str(i))
# #     tasks.append(t)
# # tasks.reverse()
# #
# # while len(tasks) > 0 or len(threads) > 0:
# #     if len(threads) < blocks and len(tasks) > 0:
# #         t = tasks.pop()
# #         t.start()
# #         threads.append(t)
# #         task_index += 1;
# #     for i in threads:
# #         if not i.isAlive():
# #             threads.remove(i)
# #             break
# # print('ooooooo')
    # book_id = 3600493
    # book_info_json = qd_QDReader.getBookInfoData(book_id)
    # Data = book_info_json['Data']
    # Volumes = Data['Volumes']
    # Chapters = Data['Chapters']
    # book_info_data = []
    # for c in Chapters:
    #     volume_name = c['n']
    #     volume_cid = c['c']
    #     volume_vip = c['v']
    #     volume_url =  'https://vipreader.qidian.com/chapter/%s/%s' % (book_id,volume_cid)
    #     if volume_cid > 0:
    #         book_info_data.append({'v_name':volume_name,'v_cid':volume_cid,'v_vip':volume_vip,'v_url':volume_url})
    #     #print('章节名：%s，章节ID：%s，vip：%s' % (volume_name,volume_cid,volume_vip))
    # print(book_info_data)

def main():
    # r = 'https://vipreader.qidian.com/chapter/%s/%s'
    thisPath = getPath()
    book_id_list = qd_QDReader.get_limit_list()
    #print(book_id_list)
    tasks = []
    for info in book_id_list:
        book_name = info['name']
        book_id = info['id']
        book_url = info['url']
        book_path = thisPath+'\\'+book_name
        book_info_list = qd_QDReader.getBookVolumeInfoJson(book_id)
        # print('name=%s,id=%s,url=%s,path=%s,list=%s' % (book_name,book_id,book_url,book_path,book_info_list))
        # print(book_info_list)
        t = downloadbook_by_json(book_name,book_info_list,book_path)
        t.start()
        tasks.append(t)
    for task in tasks:
        if task.isAlive():
            task.join()






if __name__ == "__main__":
    main()
    # l = qd_QDReader.getBookVolumeInfoJson(3656301)
    # print(l)