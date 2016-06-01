#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ============================================================================
#    File: zz_info_single_v2.py
#
#    Desc: modify-time 2015-06-05 修正了first_name列表的顺序，添加了restrict_xpaths的限制
#
# Version: 2.0
#    Date: 2015-6-3
#  Author: tangxingyu
# Company: ZGWA
#Function: 抽取症状分类目录 AND 症状的详细信息(包含其与药品的关联)
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
import md5
import hashlib
reload(sys)
sys.setdefaultencoding('utf-8') 

perr = sys.stderr
pout = sys.stdout

parse_name_list = ['parse_zz_menu','parse_zz_info']

"""
def md5_yorn_exist(weburl):
    urlmd5=hashlib.md5(weburl.encode('utf-8')).hexdigest()
    if urlmd5 in md5_list:
        #print "urlmd5 is exist"
        #print urlmd5
        #print md5_list
        return 1
    else:
        #print "urlmd5 is not exist"
        #md5_list.append(urlmd5)
        #print md5_list
        return 0
"""
    
class DrugSpider(CrawlSpider):  
    name = "zz_info_v2"
    allowed_domains = ["jbk.39.net"]
    download_delay = 1
    start_urls = ('http://jbk.39.net/zhengzhuang/',)
    #测试URL
    #start_urls = ('http://jbk.39.net/bw_t2_v11',)
    #start_urls = ('http://jbk.39.net/zhengzhuang/gjtt/zdxs/#zdxs',)
    rules = [ 
        # 定义爬取URL的规则
        #疾病目录的抓取 URL类似于http://jbk.39.net/bw_t2_v1  http://jbk.39.net/bw_v1_p30#ps
        Rule(LinkExtractor(allow=("http://jbk.39.net/((bw_t\d_v\d{1,2})|(bw_v\d{1,2}_p\d{1,2})).*"),restrict_xpaths=["//div[@class='fenlei']","//div[@class='lbox_art']/div[@id='res_tab_3']/div/div[@class='site-pages']"]),follow=True,callback='parse_zz_menu'),
        #症状详细信息的抓取 URL类似于http://jbk.39.net/zhengzhuang/gjtt/
        Rule(LinkExtractor(allow=("http://jbk.39.net/zhengzhuang/[a-zA-Z]+/$"),restrict_xpaths=["//div[@class='res lbox']/div[@class='lbox_art']"]),follow=True,callback='parse_zz_info'),
        #诊断详述中对症药品信息的抓取 URL类似于http://jbk.39.net/zhengzhuang/gjtt/zdxs/#zdxs 或者/bg/zdxs/
        #Rule(LinkExtractor(allow=(".*/zhengzhuang/[a-zA-Z]+/zdxs/.*")),follow=False, callback='parse_dzyaopin'),
    ]

    #InPut :None http://jbk.39.net/bw_t2_v1  http://jbk.39.net/bw_v1_p1#ps   p1代表第几页v1代表first_name序号
    #OutPut:{'\xe7\x96\xbc\xe7\x97\x9b'疼痛: [u'\u5173\u8282\u75bc\u75db'关节疼痛, u'\u80c3\u75db'胃痛]} 
    def parse_zz_menu(self, response):
        err_num = 0
        status = str(response.status)
        #实例化单例类，多于一个不再初始化
        single_md5 = md5single.Md5update(parse_name_list)
        
        if single_md5.Md5YornExist(response.url, status, 'parse_zz_menu') == -1:
            perr.write("zzmuurl is already exist: %s" %(response.url))
            return None
        else:
            perr.write("zzmuurl insert into []: %s" %(response.url))

        first_name = ['疼痛','发热','皮肤异常','水肿','咳','呼吸','呕','大便','尿','晕','抽搐','意识障碍','精神心理']
        m = re.match('.*v(\d{1,2}).*', response.url)

        xpath_str = "//div[@class='lbox_art']/div[@id='res_tab_3']/div[@id='res_subtab_%d']/div[@class='res_list']/dl/dt/h3/a/text()" %(int(m.group(1))+1)
        #print xpath_str
        jb_name_list = response.xpath(xpath_str).extract()
        """
        sel = Selector(response)
        sites = sel.xpath(xpath_str)
        for site in sites:
            try:
                jb_name_e = site.xpath("dl/dt/h3/a/text()").extract()
                #print jb_name_e[0]
                if jb_name_e:
                    jb_name = jb_name_e[0]
                else:
                    jb_name = ''
                jb_name_list.append(jb_name)
            except Exception,e:
                err_num = err_num + 1
                traceback.print_exc()
                continue
        """
        #print jb_name_list
        #print err_num
        OutPut = ( 'zz_menu'+ '\t' + first_name[int(m.group(1))-1] + '\t'+ ';;'.join(jb_name_list)).encode('utf8').replace('\r\n','').replace('\n','').replace(' ','')
        print OutPut


    #InPut :None url类似于http://jbk.39.net/zhengzhuang/gjtt
    #OutPut:zzjbxx\t症状名\t什么是该症状\t解答\t相关疾病列表[{'疾病名称':A,'伴随症状':,B,'就诊科室':C}, {...}, {...}]
    def parse_zz_info(self, response):
        err_num = 0
        knjb_dict = {}
        knjb_info_list = []
        status = str(response.status)

        single_md5 = md5single.Md5update(parse_name_list)
        #URL去重
        if single_md5.Md5YornExist(response.url, status, 'parse_zz_info') == -1:
            perr.write("zzinfo url exist: %s" %(response.url))
            return None
        else:
            perr.write("zzinfo url insert []: %s" %(response.url))

        sel = Selector(response)

        zzname_list = response.xpath("//header[@class='list_tit']/div/a/h1/text()").extract()
        if zzname_list:
            zzname = zzname_list[0]
        else:
            zzname = ''
        #print zzname

        zzprob1 = response.xpath("//div[@class='list_head catalogItem']/div[@class='intro clearfix']/dl/dt[@class='clearfix']/b/text()").extract()
        zzprob2 = response.xpath("//div[@class='list_head catalogItem']/div[@class='intro clearfix']/dl/dt[@class='clearfix']/b/i/text()").extract()
        zzprob_list = response.xpath("//div[@class='list_head catalogItem']/div[@class='intro clearfix']/dl/dt[@class='clearfix']/b").extract()
        #print zzprob1
        #print zzprob2
        if zzprob1 and zzprob2:
            zzprob = zzprob1[0] + zzprob2[0]
        elif zzprob_list:
            zzprob = zzprob_list[0]
        else:
            zzprob = ''
        #print zzprob
        
        #这里嵌入了全部显示的js，暂时不做处理
        zzansw_list = response.xpath("//div[@class='list_head catalogItem']/div[@class='intro clearfix']/dl/dd[@id='intro']/p/text()").extract()
        if zzansw_list:
            zzansw = ','.join(zzansw_list)
        else:
            zzansw = ''
        #print zzansw

        sel_list = sel.xpath("//div[@class='list_head catalogItem']/div[@class='zz_info']/div[@class='item']/table/tr")
        skip_num = 1
        for sel in sel_list:
            try:
                if skip_num == 1:
                    skip_num = skip_num - 1
                    continue
                knjbl = sel.xpath("td[@class='name']/a/text()").extract()
                if knjbl:
                    knjb_dict['疾病名称'] = knjbl[0]
                else:
                    knjb_dict['疾病名称'] = ''
                """
                if sel.xpath("td[2]/a/text()").extract():
                    knjb_dict['伴随症状'] = sel.xpath("td[2]/a/text()").extract(): #list
                else:
                    knjb_dict['伴随症状'] = []
                if sel.xpath("td[3]/a/text()").extract():
                    knjb_dict['就诊科室'] = sel.xpath("td[3]/a/text()").extract() #list
                else:
                    knjb_dict['就诊科室'] = []
                """
                #print knjb_dict
                knjb_info_list.append(knjb_dict['疾病名称'])
            except Exception,e:
                err_num = err_num + 1
                traceback.print_exc()
                continue
        if knjb_info_list: #这里有部分网页并非疾病信息页 过滤掉
            str_knjb_info_list = ';;'.join(knjb_info_list)
            #print str_knjb_info_list
            OutPut = ('zz_info' + '\t' + zzname + '\t' + zzprob + '\t' + zzansw +'\t' +str_knjb_info_list).encode('utf8').replace('\r\n','').replace('\n','').replace(' ','')
            print OutPut

    #InPut :None url类似于http://jbk.39.net/zhengzhuang/gjtt/zdxs/#zdxs  
    #OutPut:zzdzyaopin  关节疼痛    云南白药气雾剂;;蚁参蠲痹胶囊;;....
    def parse_dzyaopin(self, response):
        err_num = 0

        #获取疾病名称
        zz_name_list = response.xpath("//div[@class='tik clearfix']/a/h1/text()").extract()
        if zz_name_list:
            zz_name = zz_name_list[0]
        else:
            zz_name = ''
        #获取全部对症药品信息
        dz_yaopin_list = response.xpath("//div[@id='zdxs']/div[@class='item']/div[@id='relateDrug']/dl/dd/h4/a/text()").extract()
        str_dzyp = ';;'.join(dz_yaopin_list)
        OutPut = ('zzdzyaopin'+ '\t' + zz_name + '\t' + str_dzyp).encode('utf8').replace('\r\n','').replace('\n','').replace(' ','')
        #print 'zzdzyaopin'+ '\t' + zz_name + '\t' + str_dzyp
        print OutPut
        
