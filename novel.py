#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2017-09-12 17:12:48
# Project: novel

from pyspider.libs.base_handler import *
import re
from pyspider.database.mysql.mysqldb import MYSQL
class Handler(BaseHandler):
    crawl_config = {
    }


    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl('http://wodeshucheng.com', callback=self.index_page)

    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):
        for each in response.doc('.books > ul > div > h3 > a').items():
            self.crawl(each.attr.href, callback=self.novel)


    def novel(self,response):
        for each in response.doc('.book_list > ul > li > a').items():

            self.crawl(each.attr.href,callback=self.detail_page)

    @config(priority=2)
    def detail_page(self, response):
        ad=response.doc('.chapter_Turnpage').text()
        content=response.doc('.contentbox').text().strip(ad)
        temp=re.split('/',response.url)[-1]
        flag=temp.index('.html')
        chapterNum=temp[:flag]
        bookName=re.split(' ',response.doc('.srcbox > a').text())[-1]
        title=response.doc('.h1title > h1').text()
        return {
            "title":title,
            "content": content,
            "chapterNum":chapterNum,
            "bookName":bookName
        }
    def on_result(self,result):
        if not result or not result['title']:
            return
        param={
            'host':'localhost',
          'user':'root',
          'password':'zhangyanping',
              'database':'novel',
        } 

        sql=MYSQL(param)
        sql.insert('book_content',result)
