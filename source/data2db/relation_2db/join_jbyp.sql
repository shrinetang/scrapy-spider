USE data39net;

INSERT INTO tbl_jbyp_relation
SELECT
    jb_name
    ,yibao
    ,dxzhenzhuang
    ,yp_name
    ,yp_id
    ,yp_manual
    ,yp_comment
FROM
    tbl_drug_info T1
INNER JOIN
    tbl_jb_info_dzyp T2
ON
(T2.dzyp = T1.yp_name)

