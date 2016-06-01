#!/bin/bash
fname1=$1_db_zz_class
fname2=$1_db_zz_info
fname3=$1_db_zz_info_dzyp
fname4=$1_db_zz_info_xgjb

if [ -e $fname1 ]
then
     echo "File zz_class exists"
else
     echo "File zz_class not exist"
     exit
fi
echo "loading zz_class ..."
mysql -uroot -hlocalhost -proot data39net --local-infile=1 -e "load data local infile '$1_db_zz_class' into table tbl_zz_class fields terminated by '\t'"


if [ -e $fname2 ]
then
     echo "File zz_info exists"
else
     echo "File zz_info not exist"
     exit
fi
echo "loading zz_info ..."
mysql -uroot -hlocalhost -proot data39net --local-infile=1 -e "load data local infile '$1_db_zz_info' into table tbl_zz_info fields terminated by '\t'"


if [ -e $fname3 ]
then
     echo "File zz_info_dzyp exists"
else
     echo "File zz_info_dzyp exist"
     exit
fi
echo "loading zz_info_dzyp ..."
mysql -uroot -hlocalhost -proot data39net --local-infile=1 -e "load data local infile '$1_db_zz_info_dzyp' into table tbl_zz_info_dzyp fields terminated by '\t'"


if [ -e $fname4 ]
then
     echo "File zz_info_xgjb exists"
else
     echo "File zz_info_xgjb not exist"
     exit
fi
echo "loading zz_info_xgjb ..."
mysql -uroot -hlocalhost -proot data39net --local-infile=1 -e "load data local infile '$1_db_zz_info_xgjb' into table tbl_zz_info_xgjb fields terminated by '\t'"

echo "loading OK"
echo $?
