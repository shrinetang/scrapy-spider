#!/bin/bash
fname1=$1_db_jb_info
fname2=$1_db_jb_class
if [ -e $fname1 ]
then
     echo "File jb_info exists"
else
     echo "File jb_info not exist"
     exit
fi
echo "loading jb_info ..."
#mysql -uroot -hlocalhost -proot data39net --local-infile=1 -e "load data local infile '$1_db_jb_info' into table tbl_jb_info_new_2 fields terminated by '\t'"

if [ -e $fname1 ]
then
     echo "File zz_class exists"
else
     echo "File zz_class not exist"
     exit
fi
echo "loading jb_class ..."
mysql -uroot -hlocalhost -proot data39net --local-infile=1 -e "load data local infile '$1_db_jb_class' into table tbl_jb_class fields terminated by '\t'"

echo "loading OK"
echo $?
