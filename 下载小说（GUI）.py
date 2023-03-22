import tkinter as tk
from tkinter import filedialog
import requests
from bs4 import BeautifulSoup
import random

'''
下载的事件方法
'''
# 列举头
user_agent = ["Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.163 Safari/535.1 ",
              "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0) Gecko/20100101 Firefox/6.0 ",
              "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50 ",
              "Opera/9.80 (Windows NT 6.1; U; zh-cn) Presto/2.9.168 Version/11.50 ",
              "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 2.0.50727; SLCC2; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; .NET4.0C; Tablet PC 2.0; .NET4.0E)",
              "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; InfoPath.3) ",
              "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; GTB7.0) ",
              "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)",
              "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1) ",
              "Mozilla/5.0 (Windows; U; Windows NT 6.1; ) AppleWebKit/534.12 (KHTML, like Gecko) Maxthon/3.0 Safari/534.12 ",
              "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; .NET4.0C; .NET4.0E) ",
              "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; .NET4.0C; .NET4.0E; SE 2.X MetaSr 1.0) ",
              "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.3 (KHTML, like Gecko) Chrome/6.0.472.33 Safari/534.3 SE 2.X MetaSr 1.0 ",
              "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; .NET4.0C; .NET4.0E) ",
              "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/13.0.782.41 Safari/535.1 QQBrowser/6.9.11079.201 ",
              "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; .NET4.0C; .NET4.0E) QQBrowser/6.9.11079.201 ",
              "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0) "
              ]


# 随机使用头
headers = {
    'User-Agent': user_agent[random.randint(0, 16)]
}

# 获取章节地址
chapter_list = {}


def run(url):
    print('正在获取书籍章节', url)
    global book_url
    book_url = url
    res = requests.get(url, headers=headers, timeout=60)
    res.encoding = 'gbk'
    if res.status_code == 200:
        soup = BeautifulSoup(res.text, 'lxml')
        a = soup.find_all('a')
        for i in a[38:len(a)-10]:
            href_list = i.get('href').split('/')
            href = href_list[len(href_list)-1]
            title = i.text
            chapter_list[title] = href
        print(chapter_list.keys())
        insert_chapter(chapter_list.keys())


# 点击搜索
def getBookUrl():
    run(book_url_Entry.get())


# 获取小说下载的目录
def getFolder():
    folder_url.set(filedialog.askdirectory())
    folder_url_Entry_value = folder_url_Entry.get()
    global folder_url_local
    folder_url_local = folder_url_Entry_value

# 获取每章的内容
def cab():
    print('book_url', book_url)
    for key, value in chapter_list.items():
        print(f'正在获取{key}')
        res = requests.get(f'{book_url}{value}', headers=headers, timeout=60,)
        res.encoding = 'gbk'
        if res.status_code == 200:
            soup = BeautifulSoup(res.text, 'lxml')
            a = soup.find_all('div', id='content')
            write(a[0].text, key)

# 写入小说
def write(content, title):
    print('folder_url', folder_url_local)
    fs = open(f'{folder_url_local}/{title}.txt', 'a', encoding='utf-8')
    fs.write(str(content))
    fs.close()
    print(f"已保存{title}")


'''
GUI图形界面
'''
# 调用Tk()创建主窗口
win = tk.Tk()
# 给主窗口起一个名字，也就是窗口的名字
win.title('下载小说（笔趣阁）')
# 设置窗口大小:宽x高,注,此处不能为 "*",必须使用 "x"
win.geometry('600x500')

'''
创建小说下载地址
'''
fm1 = tk.Frame(win)
tk.Label(fm1, text="小说下载地址：").grid(row=0, column=0)
book_url_Entry = tk.Entry(fm1)
book_url_Entry.grid(row=0, column=1)
tk.Button(fm1, text='搜索', width=10, command=getBookUrl).grid(row=0, column=2)
fm1.pack(side=tk.TOP, anchor=tk.NW)

'''
创建小说目录地址
'''
fm2 = tk.Frame(win)
tk.Label(fm2, text="小说保存地址：").grid(row=1, column=0)
folder_url = tk.StringVar()
folder_url_Entry = tk.Entry(fm2, textvariable=folder_url)
folder_url_Entry.grid(row=1, column=1)
tk.Button(fm2, text='选择', width=10, command=getFolder).grid(row=1, column=2)
fm2.pack(side=tk.TOP, anchor=tk.NW, pady=10)

'''
创建目录
'''
fm_c = tk.Frame(win, width=600)
fm_c.pack(side=tk.TOP, anchor=tk.NW)
fm3 = tk.Frame(fm_c, width=600)
listbox1 = tk.Listbox(fm3, width=90, height=20)
listbox1.pack(side=tk.LEFT)
fm3.pack(padx=10)


def insert_chapter(list):
    for i, item in enumerate(list):
        listbox1.insert(i, item)


'''
确认按钮
'''
tk.Button(win, text=' 下 载 ', command=cab).pack(side=tk.RIGHT, padx=10)

# 开启主循环，让窗口处于显示状态
win.mainloop()
