#! /usr/bin/env python
# -*- coding:utf-8 -*-
#从res_zz_info输出导入到tbl_zz_info中,不切分最后的药品列表
import re
import string
import sys
import os
perr = sys.stderr
pout = sys.stdout

err_num = 0
line_num = 0
filename = sys.argv[1]
jb_key_list = ['别名','医保','发病部位','科室','传染性','治疗方法','治愈率','人群','治疗费用','临床检查','典型症','并发症']
jb_kv_dict = {}
for jb_key in jb_key_list:
    jb_kv_dict[jb_key] = '-'

f = open(filename,'r')
#f = open('test','r')
for eachline in f:
    try:
        eachline = eachline.strip().replace('...','')
        fields = re.split('\t',eachline)
        jb_name  = fields[0]
        jb_intro = fields[1]
        jb_kv_list = re.split(';;',fields[2])
        if len(fields)>=4:
            jb_yp_str = fields[3]
        else:
            jb_yp_str = '-'
        if not jb_kv_list and (type(jb_kv_list) != type([])):
            perr.write(eachline+'\n')
            err_num += 1
            continue
        for jb_kv in jb_kv_list:
            kv_list = re.split('::',jb_kv)
            if not kv_list and len(kv_list)!=2: #如果k::v 为空则跳过
                perr.write(eachlinei+'\n')
                err_num += 1
                continue
            if kv_list[0] and kv_list[1]: #存在Kv
                for jb_key in jb_key_list:
                    if kv_list[0].find(jb_key) != -1 :
                        jb_kv_dict[jb_key] = kv_list[1]
                        break

        print jb_name + '\t' + jb_intro + '\t' + jb_kv_dict['别名'] + '\t' + jb_kv_dict['医保'] + '\t' + jb_kv_dict['发病部位'] + '\t' + jb_kv_dict['科室'] + '\t' + jb_kv_dict['传染性'] + '\t' + jb_kv_dict['治疗方法'] + '\t' + jb_kv_dict['治愈率'] + '\t' + jb_kv_dict['人群'] + '\t' + jb_kv_dict['治疗费用'] + '\t' + jb_kv_dict['临床检查'] + '\t' + jb_kv_dict['典型症'] + '\t' + jb_kv_dict['并发症'] + '\t' + jb_yp_str 
        line_num += 1
    except IndexError,e:
        perr.write(eachline+'\n')
        err_num += 1
        continue
perr.write("\nerr_num= %d" %err_num)
perr.write("\nline_num= %d\n" %line_num)
