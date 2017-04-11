import zipfile
from qd_utils import *


def create_archive(path,name):
    zip_file_name = '%s\\%s.zip' % (path,name)
    os.chdir(path)
    #os.path.basename(name)
    zip = zipfile.ZipFile(zip_file_name, 'w')
    txt = get_html('https://f.qidian.com/')
    zip.writestr('%s.txt' % name, txt, compress_type=zipfile.ZIP_STORED)
    for html in os.listdir('.'):
        basename = os.path.basename(html)
        if basename.endswith('html'):
            zip.write(html, 'OEBPS/' + basename, compress_type=zipfile.ZIP_DEFLATED)
    zip.close()


def create_archive_url(path,zip_name,file_name,url):
    zip_file_name = '%s\\%s.zip' % (path,zip_name)
    os.chdir(path)
    #os.path.basename(name)
    txt = get_html(url)
    zip = zipfile.ZipFile(zip_file_name, 'w')
    zip.writestr(file_name, txt, compress_type=zipfile.ZIP_STORED)
    zip.close()
def add_archive_url(path,zip_name,file_name,url):
    zip_file_name = '%s\\%s.zip' % (path,zip_name)
    os.chdir(path)
    #os.path.basename(name)
    txt = get_html(url)
    zip = zipfile.ZipFile(zip_file_name, 'a')
    zip.writestr(file_name, txt, compress_type=zipfile.ZIP_STORED)
    zip.close()
def read_archive_url(path,zip_name,file_name):
    zip_file_name = '%s\\%s.zip' % (path,zip_name)
    os.chdir(path)
    #os.path.basename(name)

    zip = zipfile.ZipFile(zip_file_name, 'r')
    print(zip.infolist())
    print(zip.namelist())
    namelist = zip.namelist()
    if 'f1.txt' in namelist:
        print('find f1.txt')
    # t = zip.read(file_name)
    # print(t.decode('utf-8'))
    zip.close()
# create_archive_url(getPath(),'test.zip','f1.txt','https://book.qidian.com/info/1004150862')
# add_archive_url(getPath(),'test.zip','f2.txt','https://book.qidian.com/info/1004881070')
# add_archive_url(getPath(),'test.zip','f3.txt','https://book.qidian.com/info/3478880')
read_archive_url(getPath(),'test.zip','f1.txt')

