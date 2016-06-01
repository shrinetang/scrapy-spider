#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ============================================================================
#    File: jibin_info_single_v2.py
#
#    Desc: NULL
#
# Version: 2.0
#    Date: 2015-6-3
#  Author: tangxingyu
# Company: ZGWA
#Function: 抽取疾病分类目录 AND 疾病的详细信息(包含其与药品的关联)
#                          --- Copyleft (c), 2015 ---
#                              All Rights Reserved.
# ============================================================================

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.selector import Selector
from units import md5single
import json
import re
import traceback
import sys
import hashlib
reload(sys)
sys.setdefaultencoding('utf-8') 
perr = sys.stderr
pout = sys.stdout

#抽取列表转为字符串Get_listone("//div", response)
def Get_listone(urlxpath,response):
    astr = ''
    try:
        alist = response.xpath(urlxpath).extract()
        if type(alist) == type([]): #如果返回是列表,那么转化为字符串
            return ','.join(alist)
        else: #如果返回不是列表,那么直接输出字符串
            return alist
    except Exception,e:
        print urlxpath + "extract err"
        return astr

def changeltos(alist):
    try:
        if not alist: #空列表返回空字符串''
            return ''
        if type(alist) == type([]): #如果返回是列表,那么转化为字符串
            tempstr = ','.join(alist) #这里保存下列表进行后续的测试处理
            #去除",,"空列表的情况
            formatstr = tempstr.encode('utf8').replace('\r\n','').replace('\n','').replace(' ','').replace(',','')
            return formatstr
        else: #如果返回不是列表,那么直接输出字符串
            return alist
    except Exception,e:
        print urlxpath + "extract err"
        return astr

parse_name_list = ['parse_jibin_menu','parse_jibin_info']

class DrugSpider(CrawlSpider):  
    name = "jibin_info"
    allowed_domains = ["jbk.39.net"]
    download_delay = 1
    #start_urls = ('http://jbk.39.net/',)
    #测试URL
    start_urls = ('http://jbk.39.net/tnb/',)
    rules = [ 
        # 定义爬取URL的规则
        #Rule(LinkExtractor(allow=(".*/zq/[a-zA-z]*\??.*")),follow=True,callback='jibin_menu'),
        #疾病列表页面跳转 URL类似于http://jbk.39.net/zq/manxingbing 或者是/zq/manxingbing?hsid=0&ybid=0&p=2#more
        #过滤到重新返回第一页的内容 http://jbk.39.net/zq/manxingbing?hsid=0&ybid=0&p=1#more
        Rule(LinkExtractor(allow=(".*/zq/[a-zA-z]*($|\?.*)")),follow=True),
        #疾病详细信息和所用药品的抓取 URL类似于http://jbk.39.net/gxy/
        Rule(LinkExtractor(allow=("^http://jbk.39.net/[a-zA-Z]+/$")),follow=False,callback='parse_jibin_info'),
    ]

    #抓取疾病目录信息
    #InPut :None url类似于http://jbk.39.net/zq/xxxxx
    #OutPut:新生儿易患疾病  新生儿黄疸;;婴幼儿腹泻;;奶癣;;新生儿肺炎;;新生儿缺氧缺血性...;;母乳性黄疸;;尿布疹;;新生儿败血症
    def parse_jibin_menu(self, response):
        status = str(response.status)
        #实例化单例类，多于一个不再初始化
        single_md5 = md5single.Md5update(parse_name_list)
        
        if single_md5.Md5YornExist(response.url, status, 'parse_jibin_menu') == -1:
            print "url is already exist: %s" %(response.url)
            return 1
        else:
            print "url insert into []: %s" %(response.url)

        err_num = 0
        sel = Selector(response)
        #获取疾病名称
        fenlei_namel = response.xpath("//div[@class='headline clearfix']/h1/text()").extract()
        if fenlei_namel:
            fenlei_name = fenlei_namel[0]
        else:
            fenlei_name = ''
        fenlei_jb_list = response.xpath("//div[@class='list']/div[@class='item']/div/h4/a/text()").extract()
        if not fenlei_jb_list:
            fenlei_jb_list = []
        #print fenlei_jb_list
        OutPut = fenlei_name + '\t' + ';;'.join(fenlei_jb_list)
        print OutPut
        return 0
        #sites = sel.xpath("//div[@class='list']/div[@class='item']")

    #抓取疾病详细信息
    #InPut :None url类似于http://jbk.39.net/gxy/
    #OutPut:jibin_info  高血压 　　在未用抗高血压药情况下，收缩压≥139mmHg和/或舒张压≥89mmHg，按血压水平将高血压分为1，2，3级。
    def parse_jibin_info(self, response):
        err_num = 0
        sel = Selector(response)
        status = str(response.status)
        #实例化单例类，多于一个不再初始化
        single_md5 = md5single.Md5update(parse_name_list)
        #URL去重
        if single_md5.Md5YornExist(response.url, status, 'parse_jibin_info') == -1:
            perr.write("jbinfo url exist: %s" %(response.url))
            return None
        else:
            perr.write("jbinfo url insert []: %s" %(response.url))

        #获取疾病名称
        jb_name = Get_listone("//div[@class='chi-int']/div[@class='intro']/p/b/text()",response)
        #获取疾病介绍
        jb_intro = Get_listone("//div[@class='chi-int']/div[@class='intro']/p/text()",response)

        #//div[@class='chi-int']/div[@class='info']/ul/li[1]/i/text() key
        #//div[@class='chi-int']/div[@class='info']/ul/li[1]/a/text() value
        #//div[@class='chi-int']/div[@class='info']/ul/li[1]/text() value
        sel_list = sel.xpath("//div[@class='chi-int']/div[@class='info']/ul/li")
        kv_list = []
        for sel in sel_list:
            try:
                key = sel.xpath("i/text()").extract()
                value1 = sel.xpath("a/text()").extract()
                value2 = sel.xpath("text()").extract()
                keystrtmp = changeltos(key)
                keystr = keystrtmp.encode('utf8').replace(u'\uff1a','')
                value1str = changeltos(value1)
                value2str = changeltos(value2)
                if value1str:
                    valuestr = value1str
                elif value2str:
                    valuestr = value2str
                else:
                    valuestr = ''
                kvstr = keystr + '::' + valuestr
                kv_list.append(kvstr)
            except Exception, e:
                err_num = err_num + 1
                continue
        kv_list_str = ';;'.join(kv_list)
        OutPut = ('jibin_info' + '\t' + jb_name + '\t' + jb_intro + '\t' + kv_list_str).encode('utf8').replace('\r\n','').replace('\n','').replace(' ','')
        if jb_name != '':
            print OutPut
        return 0


