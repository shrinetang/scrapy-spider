#!/bin/bash
cat $1| awk -F"\t" '{if($1=="jb_menu") print $2"\t"$3}' >$2_db_jb_class
cat $1| awk -F"\t" '{if($1=="jb_info") print $2"\t"$3"\t"$4"\t"$5}' >$2_db_jb_info_nosp
