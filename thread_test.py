from threading import Thread
import os
import time
import random
import qd_func
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
def main():
    thisPath = getPath()
    free_list = qd_func.get_limit_list()
    for i in free_list:
        book_name = i['name']
        book_url = i['url']


# #print(tasks)
# blocks = 6
# task_count = blocks
# task_index = 0
# tasks = []
# threads = []
# for i in range(30):
#     t = downloadbook(str(i))
#     tasks.append(t)
# tasks.reverse()
#
# while len(tasks) > 0 or len(threads) > 0:
#     if len(threads) < blocks and len(tasks) > 0:
#         t = tasks.pop()
#         t.start()
#         threads.append(t)
#         task_index += 1;
#     for i in threads:
#         if not i.isAlive():
#             threads.remove(i)
#             break
# print('ooooooo')

if __name__ == "__main__":
    main()