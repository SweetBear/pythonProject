import sys
import time

from selenium import webdriver
from selenium.webdriver.common.by import By

cookie = 'uuid_c4d58350-34dc-11ed-b739-e55eae900f49=b4581c12-04f9-425b-b598-00d8447c0dea; href=https%3A%2F%2Fsyly.lianchuanghj.com%2Fsyjs-client-newh5%2F%23%2F; accessId=c4d58350-34dc-11ed-b739-e55eae900f49; pageViewNum=1'


def dealCokie(cookie):
    cookies = {}
    for line in cookie.split(';'):
        if line.strip():
            key, value = line.strip().split('=', 1)
            cookies[key] = value
    return cookies


if __name__ == '__main__':
    # print(sys.executable)
    print('11111')
    driver = webdriver.Chrome()
    cookies = dealCokie(cookie)
    print(cookies)
    driver.add_cookie(cookies)
    print('2222')
    driver.get(
        "https://syly.lianchuanghj.com/syjs-client-newh5/#/bookingIndex?resId=1506&resName=%E5%BE%B7%E5%9F%BA%E8%89%BA%E6%9C%AF%E5%8D%9A%E7%89%A9%E9%A6%86'")
    print('3333')
    print(driver.title)

    content = driver.page_source
    print(content)
# driver.quit()
