#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ============================================================================
#    File: md5single.py
#
#    Desc: NULL
#
# Version: 1.0
#    Date: 2015-6-3
#  Author: tangxingyu
# Company: ZGWA
#Function: 单例模式实现URL列表的保存和更新
#                          --- Copyleft (c), 2015 ---
#                              All Rights Reserved.
# ============================================================================

import mydb
import hashlib
import sys
perr = sys.stderr
pout = sys.stdout
#perr.write()
class Singleton(object):  
    def __new__(cls, *args, **kw):  
        if not hasattr(cls, '_instance'):  
            orig = super(Singleton, cls)  
            cls._instance = orig.__new__(cls, *args, **kw)  
        return cls._instance

class Md5update(Singleton):
    """docstring for Md5update"""
    init_count = 0
    def __init__(self, parse_name_list):
        if Md5update.init_count == 0:
            perr.write('---------------Md5 init--------------------')
            self.parse_name_list = parse_name_list
            self.parse_md5_old_dict = {}
            self.parse_md5_new_dict = {}
            #{pname1:{md:status,.....},pname2{md:status,.....}}}
            self.status_dict = {}
            #初始化MD5值记录列表
            for parse_name in self.parse_name_list:
                self.parse_md5_old_dict[parse_name] = mydb.SelectDB(parse_name)
                self.parse_md5_new_dict[parse_name] = []
                self.status_dict[parse_name] = {}
                #print self.parse_md5_old_dict[parse_name]
            Md5update.init_count = 1
            #print Md5update.init_count

    def Md5YornExist(self, weburl, status, parse_name):
        if parse_name not in self.parse_name_list:
            perr.write("parse_name not in parse_name_list")
            return -2

        urlmd5 = hashlib.md5(weburl.encode('utf-8')).hexdigest()
        if urlmd5 in self.parse_md5_old_dict[parse_name]:
            #print "urlmd5 in oldlist"
            #print urlmd5
            #print self.parse_md5_old_dict[parse_name]
            return -1
        elif urlmd5 in self.parse_md5_new_dict[parse_name]:
            #print "urlmd5 in newlist"
            #print urlmd5
            #print self.parse_md5_new_dict[parse_name]
            return -1
        else: #新添加MD5
            #print "urlmd5 is not exist"
            self.parse_md5_new_dict[parse_name].append(urlmd5)
            self.status_dict[parse_name][urlmd5] = status

            #更新数据库['md5','200','test']
            #print len(parse_md5_new_dict[parse_name])
            if len(self.parse_md5_new_dict[parse_name]) >= 100:
                #print "new %s list over 10!" %(parse_name)
                #存放待插入数据库的rows [row1,row2...]
                insertlist = []
                #存放待插入数据库的row['md5',200,pname]
                #insertrow = []
                #将新缓存数据写入数据库，并合并新旧缓存
                perr.write(str(self.parse_md5_new_dict[parse_name]))
                #print self.status_dict
                perr.write('--------------------InsertDB Begin------------------------------')
                for md5 in self.parse_md5_new_dict[parse_name]:
                    try:
                        insertrow = []
                        insertrow.append(md5)
                        if md5 not in self.status_dict[parse_name]:
                            insertrow.append(self.status_dict[parse_name][md5])
                        else:
                            insertrow.append('200')
                        insertrow.append(parse_name)
                        insertlist.append(insertrow)
                    except Exception, e:
                        continue
                perr.write(str(insertlist))
                if mydb.InsertDB(insertlist):
                    perr.write("InsertDB fail %s" %(str(insertlist)))
                perr.write('--------------------InsertDB OK------------------------------')
                #print "Write newmd5 to DB ok"
                self.parse_md5_old_dict[parse_name].extend(self.parse_md5_new_dict[parse_name])
                self.status_dict[parse_name] = {}
                perr.write("md5 old is update")
                #perr.write(self.parse_md5_old_dict)
                self.parse_md5_new_dict[parse_name] = []
                #print "md5 new is null"
            return 0

if __name__ == '__main__':
    parse_name_list = ['test','parse_jibin_info','parse_jibin_menu','hello']
    md5test = Md5update(parse_name_list)
    url_list = [] #test1
    url_list2 = [] #test2
    parse_name = 'test'

    for i in range(12,21):
        url_str = "http://ypk.39.net/comment/507831/%d.shtml" %i
        #print url_str
        url_list.append(url_str)
    url_list2 = ["http://ypk.39.net/comment/507831/2.shtml","http://ypk.39.net/comment/507831/7.shtml","http://ypk.39.net/comment/507831/9.shtml","http://ypk.39.net/comment/507831/6.shtml"]
    for url in url_list:
        if md5test.Md5YornExist(url,'200',parse_name) == -1:
            print "url is already exist: %s" %(url)
        else: 
            print "url insert into []: %s" %(url)

    for url in url_list2:
        if md5test.Md5YornExist(url,'200',parse_name) == -1:
            print "url is already exist: %s" %(url)
        else:
            print "url insert into []: %s" %(url)
    print md5test.parse_name_list
    print md5test.parse_md5_old_dict
    print md5test.parse_md5_new_dict    

    parse_name_list2 = ['dsddaf','tatgd','finger']
    md5test2 = Md5update(parse_name_list2)
    print md5test2.parse_name_list
    print md5test2.parse_md5_old_dict
    print md5test2.parse_md5_new_dict
    print Md5update.init_count
