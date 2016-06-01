USE data39net;

INSERT INTO tbl_zzyp_relation
SELECT
    zz_name
    ,T1.yp_name
    ,yp_id
    ,company
    ,yp_manual
    ,yp_comment
    ,zz_xgjb
FROM
    tbl_drug_info T1
INNER JOIN
    tbl_zz_info_dzyp T2
ON
(T2.dzyp = T1.yp_name)
