--Editor by tangxingyu
USE data39net;
INSERT INTO tbl_drug_info_new_2
SELECT
    T5.yp_name
    ,third_class
    ,yp_id
    ,pic_src
    ,icons
    ,company
    ,stars
    ,star_count
    ,price
    ,yp_manual
    ,yp_comment
    ,T5.refer_urlmd5
FROM
(
    SELECT
        T3.yp_name
        ,T3.refer_urlmd5
        ,yp_id
        ,yp_manual
        ,yp_comment
    FROM
    (
        SELECT
            T1.yp_name
            ,T1.refer_urlmd5
            ,yp_id
            ,yp_manual
            ,comment_urlmd5
        FROM
            base_drug_gaishu T1
        INNER JOIN
            base_drug_manual T2
        ON
        (T1.manual_urlmd5 = T2.refer_urlmd5)
    ) T3
    INNER JOIN
        base_drug_comment T4
    ON
    (T3.comment_urlmd5 = T4.refer_urlmd5)
) T5
LEFT JOIN
    base_drug_search T6
ON
(T5.refer_urlmd5 = T6.yps_next_md5)
WHERE
    T5.yp_name is not null
