#! /usr/bin/env python
# -*- coding:utf-8 -*-
#从res_zz_info输出导入到tbl_zz_info中
import re
import string
import sys
import os
perr = sys.stderr
pout = sys.stdout

err_num = 0
line_num = 0
filename = sys.argv[1]

f = open(filename,'r')
#f = open('test','r')
for eachline in f:
    try:
        #eachline = eachline.strip().replace('...','')
        fields = re.split('\t',eachline)
        jb_name     = fields[0]
        intro       = fields[1]
        other_name  = fields[2]
        yibao       = fields[3]
        body_part   = fields[4]
        cure_room   = fields[5]
        infect      = fields[6]
        cure_method = fields[7]
        cure_prob   = fields[8]
        crowd       = fields[9]
        cost        = fields[10]
        check       = fields[11]
        dxzhenzhuang= fields[12]
        complication= fields[13]
        if len(fields)>=15:
            xgypstr = fields[14]
        else:
            xgypstr = ''
        if not xgypstr:
            xgyplist = []
        xgyplist = re.split(',',fields[14])
        for xgyp in xgyplist:
            print jb_name + '\t' + intro + '\t' + other_name + '\t' + yibao + '\t' + body_part + '\t' + cure_room + '\t' + infect + '\t' + cure_method + '\t' + cure_prob + '\t' + crowd + '\t' + cost + '\t' + dxzhenzhuang + '\t' + complication + '\t' + xgyp
        line_num += 1
    except IndexError,e:
        err_num += 1
        continue

perr.write("line_num= %d" %line_num)
perr.write("err_num= %d" %err_num)
