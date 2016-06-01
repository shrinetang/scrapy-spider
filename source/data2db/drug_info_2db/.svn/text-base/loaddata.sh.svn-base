#!/bin/bash
fname1=$1_db_search
fname2=$1_db_gaishu
fname3=$1_db_manual
fname4=$1_db_comment
if [ -e $fname1 ]
then
     echo "File search exists"
else
     echo "File search not exist"
     exit
fi
if [ -e $fname2 ]
then
     echo "File gaishu exists"
else
     echo "File gaishu not exist"
     exit
fi
if [ -e $fname3 ]
then
     echo "File manual exists"
else
     echo "File manual not exist"
     exit
fi
if [ -e $fname4 ]
then
     echo "File comment exists"
else
     echo "File comment not exist"
     exit
fi

#mysql -uroot -hlocalhost -proot data39net --local-infile=1 -e "load data local infile '$1_db_menu' into table tbl_drug_menu fields terminated by '\t'"
echo "loading search ...."
mysql -uroot -hlocalhost -proot data39net --local-infile=1 -e "load data local infile '$1_db_search' into table base_drug_search fields terminated by '\t'"
echo "loading gaishu ...."
mysql -uroot -hlocalhost -proot data39net --local-infile=1 -e "load data local infile '$1_db_gaishu' into table base_drug_gaishu fields terminated by '\t'"
echo "loading manual ...."
mysql -uroot -hlocalhost -proot data39net --local-infile=1 -e "load data local infile '$1_db_manual' into table base_drug_manual fields terminated by '\t'"
echo "loading comment ...."
mysql -uroot -hlocalhost -proot data39net --local-infile=1 -e "load data local infile '$1_db_comment' into table base_drug_comment fields terminated by '\t'"
echo "loading OK"
echo $?
