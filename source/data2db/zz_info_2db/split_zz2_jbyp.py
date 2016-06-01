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
select = sys.argv[2] #选择是给哪个列表进行拆分

f = open(filename,'r')
#f = open('res_zz_info','r')
for eachline in f:
    try:
        eachline = eachline.strip().replace('...','')
        fields = re.split('\t',eachline)
        zz_name = fields[0]
        zz_ques = fields[1]
        zz_answ = fields[2]
        if len(fields)>=4:
            zz_xgjb = fields[3]
        else:
            zz_xgjb = ''
        if len(fields)>=5:
            zz_dzyp = fields[4]
        else:
            zz_dzyp = ''
        if select == 'zz_dzyp':
            zz_dzyp_list = re.split(';;',zz_dzyp)
            if not zz_dzyp_list:
                err_num += 1
                continue
            for dzyp in zz_dzyp_list:
                print zz_name + '\t' + zz_ques + '\t' +zz_answ +'\t' + dzyp + '\t' + zz_xgjb
        elif select == 'zz_xgjb':
            zz_xgjb_list = re.split(';;',zz_xgjb)
            if not zz_xgjb_list:
                err_num += 1
                continue
            for xgjb in zz_xgjb_list:
                print zz_name + '\t' + zz_ques + '\t' +zz_answ +'\t' + zz_dzyp + '\t' + xgjb
        else:
            print 'SELECTX ERROR'
            break
        line_num += 1
    except IndexError,e:
        err_num += 1
        continue
#print line_num
#print line_drop_num
#print err_num
perr.write("line_num= %d" %line_num)
perr.write("err_num= %d" %err_num)
