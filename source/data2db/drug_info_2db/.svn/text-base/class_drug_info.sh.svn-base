#!/bin/bash
echo $1 $2
#cat $1|awk -F"\t" '{if($1=="drugmenu") print $2"\t"$3"\t"$4"\t"$5}' >$2_db_menu
cat $1|awk -F"\t" '{if($1=="drugsearch") print $2"\t"$3"\t"$4"\t"$5"\t"$6"\t"$7"\t"$8"\t"$9"\t"$10"\t"$11}' >$2_db_search
cat $1|awk -F"\t" '{if($1=="druggaishu") print $2"\t"$3"\t"$4"\t"$5}' >$2_db_gaishu
cat $1|awk -F"\t" '{if($1=="drugmanual") print $2"\t"$3"\t"$4"\t"$5}' >$2_db_manual
cat $1|awk -F"\t" '{if($1=="drugcmt")    print $2"\t"$3"\t"$4}'|awk -F"\t" '{merge[$1"\t"$2]=merge[$1"\t"$2]$3"-";} END{for(name in merge) print name"\t"merge[name]}' >$2_db_comment
