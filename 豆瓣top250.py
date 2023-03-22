import requests
import re
from bs4 import BeautifulSoup
import json
import os

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"}
url = 'https://movie.douban.com/top250'


def find_count():  # 找到页数，每页25个
    res = requests.get(url, headers=headers)
    if res.status_code == 200:
        soup = BeautifulSoup(res.text, features='lxml', from_encoding='utf-8')
        count = soup.select('.count')[0].string
        return [int(s) for s in re.findall(r'-?\d+\.?\d*', count)][0]


def handle_text(page_num):  # 处理函数
    res = requests.get(url + f'?start={page_num}', headers=headers)
    list = []
    if res.status_code == 200:
        soup = BeautifulSoup(res.text, features='lxml', from_encoding='utf-8')
        pic = soup.select('.pic')
        for k in range(0, len(pic)):
            index = pic[k].find('em').string
            imgs = pic[k].find('img').attrs
            list.append(
                {"index": index,  "name": imgs['alt'], "img": imgs['src']})
        return list


# 如果存在文件，则删除
if os.path.exists('./douban.json'):
    os.remove('./douban.json')
# 获取需要请求的次数
count = int(find_count() / 25)
# 开始处理数据
result = []
for k in range(0, count, 25):
    result_item = handle_text(k)
    for i in result_item:
        result.append(i)
# 保存文件
fs = open('./douban.json', 'a', encoding='utf-8')
fs.write(json.dumps(result, ensure_ascii=False))
fs.close()
