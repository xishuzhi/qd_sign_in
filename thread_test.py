from threading import Thread
import os
import time
import random
import qd_func
class downloadbook(Thread):
    def __init__(self,book_name,book_urls,dir_path,qd):
        Thread.__init__(self)
        self.name = book_name
        self.urls = book_urls
        self.dir_path = dir_path
        self.qd = qd
    def run(self):
        pass
        # t = random.randint(0,5)
        # print('run:%s,sleep=%s'% (self.name,t))
        # time.sleep(t)
        # print('stop:%s' % self.name)
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
    thisPath = './'
    if os.name == 'nt':
        thisPath = os.getcwd()
    elif os.name == 'Android':
        thisPath = '/storage/emulated/0/qpython/scripts3'
def main():

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