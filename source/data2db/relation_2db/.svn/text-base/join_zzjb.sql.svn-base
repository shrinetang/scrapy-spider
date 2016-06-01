USE data39net;

INSERT INTO tbl_zzjb_relation
SELECT
    zz_name
    ,T2.jb_name
    ,zz_dzyp
    ,intros as jb_intros
    ,yibao
    ,dxzhenzhuang
    ,complication
FROM
    tbl_zz_info_xgjb T1
INNER JOIN
    tbl_jb_info T2
ON
(T1.xgjb = T2.jb_name)
