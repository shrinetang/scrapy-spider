CREATE DATABASE IF NOT EXISTS data39net default charset utf8 COLLATE utf8_general_ci;
USE data39net;

CREATE TABLE IF NOT EXISTS `tbl_zz_class`(
    `zz_type`    varchar(100)   NOT NULL DEFAULT '' COMMENT '症状分类名',
    `zz_name`    varchar(100)   NOT NULL DEFAULT '' COMMENT '症状名称' 
) ENGINE=innoDB DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS `tbl_zz_info`(
    `zz_name`    varchar(100)   NOT NULL DEFAULT '' COMMENT '症状名称',
    `question`   varchar(100)   NOT NULL DEFAULT '' COMMENT '症状问',
    `answer`     varchar(1000)  NOT NULL DEFAULT '' COMMENT '症状解释',
    `zz_xgjb`    varchar(500)   NOT NULL DEFAULT '' COMMENT '相关疾病列表',
    `zz_dzyp`    varchar(500)   NOT NULL DEFAULT '' COMMENT '对症药品列表',
    PRIMARY KEY (`zz_name`)
) ENGINE=innoDB DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS `tbl_zz_info_dzyp`(
    `zz_name`    varchar(100)   NOT NULL DEFAULT '',
    `question`   varchar(100)   NOT NULL DEFAULT '',
    `answer`     varchar(1000)  NOT NULL DEFAULT '',
    `dzyp`       varchar(100)   NOT NULL DEFAULT '',
    `zz_xgjb`    varchar(500)   NOT NULL DEFAULT '',
    PRIMARY KEY (`zz_name`,`dzyp`)
) ENGINE=innoDB DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS `tbl_zz_info_xgjb`(
    `zz_name`    varchar(100)   NOT NULL DEFAULT '',
    `question`   varchar(100)   NOT NULL DEFAULT '',
    `answer`     varchar(1000)  NOT NULL DEFAULT '',
    `zz_dzyp`    varchar(500)   NOT NULL DEFAULT '',
    `xgjb`       varchar(100)   NOT NULL DEFAULT '',
    PRIMARY KEY (`zz_name`,`xgjb`)
) ENGINE=innoDB DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS `tbl_zzjb_relation`(
    `zz_name`       varchar(100)   NOT NULL DEFAULT '' COMMENT '症状名',
    `jb_name`       varchar(100)   NOT NULL DEFAULT '' COMMENT '对应疾病名称',
    `zz_dzyp`       varchar(500)   NOT NULL DEFAULT '' COMMENT '对症药品列表',
    `intros`        varchar(1000)  NOT NULL DEFAULT '' COMMENT '症状介绍',
    `yibao`         varchar(100)   NOT NULL DEFAULT '' COMMENT '是否为医保',
    `dxzhenzhuang`  varchar(2000)  NOT NULL DEFAULT '' COMMENT '典型症状',
    `complication`  varchar(1000)  NOT NULL DEFAULT '' COMMENT '伴随症状',
) ENGINE=innoDB DEFAULT CHARSET=utf8;

