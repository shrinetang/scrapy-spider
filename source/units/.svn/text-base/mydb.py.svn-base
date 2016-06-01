#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ============================================================================
#    File: mydb.py
#
#    Desc: NULL
#
# Version: 1.0
#    Date: 2015-6-3
#  Author: tangxingyu
# Company: ZGWA
#Function: 实现数据库的读写（辅助md5single模块）
#                          --- Copyleft (c), 2015 ---
#                              All Rights Reserved.
# ============================================================================

import os
import sys
import MySQLdb
perr = sys.stderr
pout = sys.stdout

reload(sys)
sys.setdefaultencoding('utf-8')

def InsertDB(values):
    #print '-------------Insert DB----------------'
    #print values
    try:
        conn = MySQLdb.connect(host="localhost", user="root", passwd="root", db="spider", charset="utf8")
        cursor = conn.cursor()
        cursor.execute("SET NAMES utf8;")
        cursor.execute("SET CHARACTER SET utf8;")
        cursor.execute("SET character_set_connection=utf8;")
        for value in values:
            print value
            cursor.execute("insert into spider_urlmd5_record values(%s,%s,%s)",value)
        conn.commit()
        cursor.close()
        conn.close()
        #print '--------------Insert DB ok ---------------'
        return 0
    except MySQLdb.Error, e:
        perr.write("Mysql Error %d: %s" % (e.args[0], e.args[1]))
        return 1


def SelectDB(parse_name):
    rows = []
    row_list = []
    try:
        conn = MySQLdb.connect(host="localhost", user="root", passwd="root", db="spider", charset="utf8")
        cursor = conn.cursor()
        SQL = """
        SELECT `urlmd5`
        FROM   `spider_urlmd5_record`
        WHERE  `parse_name`='%s' and `status`='200'""" % (parse_name)
        cursor.execute(SQL)
        rows = cursor.fetchall()        
        for row in rows:
            row_str = ','.join(row)
            row_list.append(row_str)
        #print rows
        #rows_list = list(trows)
        #for row_tuple in rows_list:
        #    row_str =  row_tuple[0]
        #    rows.append(row_str)
        cursor.close()
        conn.close()
        return row_list
    except MySQLdb.Error, e:
        perr.write("Mysql Error %d: %s" % (e.args[0], e.args[1]))
        return []


if __name__ == '__main__':
    #values = [['hello3','200','test'],['hello4','200','test'],['hello5','200','test']]
    #InsertDB(values)
    #[u'afsf', u'hello']
    x = SelectDB('test')
    print x
