CREATE DATABASE IF NOT EXISTS data39net default charset utf8 COLLATE utf8_general_ci;
USE data39net;

CREATE TABLE IF NOT EXISTS `tbl_jb_info_new_2`(
    `jb_name`       varchar(100)   NOT NULL DEFAULT '' COMMENT '疾病名称',
    `intros`        varchar(1000)  NOT NULL DEFAULT '' COMMENT '疾病介绍',
    `other_name`    varchar(100)   NOT NULL DEFAULT '' COMMENT '别名',
    `yibao`         varchar(100)   NOT NULL DEFAULT '' COMMENT '是否医保',
    `body_part`     varchar(100)   NOT NULL DEFAULT '' COMMENT '发病部位',
    `cure_room`     varchar(100)   NOT NULL DEFAULT '' COMMENT '治疗科室',
    `infect`        varchar(100)   NOT NULL DEFAULT '' COMMENT '是否传染',
    `cure_method`   varchar(100)   NOT NULL DEFAULT '' COMMENT '治疗方法',
    `cure_prob`     varchar(100)   NOT NULL DEFAULT '' COMMENT '治愈概率',
    `crowd`         varchar(100)   NOT NULL DEFAULT '' COMMENT '高发人群',
    `cost`          varchar(100)   NOT NULL DEFAULT '' COMMENT '花费',
    `jbexam`        varchar(100)   NOT NULL DEFAULT '' COMMENT '检查方式',
    `dxzhenzhuang`  varchar(100)   NOT NULL DEFAULT '' COMMENT '典型症状',
    `complication`  varchar(100)   NOT NULL DEFAULT '' COMMENT '伴随症状',
    `xgyplist`      varchar(500)   NOT NULL DEFAULT '' COMMENT '相关药品列表',
    PRIMARY KEY (`jb_name`)
) ENGINE=innoDB DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS `tbl_jb_info_dzyp`(
    `jb_name`       varchar(100)   NOT NULL DEFAULT '',
    `intros`        varchar(1000)  NOT NULL DEFAULT '',
    `other_name`    varchar(100)   NOT NULL DEFAULT '',
    `yibao`         varchar(100)   NOT NULL DEFAULT '',
    `body_part`     varchar(100)   NOT NULL DEFAULT '',
    `cure_room`     varchar(100)   NOT NULL DEFAULT '',
    `infect`        varchar(100)   NOT NULL DEFAULT '',
    `cure_method`   varchar(100)   NOT NULL DEFAULT '',
    `cure_prob`     varchar(100)   NOT NULL DEFAULT '',
    `crowd`         varchar(100)   NOT NULL DEFAULT '',
    `cost`          varchar(100)   NOT NULL DEFAULT '',
    `dxzhenzhuang`  varchar(100)   NOT NULL DEFAULT '',
    `complication`  varchar(100)   NOT NULL DEFAULT '',
    `dzyp`          varchar(100)   NOT NULL DEFAULT '',
    PRIMARY KEY (`jb_name`,`dzyp`)
) ENGINE=innoDB DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS `tbl_jb_class`(
    `jb_type`    varchar(100)   NOT NULL DEFAULT '',
    `jb_name`    varchar(100)   NOT NULL DEFAULT '',
) ENGINE=innoDB DEFAULT CHARSET=utf8;
