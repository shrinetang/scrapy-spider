CREATE DATABASE IF NOT EXISTS data39net default charset utf8 COLLATE utf8_general_ci;
USE data39net;

CREATE TABLE IF NOT EXISTS `tbl_jbyp_relation`(
    `jb_name`       varchar(100)  NOT NULL DEFAULT '' COMMENT '疾病名',
    `yibao`         varchar(100)  NOT NULL DEFAULT '' COMMENT '是否医保',
    `dxzhenzhuang`  varchar(200)  NOT NULL DEFAULT '' COMMENT '典型症状',
    `yp_name`       varchar(100)  NOT NULL DEFAULT '' COMMENT '药品名称',
    `yp_id`         varchar(100)  NOT NULL DEFAULT '' COMMENT '药品国标准号',
    `yp_manual`     varchar(2000) NOT NULL DEFAULT '' COMMENT '药品说明书',
    `yp_comment`    varchar(1000) NOT NULL DEFAULT '' COMMENT '药品评价'
) ENGINE=innoDB DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS `tbl_zzjb_relation`(
    `zz_name`       varchar(100)   NOT NULL DEFAULT '' COMMENT '症状名',
    `jb_name`       varchar(100)   NOT NULL DEFAULT '' COMMENT '疾病名',
    `zz_dzyp`       varchar(500)   NOT NULL DEFAULT '' COMMENT '对症药品',
    `jb_intros`     varchar(1000)  NOT NULL DEFAULT '' COMMENT '疾病介绍',
    `yibao`         varchar(100)   NOT NULL DEFAULT '' COMMENT '是否医保疾病',
    `dxzhenzhuang`  varchar(200)  NOT NULL DEFAULT '' COMMENT '疾病典型症状',
    `complication`  varchar(200)  NOT NULL DEFAULT '' COMMENT '疾病伴随症状'
) ENGINE=innoDB DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS `tbl_zzyp_relation`(
    `zz_name`    varchar(100)   NOT NULL DEFAULT '' COMMENT '症状名',
    `yp_name`    varchar(100)   NOT NULL DEFAULT '' COMMENT '药品名',
    `yp_id`      varchar(100)   NOT NULL DEFAULT '' COMMENT '药品国药准字',
    `company`    varchar(100)   NOT NULL DEFAULT '' COMMENT '生产厂家',
    `yp_manual`  varchar(2000)  NOT NULL DEFAULT '' COMMENT '药品说明书',
    `yp_comment` varchar(1000)  NOT NULL DEFAULT '' COMMENT '药品评价',
    `zz_xgjb`    varchar(500)   NOT NULL DEFAULT '' COMMENT '症状相关疾病'
) ENGINE=innoDB DEFAULT CHARSET=utf8;


