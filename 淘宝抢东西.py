from selenium import webdriver
from selenium.webdriver.common.by import By
import re
import datetime
import time
import threading

# 启动浏览器的驱动器
driver = webdriver.Chrome()
# 最大化浏览器
driver.maximize_window()

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
}

# 需要抢购的商品页面链接
url = "https://detail.tmall.com/item.htm?areaId=610100&cat_id=2&id=42302551887&is_b=1&rn=ee9ddd89a20cdfdbf21dbcf8c4f6a6da&skuId=4228835266195&spm=a220m.1000862.1000725.1.7cdb8dfc4OMuMJ"


def open():
    driver.get(url)
    print('请在15秒内扫码登录')
    time.sleep(15)
    print('请在15秒内选择购买商品的规格')
    time.sleep(15)
    find()


def find():
    # 查找数量
    if driver.find_element(By.CLASS_NAME, 'quantityTip'):
        text = re.compile('有货').findall(
            driver.find_element(By.CLASS_NAME, 'quantityTip').text)
        print('text', text)
        if len(text) > 0:
            # 有货的话，直接购买
            now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
            print("有货时间：%s" % now)
            buy(len(text))
        else:
            # 定时器刷新页面
            driver.refresh()
            timer = threading.Timer(1, find)
            timer.start()


def buy(num):
    # 查找购买按钮
    if driver.find_elements(By.CLASS_NAME, 'Actions--leftBtn--3kx8kg8'):
        while True:
            # 如果有货的话
            if num > 0:
                try:
                    driver.find_elements(
                        By.CLASS_NAME, 'Actions--leftBtn--3kx8kg8')[0].click()
                    print('进入结算页面')
                    time.sleep(0.01)
                    submit()
                except:
                    pass
            break


def submit():
    while True:
        try:
            if driver.find_element(By.LINK_TEXT, '提交订单'):
                driver.find_element(By.LINK_TEXT, '提交订单').click()
                now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
                print("抢购成功时间：%s" % now)
                break
        except:
            print("再次尝试提交订单")
            time.sleep(0.01)


open()
