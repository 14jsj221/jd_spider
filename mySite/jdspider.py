# -*- coding: utf-8 -*-
import requests
from lxml import html


def get_html(keyword):
    url = "https://search.jd.com/Search?keyword=" + keyword
    urls = []
    for i in range(1, 2):
        if i % 2 == 1:
            tempUrl = url + "&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&bs=1&wq=dell&page=" + str(i) + "&s=1&click=0"
            urls.append(tempUrl)

    list = []
    for url in urls:
        r = requests.get(url)
        r.encoding = 'utf-8'
        html_code = html.fromstring(r.text)

        lis = html_code.xpath('//*[@id="J_goodsList"]/ul/li')

        for li in lis:
            item = {}
            item['shop'] = li.xpath("div/div[@class='p-shop']/span/a/text()")
            item['price'] = li.xpath("div/div[@class='p-price']/strong/i/text()")
            item['comments'] = li.xpath("div/div[@class='p-commit']/strong/a/text()")
            item['name'] = li.xpath("div/div[contains(@class,'p-name')]/a/em/text()")
            item['url'] = li.xpath("div/div[contains(@class,'p-name')]/a/@href")
            list.append(item)
    return list


def write_to_txt(list):
    f = open('res.txt', 'w')
    for item in list:
        t1 = ''.join(item['shop']).strip()
        t2 = ''.join(item['price']).strip()
        t3 = ''.join(item['comments']).strip()
        t4 = ''.join(item['name']).strip()
        t5 = ''.join(item['url'])
        if t1 == '' or t2 == '' or t3 == '' or t4 == '' or t5 == '':
            continue
        f.write('店铺：' + ''.join(item['shop']) + '\n')
        f.write('价格：' + ''.join(item['price']) + '\n')
        f.write('评论：' + ''.join(item['comments']) + '\n')
        f.write('商品名称：' + ''.join(item['name']) + '\n')
        f.write('商品链接：https:' + ''.join(item['url']) + '\n')
        f.write('\n' + '\n' + '\n')
    f.close()