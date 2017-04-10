import tarfile
from io import StringIO
from io import BytesIO
from os import path


class JsonFormatter:
  def __init__(self,intend=4,name=""):
    self.name=name
    self.intend=intend
    self.stack=[]
    self.obj=None
    self.source=self.get_source(name)
    self.prepare()
  @staticmethod
  def json_str(s):
    return '"'+s+'"'
  @staticmethod
  def get_source(name):
    with open(name,'r') as f:
      return ''.join(f.read().split())
  def prepare(self):
    try:
      self.obj=eval(self.source)
    except:
      raise Exception('Invalid json string!')
  def line_intend(self,level=0):
    return '\n'+' '*self.intend*level
  def parse_dict(self,obj=None,intend_level=0):
    self.stack.append(self.line_intend(intend_level)+'{')
    intend_level+=1
    for key,value in obj.items():
      key=self.json_str(str(key))
      self.stack.append(self.line_intend(intend_level)+key+':')
      self.parse(value,intend_level)
      self.stack.append(',')
    self.stack.append(self.line_intend(intend_level-1)+'}')
  def parse_list(self,obj=None,intend_level=0):
    self.stack.append(self.line_intend(intend_level)+'[')
    intend_level+=1
    for item in obj:
      self.parse(item,intend_level)
      self.stack.append(',')
    self.stack.append(self.line_intend(intend_level-1)+']')
  def parse(self,obj,intend_level=0):
    if obj is None:
      self.stack.append('null')
    elif obj is True:
      self.stack.append('true')
    elif obj is False:
      self.stack.append('false')
    elif isinstance(obj,(int,long,float)):
      self.stack.append(str(obj))
    elif isinstance(obj,str):
      self.stack.append(self.json_str(obj))
    elif isinstance(obj,(list,tuple)):
      self.parse_list(obj,intend_level)
    elif isinstance(obj,dict):
      self.parse_dict(obj,intend_level)
    else:
      raise Exception('Invalid json type %s!' % obj)
  def render(self):
    self.parse(self.obj,0)
    res_file='good'+self.name
    res=''.join(self.stack)
    with open(res_file,'w') as f:
      f.write(res)
    print (res)

def serve_file(request='t.tar.gz'):
    out = BytesIO()
    tar = tarfile.open(request,mode = "w:gz", fileobj = out)
    data = 'lala'.encode('utf-8')
    file = BytesIO(data)
    info = tarfile.TarInfo(name="1.txt")
    info.size = len(data)
    tar.addfile(tarinfo=info, fileobj=file)
    tar.close()

def tar_test():

    out = BytesIO()
    tar = tarfile.open('sample.tar.gz', 'w:gz', fileobj=out)
    data = 'lala'.encode('utf-8')
    file = BytesIO(data)
    info = tarfile.TarInfo(name="1.txt")
    info.size = len(data)
    tar.addfile(tarinfo=info, fileobj=file)
    for tarinfo in tar:
        print(tarinfo.name, "is", tarinfo.size, "bytes in size and is", end="")
        if tarinfo.isreg():
            print("a regular file.")
        elif tarinfo.isdir():
            print("a directory.")
        else:
            print("something else.")
    tar.close()
def tar_test2():
    with tarfile.open("sample.tar", "w") as tar:
        for name in ["foo", "bar", "quux"]:
            tar.add(name)
def save_tar_gz(tar_gz_name,file_name,file_data_bytes):
    info = tarfile.TarInfo(file_name)
    info.size = len(file_data_bytes)
    try:
        tar = tarfile.open(tar_gz_name, "w:gz")
        # if not path.exists(tar_gz_name):
        #     tar = tarfile.open(tar_gz_name, "w:gz")
        # else:
        #     tar = tarfile.open(tar_gz_name, "r|*")
        tar.addfile(info, BytesIO(file_data_bytes))
        # for tarinfo in tar:
        #     print(tarinfo.name, "is", tarinfo.size, "bytes in size and is", end="")
        #     if tarinfo.isreg():
        #         print("a regular file.")
        #     elif tarinfo.isdir():
        #         print("a directory.")
        #     else:
        #         print("something else.")
    except Exception as e:
        print('save_tar_gz error:%s' % e)


# !user/bin/env python3
# -*-coding : utf-8 -*-

import zipfile
from io import BytesIO
import os

u'''
Create zip file in memory.
'''
class InMemoryZIP(object):

    def __init__(self):
        # create the in-memory file-like object
        self.in_memory_zip = BytesIO()

    def append(self, filename_in_zip, file_contents):
        """ Appends a file with name filename_in_zip \
        and contents of file_contents to the in-memory zip.
        """
        # create a handle to the in-memory zip in append mode
        zf = zipfile.ZipFile(self.in_memory_zip, 'a',
                             zipfile.ZIP_DEFLATED, False)

        # write the file to the in-memory zip
        zf.writestr(filename_in_zip, file_contents)

        # mark the files as having been created on Windows
        # so that Unix permissions are not inferred as 0000
        for zfile in zf.filelist:
            zfile.create_system = 0
        return self

    def appendfile(self, file_path, file_name=None):
        """ Read a file with path file_path \
        and append to in-memory zip with name file_name.
        """
        if file_name is None:
            file_name = os.path.split(file_path)[1]

        f = open(file_path, 'rb')
        file_contents = f.read()
        self.append(file_name, file_contents)
        f.close()
        return self

    def read(self):
        """ Returns a string with the contents of the in-memory zip.
        """
        self.in_memory_zip.seek(0)
        return self.in_memory_zip.read()

    def writetofile(self, filename):
        """
        Write the in-memory zip to a file
        """
        f = open(filename, 'wb')
        f.write(self.read())
        f.close()

class zip(object):
    def __init__(self,zip_filename):
        self.in_memory_zip = BytesIO()
        self.zip_filename = zip_filename

    def append(self, filename_in_zip, file_contents):
        zf = zipfile.ZipFile(self.in_memory_zip, 'a', zipfile.ZIP_DEFLATED, False)
        zf.writestr(filename_in_zip, file_contents)
        # mark the files as having been created on Windows
        # so that Unix permissions are not inferred as 0000
        for zfile in zf.filelist:
            zfile.create_system = 0
        return self
from qd_utils import *
if __name__ == "__main__":
    pass
    # sta = """
    #
    #
    #
    # """
    # # print('start')
    # # # for i in range(22,42):
    # # #     save_tar_gz('t.tar.gz','000_%s.txt'%i,sta.encode('utf-8'))
    # # imz = InMemoryZIP()
    # # #imz.appendfile('a.txt').append('test.txt', 'This is content in test.txt')
    # # # for i in range(0,10):
    # # #     imz.append('test%s.txt'%i, sta)
    # # # imz.writetofile('test.zip')
    # # z = imz.read('test.zip')
    # # print()
    # #
    # # print('end')
    # getBookVolumeInfoJson(1004600033)
    # print()
    # jf = JsonFormatter(name="json.txt")
    # jf.render()
    str_txt = '32,33,34,54'
    print(str_txt.split())