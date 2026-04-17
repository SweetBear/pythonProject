# -*- coding: UTF-8 -*-

import time
import traceback
from urllib import request
from urllib.parse import quote_plus
from bs4 import BeautifulSoup
from MongoDBUtil import MongoDBUtil
import uuid
import datetime
import pymongo
import logging

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
mongoUtil = MongoDBUtil(ip="218.90.198.56", db_name="db_book", port=27017)
logging.basicConfig(filename=f'D:\GL_LOG\doubanSpider\spider.log', level=logging.ERROR,
                    format='%(asctime)s %(funcName)s %(threadName)s %(message)s')
logger = logging.getLogger()  # 获取Logger对象


def book_spider(tag_name):
    url = 'https://book.douban.com/tag/'
    try:

        # 获取总页数
        req = request.Request(url + quote_plus(tag_name), headers=headers)
        source_code = request.urlopen(req).read().decode('utf-8')
        plain_text = str(source_code)
        soup = BeautifulSoup(plain_text, 'html.parser')
        paginator_soup = soup.find('div', {'class', 'paginator'})
        if paginator_soup == None:
            total_page = 1
        else:
            paginator_tag = paginator_soup.find_all('a')
            total_page = paginator_tag[len(paginator_tag) - 2].get_text()
        filter = {'tag_name': tag_name}
        row = mongoUtil.find_one(collect_name="book_tag_info", filter=filter)
        spider_tag_book_url(url, tag_name, total_page, row.get("query_num"))

    except Exception as e:
        print(e)
        traceback.print_exc()


##获取豆瓣读书的热门标签
def book_tag_spider():
    url = 'https://book.douban.com/tag/'
    try:
        # 获取总页数
        req = request.Request(url, headers=headers)
        source_code = request.urlopen(req).read().decode('utf-8')
        plain_text = str(source_code)
        soup = BeautifulSoup(plain_text, 'html.parser')
        table_soup_list = soup.find_all('table', {'class', 'tagCol'})
        for table_soup in table_soup_list:
            tag_soups = table_soup.find_all('a')
            for tag_soup in tag_soups:
                tag_name = tag_soup.get_text()

                document = {'uid': str(uuid.uuid4()).replace("-", ""), 'tag_name': tag_name,
                            'spider_state': 0, 'create_time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

                stat = mongoUtil.insert_one(collect_name="book_tag_info", document=document)
        time.sleep(2)
    except Exception as e:
        print(e)
        traceback.print_exc()


def spider_tag_book_url(url, book_tag, total_page, query_num):
    print('开始爬取热门标签：' + book_tag)
    total_page = int(total_page)
    url = url + quote_plus(book_tag)
    if query_num == 0:
        i = 0
    else:
        i = int(query_num) // 20
    book_url = ''
    book_name = ''
    book_id = ''
    while i < total_page:

        if '&type=T' not in url:
            url = url + '?start=' + str(i * 20) + '&type=T'
        else:
            url = url.replace('?start=' + str((i - 1) * 20) + '&type=T', '?start=' + str(i * 20) + '&type=T')
        print(url)
        try:
            req = request.Request(url, headers=headers)
            source_code = request.urlopen(req, timeout=10).read().decode('utf-8')
        except Exception as error:
            try:
                logger.error("请求url超时，url=" + url, error)
                req = request.Request(url, headers=headers)
                source_code = request.urlopen(req, timeout=10).read().decode('utf-8')
            except Exception as error:
                logger.error("再次请求url超时，url=" + url, error)
                i += 1
                time.sleep(2)
                continue

        plain_text = str(source_code)
        logger.error("url:" + url)
        logger.error(plain_text)
        soup = BeautifulSoup(plain_text, 'html.parser')
        try:
            no_flag = soup.find('div', {'id': 'subject_list'}).get_text()
            if no_flag != None and '没有找到符合条件的图书' in no_flag:
                print("以下列表未空，结束当前标签")
                break
            list_soup = soup.find_all('li', {'class': 'subject-item'})

            for liSoup in list_soup:
                try:
                    # img_url = liSoup.find('a', {'class', 'nbg'}).find('img').get('src')
                    book_url = liSoup.find('div', {'class', 'info'}).find('a').get('href')
                    book_name = liSoup.find('div', {'class', 'info'}).find('a').get_text().replace("\n", "")
                    book_id = book_url.replace("https://book.douban.com/subject/", "").replace("/", "")

                    # print(book_url + "==>" + book_name)
                    """文档操作：增加"""
                    document = {'uid': str(uuid.uuid4()).replace("-", ""), '_id': book_id, 'book_name': book_name,
                                'book_url': book_url, 'book_tag': [book_tag], 'spider_state': 0,
                                'create_time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

                    stat = mongoUtil.insert_one(collect_name="book_url_info", document=document)
                except pymongo.errors.DuplicateKeyError:
                    print('主键冲突，冲突名称：' + book_name + ',主键为：' + book_id)
                    try:
                        filter = {"_id": book_id}
                        spec = {"book_tag": book_tag}
                        update = {"$push": spec}
                        stat = mongoUtil.update_one(collect_name="book_url_info", filter=filter, update=update)
                    except Exception as e:
                        print(e)
                        traceback.print_exc()
            i += 1
            time.sleep(2)
        except Exception as e:
            print(e)
            traceback.print_exc()
            i += 1
            time.sleep(2)

    filter = {"tag_name": tag_name}
    spec = {"spider_state": 1}
    update = {"$set": spec}
    stat = mongoUtil.update_one(collect_name="book_tag_info", filter=filter, update=update)


if __name__ == '__main__':
    tag_names = []
    filter = {'spider_state': 0}
    rows = mongoUtil.find(collect_name="book_tag_info", filter=filter)
    for row in rows:
        tag_names.append(row.get('tag_name'))
    print(len(tag_names))

    for tag_name in tag_names:
        print('开始爬取：' + tag_name + '书籍')
        book_spider(tag_name)
        print('结束爬取标签：' + tag_name)
        time.sleep(5)
    # book_tag_spider()
