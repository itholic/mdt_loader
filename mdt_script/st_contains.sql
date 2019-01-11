-- 특정 컬럼의 데이터가 해당 범위 안에 존재하는지 질의하기위한 샘플쿼리

select
    *
from
    PM_RTT_SCORE
WHERE
    st_contains(geomfromtext('polygon((28.621964 77.245142, 28.621964 77.210483, 28.602121 77.210483, 28.602121 77.245142, 28.621964 77.245142))'), geom);

================

select
    count(*)
from
    PM_RTT_ScORE
WHERE
    st_contains(geomfromtext('polygon((28.621964 77.245142, 28.621964 77.210483, 28.602121 77.210483, 28.602121 77.245142, 28.621964 77.245142))'), geom);
