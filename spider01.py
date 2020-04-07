from selenium import webdriver
from time import sleep
from lxml import html
import csv
path = r'C:\Users\leon\Desktop\spider.csv'


etree = html.etree
browser = webdriver.Chrome(r'C:\Users\leon\Desktop\other\chromedriver.exe')
tot = 0

# 拿到每一页的URL，每页有20条记录
def get_pages():
    pages = 1125
    max_offset = (pages-1) * 20
    start_offset = 0

    while start_offset < max_offset:
        tmp = start_offset
        url = 'https://www.cnvd.org.cn/flaw/typeResult?typeId=29&max=20&offset='+str(tmp)
        browser.get(url)
        sleep(8)
        page_text = browser.page_source
        yield page_text
        start_offset += 20

# 拿到每一条信息详情页的源码

def get_info(url_list):

    for it in url_list:
        print('get it',it)
        browser.get(it)
        sleep(5)
        yield browser.page_source


# 提取网页中需要的字段信息
def get_dic(tree):

    body = tree.xpath('//tbody')[0]

    dic = {}

    # cnvd-id

    name = body.xpath('./tr[1]/td[1]/text()')[0]
    val = body.xpath('./tr[1]/td[2]/text()')[0]
    val = val.strip()
    dic[name] = val

    # 公开日期
    name = body.xpath('./tr[2]/td[1]/text()')[0]
    val = body.xpath('./tr[2]/td[2]/text()')[0]
    val = val.strip()
    dic[name] = val

    # 危险级别
    name = body.xpath('./tr[3]/td[1]/text()')[0]
    val = body.xpath('./tr[3]/td[2]/text()')[1]
    val = val.strip().split()[0]
    dic[name] = val

    # 影响产品
    name = body.xpath('./tr[4]/td[1]/text()')[0]
    val = body.xpath('./tr[4]/td[2]/text()')
    b = [it.strip() for it in val]
    val = ''.join(b)
    dic[name] = val

    # 漏洞描述
    name = body.xpath('./tr[5]/td[1]/text()')[0]
    val = body.xpath('./tr[5]/td[2]/text()')
    b = [it.strip() for it in val]
    val = ''.join(b)
    dic[name] = val

    # 漏洞类型
    name = body.xpath('./tr[6]/td[1]/text()')[0]
    val = body.xpath('./tr[6]/td[2]/text()')[0].strip()
    dic[name] = val

    # 漏洞解决方案
    name = body.xpath('./tr[8]/td[1]/text()')[0]
    val = body.xpath('./tr[8]/td[2]/text()')
    b = [it.strip() for it in val]
    val = ''.join(b)
    dic[name] = val
    return dic


# 将得到的字典写入log文件
def write_to_file(dic):
    global tot
    a = []
    for it in dic.keys():
        newstr = str(it) + " : " + str(dic[it])
        a.append(newstr)

    with open(path, 'a', encoding='utf-8') as fp:
        mywriter = csv.writer(fp)
        mywriter.writerow(a)


    print(tot, ':write successfully')
    print(dic)
    print('-----------------------------')
    tot += 1


for it in get_pages():
    tree = etree.HTML(it)
    tmp_list = tree.xpath("//tr//a/@href")
    url_list = [ 'https://www.cnvd.org.cn'+it for it in tmp_list]

    for it in get_info(url_list):
        new_tree = etree.HTML(it)
        dic = get_dic(new_tree)
        write_to_file(dic)










