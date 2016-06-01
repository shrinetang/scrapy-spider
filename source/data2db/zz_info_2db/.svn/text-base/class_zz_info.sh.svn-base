#!/bin/bash
cat $1| awk -F"\t" '{if($1=="zz_menu") print $1"\t"$2"\t"$3}'|awk -F"\t" '{split($3,zzlist,";;"); for(zz in zzlist) print $2"\t"zzlist[zz]}' >$2_db_zz_class
cat $1| awk -F"\t" '{if($1=="zz_info")print $2"\t"$3"\t"$4"\t"$5"\t"$6}' >$2_db_zz_info
