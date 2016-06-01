#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ============================================================================
#    File: md5update.py
#
#    Desc: NULL
#
# Version: 1.0
#    Date: 2015-6-3
#  Author: tangxingyu
# Company: ZGWA
#Function: 模块方式实现URL列表的保存和更新
#                          --- Copyleft (c), 2015 ---
#                              All Rights Reserved.
# ============================================================================

import mydb
import hashlib
parse_name_list = ['test','parse_jibin_menu','parse_jibin_info']
parse_md5_old_dict = {}
parse_md5_new_dict = {}
status_dict = {}

print __name__

def init_parse_md5():
    for parse_name in parse_name_list:
        parse_md5_old_dict[parse_name] = mydb.SelectDB(parse_name)
        print parse_md5_old_dict[parse_name]
        parse_md5_new_dict[parse_name] = []

if __name__ == 'units.md5update':
    print 'module md5 init ...'
    init_parse_md5()

def Md5YornExist(weburl,status,pname):
    urlmd5 = hashlib.md5(weburl.encode('utf-8')).hexdigest()
    global parse_md5_old_dict
    global parse_md5_new_dict
    global status_dict
    if urlmd5 in parse_md5_old_dict[pname]:
        #print "urlmd5 in oldlist"
        #print urlmd5
        #print parse_md5_old_dict[pname]
        return -1
    elif urlmd5 in parse_md5_new_dict[pname]:
        #print "urlmd5 in newlist"
        #print urlmd5
        #print parse_md5_new_dict[pname]
        return -1
    else: #新添加MD5
        #print "urlmd5 is not exist"
        parse_md5_new_dict[pname].append(urlmd5)
        status_dict[urlmd5] = status

        #更新数据库['md5','200','test']
        #print len(parse_md5_new_dict[pname])
        if len(parse_md5_new_dict[pname]) >= 5:
            print "new %s list over 5!" %(pname)
            #存放待插入数据库的rows [row1,row2...]
            insertlist = []
            #存放待插入数据库的row['md5',200,'pname']
            #insertrow = []
            #将新缓存数据写入数据库，并合并新旧缓存
            for md5 in parse_md5_new_dict[pname]:
                insertrow = []
                insertrow.append(md5)
                insertrow.append(status_dict[md5])
                insertrow.append(pname)
                insertlist.append(insertrow)
            print insertlist
            #if mydb.InsertDB(insertlist):
            #    print "InsertDB fail %s" %(str(insertlist))
            print "Write newmd5 to DB ok"
            parse_md5_old_dict[pname].extend(parse_md5_new_dict[pname])
            status_dict = {}
            print "md5 old is update"
            print parse_md5_old_dict
            parse_md5_new_dict[pname] = []
            print "md5 new is null"
        return 0

if __name__ == '__main__':
    print 'main init ...'
    url_list = [] #test1
    url_list2 = [] #test2
    line_list = []
    init_parse_md5()
    pname = 'test'
    for i in range(1,11):
        url_str = "http://ypk.39.net/comment/507831/%d.shtml" %i
        print url_str
        url_list.append(url_str)
    url_list2 = ["http://ypk.39.net/comment/507831/2.shtml","http://ypk.39.net/comment/507831/7.shtml","http://ypk.39.net/comment/507831/9.shtml","http://ypk.39.net/comment/507831/6.shtml"]
    for url in url_list:
        if Md5YornExist(url,'200',pname) == -1:
            print "url is already exist: %s" %(url)
        else: 
            print "url insert into []: %s" %(url)

    for url in url_list2:
        if Md5YornExist(url,'200',pname) == -1:
            print "url is already exist: %s" %(url)
        else:
            print "url insert into []: %s" %(url)

