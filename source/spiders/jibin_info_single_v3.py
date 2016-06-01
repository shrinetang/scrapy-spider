#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ============================================================================
#    File: jibin_info_single_v3.py
#
#    Desc: modify-time 2015-06-04 修正了restirct_xpath 抓取规则，添加了疾病相关药品的抓取
#
# Version: 3.1
#    Date: 2015-6-3
#  Author: tangxingyu
# Company: ZGWA
#Function: 抽取疾病分类目录(包含其与症状的关联) AND 疾病的详细信息(包含其与药品的关联)
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
    name = "jibin_info_v3"
    allowed_domains = ["jbk.39.net"]
    download_delay = 1
    start_urls = ('http://jbk.39.net/',)
    #测试URL
    #start_urls = ('http://jbk.39.net/tnb/',)
    rules = [ 
        # 定义爬取URL的规则
        #疾病列表页面跳转 URL类似于http://jbk.39.net/zq/manxingbing 或者是/zq/manxingbing?hsid=0&ybid=0&p=2#more
        Rule(LinkExtractor(allow=("http://jbk.39.net/zq/[a-zA-z]*($|\?.*)"),restrict_xpaths=["//div[@class='left']/div[@class='lbox']/ul[@class='leftlist']","//div[@class='chr-all']/div[@class='site-pages']"]),follow=True,callback='parse_jibin_menu'),
        #疾病详情页URL
        Rule(LinkExtractor(allow=("http://jbk.39.net/[a-zA-z]*/$"),restrict_xpaths=["//div[@class='chr-all']/div[@class='list']"]),follow=True,callback='parse_jibin_info'),
    ]

    #抓取疾病目录信息
    #InPut :None url类似于http://jbk.39.net/zq/xxxxx
    #OutPut:
    def parse_jibin_menu(self, response):
        status = str(response.status)
        #实例化单例类，多于一个不再初始化
        single_md5 = md5single.Md5update(parse_name_list)
        
        if single_md5.Md5YornExist(response.url, status, 'parse_jibin_menu') == -1:
            perr.write("jbmuurl is already exist: %s" %(response.url))
            return None
        else:
            perr.write("jbmuurl insert into []: %s" %(response.url))

        err_num = 0
        fenlei_namel = response.xpath("//div[@class='headline clearfix']/h1/text()").extract()
        if fenlei_namel:
            fenlei_name = fenlei_namel[0]
        else:
            fenlei_name = '-'
            perr.write('fenlei_name_err:%s\n' %(response.url))
        sel = Selector(response)
        sites = sel.xpath("//div[@class='chr-all']/div[@class='list']/div[@class='item']")
        #循环抓取疾病列表数据
        for site in sites:
            try:
                jb_name = site.xpath("div[@class='tit clearfix']/h4/a/text()").extract()[0]
                jb_xgzz_list = site.xpath("ul[@class='tag clearfix']/li[not(@class)]/a/text()").extract()
                if not jb_xgzz_list and (type(jb_xgzz_list) != type([])):
                    perr.write('jb_xgzz_list_err:%s\n' %(response.url))
                    continue
                jb_xgzz_str = ';;'.join(jb_xgzz_list)
                OutPut = ('jb_menu' + '\t' + fenlei_name + '\t' + jb_name + '\t' + jb_xgzz_str).encode('utf8').replace('\r\n','').replace('\n','').replace(' ','')
                print OutPut
            except Exception, e:
                err_num += 1
        if err_num != 0:
            perr.write('jb_menu_err_num:%d,%s\n' %(err_num,response.url))

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
        jbyp_list = response.xpath("//div[@class='lbox']/div[@class='lbox-drug clearfix']/dl/dd/h4/a/text()").extract()
        jbyp_str  = ';;'.join(jbyp_list)
        kv_list_str = ';;'.join(kv_list)
        OutPut = ('jb_info' + '\t' + jb_name + '\t' + jb_intro + '\t' + kv_list_str + '\t' + jbyp_str).encode('utf8').replace('\r\n','').replace('\n','').replace(' ','')
        if jb_name != '':
            print OutPut
        return 0


