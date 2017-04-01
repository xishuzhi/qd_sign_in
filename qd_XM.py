import json
from urllib import error,request
from bs4 import BeautifulSoup

def getByJson(id):
    try:
        url = 'https://book.qidian.com/ajax/book/category?_csrfToken=3nzlXYWwxZjUJPmUZyX8x0Zed1EBaizVQaOfPrwi&bookId=%s ' % id
        req = request.Request(url)
        req.add_header('Accept-encoding', 'gzip, deflate, sdch, br')
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3033.0 Safari/537.36')
        req.add_header('Accept-Language', 'zh-CN,zh;q=0.8')
        req.add_header('Cookie', 'stat_gid=8466091309; nread=2; nb=2; ns=2; _csrfToken=3nzlXYWwxZjUJPmUZyX8x0Zed1EBaizVQaOfPrwi; qdgd=1; statisticUUID=1488351430_34765; newstatisticUUID=1489378491_236948254; qdrs=0|2|2|1|1; lrbc=3536156%7C84866158%7C0%2C1003383443%7C316603456%7C1%2C3605783%7C95097080%7C1; rcr=3536156%2C1003383443%2C3605783%2C1004289255%2C3155120%2C1005007573%2C1003807527%2C1004166084%2C2782032%2C1005194988%2C1002959239%2C1004821729%2C1005001441%2C1005049162; hiijack=0; al=1; stat_sessid=19612237024; e1=%7B%22pid%22%3A%22qd_P_limitfree%22%2C%22eid%22%3A%22qd_E05%22%2C%22l1%22%3A5%7D; e2=%7B%22pid%22%3A%22qd_P_limitfree%22%2C%22eid%22%3A%22%22%2C%22l1%22%3A5%7D; ywkey=yw3894070335; ywguid=800001933406')
        req.add_header('X-Requested-With', 'XMLHttpRequest')
        req.add_header('Accept', 'application/json, text/javascript, */*; q=0.01')
        req.add_header('Host', 'book.qidian.com')
        response = request.urlopen(req)
        html_bytes = response.read()
        #print(html_bytes.decode('utf-8'))
        json_data = json.loads(html_bytes.decode('utf-8'))
        return json_data,html_bytes
    except error.URLError as e:
        print(e.reason)
def getBookInfoList(json_data):
    l = []
    for i in json_data['data']['vs']:
        # print(i)
        for j in i['cs']:
            #print(j)
            cN = j['cN']
            cU = j['cU']
            uuid = j['uuid']
            l.append({'name': cN, 'url': cU, 'uuid':uuid})
    return l

#从免费书列表中获取限免书籍信息
def get_limit_list():
    fp = request.urlopen("https://f.qidian.com/")
    html = fp.read()
    metaSoup = BeautifulSoup(html, "html.parser")
    # print(metaSoup)
    limit_list = metaSoup.find('div', attrs={'id': 'limit-list'})
    # print(limit_list)
    book_info_list = limit_list.findAll('div', attrs={'class': 'book-mid-info'})
    book = []
    for i in book_info_list:
        data = {'name':i.h4.get_text(),'url':'http:' + i.h4.a['href']+"#Catalog"}
        book.append(data)
    print(book)
    return book






if __name__ == '__main__':
    #main()
    pass