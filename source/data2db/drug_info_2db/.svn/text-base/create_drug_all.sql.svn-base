--editor by xingyu

CREATE DATABASE IF NOT EXISTS data39net default charset utf8 COLLATE utf8_general_ci;
USE data39net;

CREATE TABLE IF NOT EXISTS `base_drug_search`(
    `refer_urlmd5`   varchar(100)   NOT NULL DEFAULT '' COMMENT 'referurlmd5',
    `third_class`    varchar(100)   NOT NULL DEFAULT '' COMMENT '三级分类',
    `yp_name`        varchar(100)   NOT NULL DEFAULT '' COMMENT '药品名',
    `pic_src`        varchar(100)   NOT NULL DEFAULT '' COMMENT '药品图片Src',
    `icons`          varchar(100)   NOT NULL DEFAULT '' COMMENT 'OTC属性',
    `company`        varchar(100)   NOT NULL DEFAULT '' COMMENT '生产厂家',
    `stars`          varchar(20)    NOT NULL DEFAULT '' COMMENT '评论星级',
    `star_count`     varchar(20)    NOT NULL DEFAULT '' COMMENT '评论数',
    `price`          varchar(100)   NOT NULL DEFAULT '' COMMENT '参考价格',
    `yps_next_md5`   varchar(100)   NOT NULL DEFAULT '' COMMENT '跳转URLMD5',
     PRIMARY KEY (`yps_next_md5`)
) ENGINE=innoDB DEFAULT CHARSET=utf8 COMMENT='药品检索原始数据表';

CREATE TABLE IF NOT EXISTS `base_drug_gaishu`(
    `yp_name`         varchar(100)   NOT NULL DEFAULT '' COMMENT '药品名',
    `refer_urlmd5`    varchar(100)   NOT NULL DEFAULT '' COMMENT 'refer url的MD5',
    `manual_urlmd5`   varchar(100)   NOT NULL DEFAULT '' COMMENT '跳转到manual url的MD5',
    `comment_urlmd5`  varchar(100)   NOT NULL DEFAULT '' COMMENT '跳转到comment url的MD5',
    PRIMARY KEY (`refer_urlmd5`)
) ENGINE=innoDB DEFAULT CHARSET=utf8 COMMENT '药品概述原始数据表';

CREATE TABLE IF NOT EXISTS `base_drug_manual`(
    `yp_name`      varchar(100)   NOT NULL DEFAULT ''  COMMENT '药品名',
    `yp_id`        varchar(100)   NOT NULL DEFAULT ''  COMMENT '药品国批号',
    `refer_urlmd5` varchar(100)   NOT NULL DEFAULT ''  COMMENT 'refer',
    `yp_manual`    varchar(2000)  NOT NULL DEFAULT ''  COMMENT 'kv字典的{}形式存放的药品属性',
     PRIMARY KEY (`refer_urlmd5`)
) ENGINE=innoDB DEFAULT CHARSET=utf8 COMMENT='药品说明书原始数据表';

CREATE TABLE IF NOT EXISTS `base_drug_comment`(
    `yp_name`       varchar(100)   NOT NULL DEFAULT ''  COMMENT '药品名称',
    `refer_urlmd5`  varchar(100)   NOT NULL DEFAULT ''  COMMENT 'refer',
    `yp_comment`    varchar(5000)  NOT NULL DEFAULT ''  COMMENT '药品评价列表',
     PRIMARY KEY (`refer_urlmd5`)
) ENGINE=innoDB DEFAULT CHARSET=utf8 COMMENT='药品评价原始数据表';

CREATE TABLE IF NOT EXISTS `tbl_drug_info_new_2`(
    `yp_name`       varchar(100)   NOT NULL DEFAULT ''  COMMENT '药品名',
    `third_class`   varchar(100)   NOT NULL DEFAULT ''  COMMENT '药品分类',
    `yp_id`         varchar(100)   NOT NULL DEFAULT ''  COMMENT '药品国批号',
    `pic_src`       varchar(100)   NOT NULL DEFAULT ''  COMMENT '药品图片Src',
    `icons`         varchar(100)   NOT NULL DEFAULT ''  COMMENT 'OTC属性',
    `company`       varchar(100)   NOT NULL DEFAULT ''  COMMENT '生产厂家',
    `stars`         varchar(100)   NOT NULL DEFAULT ''  COMMENT '评论星级',
    `star_count`    varchar(100)   NOT NULL DEFAULT ''  COMMENT '评论数',
    `price`         varchar(100)   NOT NULL DEFAULT ''  COMMENT '参考价格',
    `yp_manual`     varchar(2000)  NOT NULL DEFAULT ''  COMMENT '药品说明书',
    `yp_comment`    varchar(1000)  NOT NULL DEFAULT ''  COMMENT '药品评论',
    `url_md5`       varchar(100)   NOT NULL DEFAULT ''  COMMENT 'url_md5',
     PRIMARY KEY (`url_md5`)
) ENGINE=innoDB DEFAULT CHARSET=utf8 COMMENT='药品信息汇总表';
