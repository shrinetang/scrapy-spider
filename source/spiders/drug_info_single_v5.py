#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ============================================================================
#    File: drug_info_single_v5.py
#
#    Desc: NULL
#
# Version: 5.0
#    Date: 2015-6-3
#  Author: tangxingyu
# Company: ZGWA
#Function: 抽取药品详细信息(包含目录、检索页、概述页、说明书页、评论页)
#                          --- Copyleft (c), 2015 ---
#                              All Rights Reserved.
# ============================================================================

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.selector import Selector
from units import md5single
import traceback
import sys
import re
import hashlib
reload(sys)
sys.setdefaultencoding('utf-8') 
perr = sys.stderr
pout = sys.stdout

parse_name_list = ['parse_drug_search','parse_drug_gaishu','parse_drug_manual','parse_drug_comment']
s_num = 0
g_num = 0
m_num = 0
c_num = 0

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

class DrugSpider(CrawlSpider):  
    name = "drug_info_v5"
    allowed_domains = ["ypk.39.net"]
    start_urls = ("http://ypk.39.net/AllCategory.aspx",)
    #start_urls = ('http://ypk.39.net/yaopin/zty/7b25a.html',)
    rules = [ # 定义爬取URL的规则
        #URL http://ypk.39.net/AllCategory.aspx
        Rule(LinkExtractor(allow=("^http://ypk.39.net/search/[a-zA-Z]+/$"),restrict_xpaths=["//div[@class='page']/div[@id='d1']"]),follow=True),
        #Rule(LinkExtractor(allow=(".*manual.*")),callback='parse_item_manual'),
        #URL http://ypk.39.net/search/jierezhentong/
        Rule(LinkExtractor(allow=("http://ypk.39.net/search/[a-zA-Z]+/($|--0-0-0-0-9-0-0-0-\d+/)"),restrict_xpaths=["//div[@class='page']/div[@class='search_right']/span/span[@class='pgleft']"]),follow=True, callback='parse_drug_search'),
        #URL http://ypk.39.net/yaopin/mianyi/ky/kfsy/add6c.html
        Rule(LinkExtractor(allow=("http://ypk.39.net/yaopin/.*"),restrict_xpaths=["//div[@class='page']/div[@class='search_right']/ul"]), follow=True, callback='parse_drug_gaishu'),
        #URL http://ypk.39.net/manual/712044/0/
        Rule(LinkExtractor(allow=("http://ypk.39.net/manual/.*"),restrict_xpaths=["//div[@class='page']/div[@class='yps_top']"]), follow=False, callback='parse_drug_manual'),
        #URL http://ypk.39.net/comment/510208/1.shtml 需要翻页
        #//div[@class='page']/div[@class='yps_left']/div[@class='dpzx']
        Rule(LinkExtractor(allow=("http://ypk.39.net/comment/\d+/\d+\..*"),restrict_xpaths=["//div[@class='page']/div[@class='yps_top']","//div[@class='dpzx']/span[@class='pages']"]), follow=True, callback='parse_drug_comment'),
    ]


    def parse_drug_menu(self, response):
        #第一层目录：药品/保健品/中药材/家用器械
        err_num = 0
        single_md5 = md5single.Md5update(parse_name_list)
        status = str(response.status)
        if single_md5.Md5YornExist(response.url, status, 'parse_drug_menu') == -1:
            perr.write("dmenu url is already exist: %s" %(response.url))
            return None
        else:
            perr.write("dmenu url insert into []: %s" %(response.url))

        m1_list = response.xpath("//div[@class='page']/div/div/h2/text()").extract() 
        for v1 in range(len(m1_list)):
            try:
                m2_xpath = "//div[@class='page']/div[@id='d%d']/dl/dt/a/text()" %(v1+1)
                #第二层目录：药品/感冒发热..
                #print m2_xpath
                m2_list = response.xpath(m2_xpath).extract()
                for v2 in range(len(m2_list)):
                    m3_xpath = "//div[@class='page']/div[@id='d%d']/dl[%d]/dd/a/text()" %(v1+1,v2+1)
                    m3_url_xpath = "//div[@class='page']/div[@id='d%d']/dl[%d]/dd/a/@href" %(v1+1,v2+1)
                    #print m3_xpath
                    #print m3_url_xpath
                    #第三层目录：药品/感冒发热/解热镇痛
                    m3_list = response.xpath(m3_xpath).extract()
                    #第三层目录对应的跳转URL 药品/感冒发热/解热镇痛url
                    m3_url_list = response.xpath(m3_url_xpath).extract()
                    for v3 in range(len(m3_list)):
                        m1 = m1_list[v1].encode('utf8').replace('\r\n','').replace('\n','').replace(' ','')
                        m2 = m2_list[v2].encode('utf8').replace('\r\n','').replace('\n','').replace(' ','')
                        m3 = m3_list[v3].encode('utf8').replace('\r\n','').replace('\n','').replace(' ','')
                        m3_url = ('http://ypk.39.net' + m3_url_list[v3]).encode('utf8')
                        m3_urlmd5 = hashlib.md5(m3_url.encode('utf-8')).hexdigest()
                        print 'drugmenu' + '\t' + m1 + '\t' + m2 + '\t' + m3 + '\t' + m3_urlmd5
            except Exception,e:
                err_num = err_num + 1
                continue
        #print err_num

    #InPut :None url类似于http://ypk.39.net/search/dixuejia/
    #OutPut:低血钾 门冬氨酸钾镁片 src=http://img.39.net/yp/s/8/756294.jpg icon3;;icon12     上海现代制药股份有限公司  star0       ￥13.28
    def parse_drug_search(self, response):
        #URL去重
        status = str(response.status)
        single_md5 = md5single.Md5update(parse_name_list)
        if single_md5.Md5YornExist(response.url, status, 'parse_drug_search') == -1:
            perr.write("dsearch url is already exist: %s" %(response.url))
            return None
        else:
            perr.write("dsearch url insert into []: %s" %(response.url))

        sel = Selector(response)
        #查找检索分类名search_tips
        search_tips_1 = response.xpath("//div[@class='search_right']/div[@class='search_tips']/a/text()").extract()
        search_tips_2 = response.xpath("//div[@class='subs']/p/a[3]/text()").extract()
        if search_tips_2:
            search_tips = search_tips_2[0]
        elif search_tips_1:
            search_tips = search_tips_1[0]
        else:
            search_tips = ''
            perr.write('search_tips_err:%s\n' %(response.url))

        #记录入口URL信息
        yprevurlmd5  = hashlib.md5(response.url.encode('utf-8')).hexdigest()
        #查询分类下药品信息
        yps_list = sel.xpath("//div[@class='page']/div[@class='search_right']/ul[@class='search_ul search_ul_yb']/li")
        #items = []
        yps_dict = {}
        #搜索的药品列表
        err_num = 0
        if not yps_list:
            perr.write('yps_list_err:%s\n' %(response.url))
            return None
        for yps in yps_list:
            try:
                #item  = ypsItem()
                #依次为药品名，图片，属性列表，生产厂家，评论星级，评价数，参考价格
                yname = yps.xpath("div[@class='msgs']/strong/a/text()").extract()
                ypicurl  = yps.xpath("a/img/@src").extract()
                yattr = yps.xpath("div[@class='msgs']/strong/i/@class").extract()
                ymake = yps.xpath("div[@class='msgs']/p[2]/text()[2]").extract()
                ycomt = yps.xpath("div[@class='some']/p/span/@class").extract()
                ycomn = yps.xpath("div[@class='some']/p/b/i/text()").extract()
                ypric = yps.xpath("div[@class='some']/cite/font/text()").extract()
                ynexturl_tail = yps.xpath("div[@class='msgs']/strong/a/@href").extract()[0].encode('utf8').replace('\r\n','').replace('\n','').replace(' ','')
                ynexturl = ('http://ypk.39.net' + ynexturl_tail).encode('utf8')
                ynexturlmd5 = hashlib.md5(ynexturl.encode('utf-8')).hexdigest()
                #print ypic[0]
                #print yname[0]
                #print yattr[0]
                #print ymake[0]
                #print ycomt[0]
                #print ycomn[0]
                #print ypric[0]
                if type(yname) == type([]):
                #print type(yname)
                    yps_dict['yname'] = yname[0]
                else:
                    yps_dict['yname'] = 'yname'
                if ypicurl:
                    yps_dict['ypicurl']  = 'src=' + ypicurl[0]
                else:
                    yps_dict['ypicurl']  = 'ypicurl'
                if yattr:
                    yps_dict['yattr'] = ';;'.join(yattr)
                else:
                    yps_dict['yattr'] = 'yattr'
                if ymake:
                    yps_dict['ymake'] = ymake[0]
                else:
                    yps_dict['ymake'] = 'ymake'
                if ycomt:
                    yps_dict['ycomt'] = ycomt[0]
                else:
                    yps_dict['ycomt'] = 'ycomt'
                if ycomn:
                    yps_dict['ycomn'] = ycomn[0]
                else:
                    yps_dict['ycomn'] = 'ycomn'
                if ypric:
                    yps_dict['ypric'] = ypric[0]
                else:
                    yps_dict['ypric'] = 'ypric'
                #print yps_dict
                OutPut = ('drugsearch' + '\t' + yprevurlmd5 + '\t' + search_tips + '\t' + yps_dict['yname'] + '\t' + yps_dict['ypicurl'] + '\t' + yps_dict['yattr'] + '\t' + yps_dict['ymake'] + '\t' + yps_dict['ycomt'] + '\t' + yps_dict['ycomn'] + '\t' + yps_dict['ypric'] + '\t' + ynexturlmd5).encode('utf8').replace('\r\n','').replace('\n','').replace(' ','')
                print OutPut
            except Exception, e:
                err_num = err_num + 1
                continue
        if err_num != 0:
            perr.write('yps_err_num:%d,%s\n' %(err_num,response.url))
        #print 'ERR %d' %err_num
        #print len(yps_dict.keys())
        global s_num
        s_num += 1
        perr.write('s_num:%d' %(s_num))

    def parse_drug_gaishu(self, response):
        err_num = 0
        status = str(response.status)
        single_md5 = md5single.Md5update(parse_name_list)
        if single_md5.Md5YornExist(response.url, status, 'parse_drug_gaishu') == -1:
            perr.write("dgaishu url is already exist: %s\n" %(response.url))
            return None
        else:
            perr.write("dgaishu url insert into []: %s\n" %(response.url))

        yp_name = response.xpath("//div[@class='page']/div[@class='yps_top']/div[@class='t1']/h1/a/text()").extract()[0].encode('utf8').replace('\r\n','').replace('\n','').replace(' ','')
        #记录输出前后URL的MD5值方便关联
        gs_prev_urlmd5  = hashlib.md5(response.url.encode('utf-8')).hexdigest()
        m_url_tail = response.xpath("//div[@class='page']/div[@class='yps_top']/div[@class='t4']/ul/li[2]/a/@href").extract()[0].encode('utf8').replace('\r\n','').replace('\n','').replace(' ','')
        m_url = ('http://ypk.39.net' + m_url_tail).encode('utf8')
        gs_manual_md5 = hashlib.md5(m_url.encode('utf-8')).hexdigest()
        c_url_tail = response.xpath("//div[@class='page']/div[@class='yps_top']/div[@class='t4']/ul/li[3]/a/@href").extract()[0].encode('utf8').replace('\r\n','').replace('\n','').replace(' ','')
        c_url = ('http://ypk.39.net' + c_url_tail).encode('utf8')
        gs_comment_md5 = hashlib.md5(c_url.encode('utf-8')).hexdigest()
        if yp_name:
            OutPut = ('druggaishu' + '\t' + yp_name + '\t' + gs_prev_urlmd5 + '\t' + gs_manual_md5 + '\t' + gs_comment_md5)
            print OutPut
        else:
            perr.write("gaishu_ypname_null: %s\n" %(response.url))
        global g_num
        g_num += 1
        perr.write('g_num:%d' %(g_num))

    #InPut :None  
    #OutPut:
    def parse_drug_manual(self, response):
        err_num = 0
        status = str(response.status)
        single_md5 = md5single.Md5update(parse_name_list)
        if single_md5.Md5YornExist(response.url, status, 'parse_drug_manual') == -1:
            perr.write("dmanual url is already exist: %s\n" %(response.url))
            return None
        else:
            perr.write("dmanual url insert into []: %s\n" %(response.url))

        manual_prev_urlmd5  = hashlib.md5(response.url.encode('utf-8')).hexdigest()
        kv_list = []
        yaopin_id = ''
        sel = Selector(response)
        yaopin_name = response.xpath("//div[@class='page']/div/div/h1/a/text()").extract()[0]
        fenlei_list = sel.xpath("//div[@class='tab_hover shuoming']/div[@class='tab_box']/div[@id='tab_con_1']/dl")
        #循环抽取分类名称及其内容
        for fenlei in fenlei_list:
            try:
                list_key = fenlei.xpath("dt/text()").extract()
                list_value1  = fenlei.xpath("dd/p/text()").extract()
                list_value2  = fenlei.xpath("dd/text()").extract()
                list_value3  = fenlei.xpath("dd").extract()
                if list_key:
                    key = list_key[0]
                else:
                    key = 'mkey'
                if list_value1:
                    value = list_value1
                elif list_value2:
                    value = list_value2
                else:
                    value = list_value3
                kvstr = key + '::' + ';;'.join(value)
                if key.encode('utf8') == '【批准文号】':
                    yaopin_id = value[0].encode('utf8').replace('\r\n','').replace('\n','').replace(' ','')
                #print kvstr
                kv_list.append(kvstr)
            except Exception,e:
                err_num = err_num + 1
                continue
        if err_num != 0:
            perr.write("dmanual_errnum:%d %s\n" %(err_num, response.url))
        if yaopin_id == '':
            perr.write("dmanual_yaopinid is null: %s\n" %(err_num, response.url))
        #print err_num
        kv_list_str = ';;'.join(kv_list)
        OutPut = ('drugmanual' + '\t' + yaopin_name + '\t' + yaopin_id + '\t' + manual_prev_urlmd5 + '\t' + kv_list_str).encode('utf8').replace('\r\n','').replace('\n','').replace(' ','')
        print OutPut
        global m_num
        m_num += 1
        perr.write('s_num:%d' %(m_num))

    #InPut :None http://ypk.39.net/comment/509184/1.shtml 
    #OutPut:
    def parse_drug_comment(self, response):
        #URL去重
        err_num = 0
        status = str(response.status)
        single_md5 = md5single.Md5update(parse_name_list)
        if single_md5.Md5YornExist(response.url, status, 'parse_drug_comment') == -1:
            perr.write("dcomment url is already exist: %s" %(response.url))
            return None
        else:
            perr.write("dcomment url insert into []: %s" %(response.url))

        first_page_url = re.sub("\d+.shtml", "1.shtml" , response.url)
        comment_prev_urlmd5  = hashlib.md5(first_page_url.encode('utf-8')).hexdigest()
        cmt_list = []
        #获取药品名称
        yaopin_name = Get_listone("//div[@class='page']/div[@class='yps_top']/div[@class='t1']/h1/a/text()", response)
        #评价列表
        sel = Selector(response)
        sel_list = sel.xpath("//div[@class='pls']/div[@class='pls_box']")
        for sel in sel_list:
            try:
                cmt = sel.xpath("div[@class='pls_mid']/p/text()").extract()
                if type(cmt) == type([]):   
                    cmt_str = ','.join(cmt)
                else:
                    cmt_str = cmt
                #print cmt_str
                cmt_list.append(cmt_str)
            except Exception, e:
                err_num += 1
                continue
        cmt_list_str = ';;'.join(cmt_list)
        if err_num != 0:
            perr.write('drugcomment_err_num:%d,%s\n' %(err_num,response.url))
        #print cmt_list_str
        OutPut = ('drugcmt' + '\t' + yaopin_name + '\t' + comment_prev_urlmd5+ '\t' + cmt_list_str).encode('utf8').replace('\r\n','').replace('\n','').replace(' ','')
        print OutPut
        global c_num
        c_num  += 1
        perr.write('c_num:%d' %(c_num))
