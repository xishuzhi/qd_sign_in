import tarfile
from io import StringIO
from io import BytesIO
from os import path
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
    sta = """
    [幻想未来] 未来之星际童话（一） BY： 来自远方


　　文案：

　　西历3021年，最后一次世界大战爆发，地球毁灭。

　　一批幸存者离开了家园到新的星球定居。新的种族，新的阶层产生。城市开始兴建，国家陆续崛起，不同的种族矛盾激化，社会秩序被重新确立……

　　从求生者到侵略者者的转变，只不过是一瞬间。

　　这是强者为尊的世界，适者生存。

　　商平从二十一世纪的地球重生到这个星球，醒过来的那一刻，命运就已经开始改变。

　　内容标签：强强灵魂转换宫廷侯爵天之骄子

　　搜索关键字：主角：商平┃配角：索兰·艾德里希，刘郗，奥斯汀┃其它：未来时空，战舰，星际战争

　　第一卷：毁灭与新生

　　第一章

　　地球历史进入三十一世纪，人类社会的发展日新月异，进入了高度繁荣的黄金时代。

　　G国物理学家马克·温斯顿将宇宙量子转换运用到改进宇宙航行器，使在不同的空间与亚空间中连接质点进行空间跳跃成为可能。人类不再拘囿于地球及周边的卫星，脚步开始遍及整个银河系，甚至开始向外太空延展。

　　“这是人类历史从未有过的高度繁荣时代，我为生存在这个时代而自豪。”——经济学家亚当·劳伦斯。

　　但是，高度的繁荣与飞速的发展，带来的不只是财富与繁荣，如同人类历史发展的每个阶段一样，金钱与权力开始从金字塔的顶端腐蚀，部分掌权者沉迷于眼前取得的成就，不思进取，沦陷在奢靡的享受与虚假的恭维之中。

　　腐败与堕落开始滋生，大国主义蔓延，小国的怨愤情绪增长，国与国之间的摩擦日渐加剧。

　　公元3021年夏历7月，最后一次世界大战爆发。

　　最初由J国挑起，随着争端的不断扩大，M国，N国，C国，R国等大国纷纷投入战争。

　　战乱迭起，全体人类都被卷入到了这场旷日持久的杀戮之中，不同的种族，不同的性别，不同的宗教，理性与秩序荡然无存，怜悯和宽恕都被摒弃，只有血腥与残杀才是最终的救赎。军队与平民再无界限，举起武器的那一刻，唯一的目的便是将眼前的敌人撕碎。

　　人，变成了野兽。

　　“既然无法生存下去，那么，就将一切都毁灭掉吧。”

　　一位哲学家，在侵略军闯进家中时，留下了这样一句话后饮弹自尽。

　　这句格言，奠定了整个地球悲剧的基调。

　　绝望与恐惧蔓延，贪婪残忍与暴虐全部挣脱了束缚，M国最先撕毁了禁用核武的条约，在第一颗核弹炸响的那一刻，潘多拉的匣子被打开了，破灭的乐章开始奏响……

　　公元3033年3月

　　地球，存在于宇宙几亿年的蓝色星球，最终走向了毁灭。

　　最后的幸存者，在宇宙飞船上亲眼见证了美丽母星毁灭的瞬间，蔚蓝色的、曾经孕育了几亿年生命的美丽星球，在爆炸声中，碎裂成了银河系中的粒粒尘埃。

　　遥望着被自己毁灭的家园，悔恨的泪水也无法洗去身上的罪孽，是他们亲手杀死了孕育他们的母亲……


    """
    # print('start')
    # # for i in range(22,42):
    # #     save_tar_gz('t.tar.gz','000_%s.txt'%i,sta.encode('utf-8'))
    # imz = InMemoryZIP()
    # #imz.appendfile('a.txt').append('test.txt', 'This is content in test.txt')
    # # for i in range(0,10):
    # #     imz.append('test%s.txt'%i, sta)
    # # imz.writetofile('test.zip')
    # z = imz.read('test.zip')
    # print()
    #
    # print('end')
    getBookVolumeInfoJson(1004600033)
    print()
