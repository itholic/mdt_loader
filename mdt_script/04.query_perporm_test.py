#!/bin/env python
# coding: utf-8

import time

import API.M6 as M6
import connection_info as info

conn = M6.Connection(info.host, info.user_id, info.user_passwd, Direct=info.direct, Database=info.database)
c = conn.Cursor()
c.SetFieldSep('|^|')
c.SetRecordSep('|^-^|')

test_table_list = ["PM_RTT_SCORE", "PM_NPR", "CL_DELHI_ENB_CELL", "CL_DELHI_ENB_CELL_COVERAGE_USER", "CL_DELHI_ENB_CELL_COVERAGE_CELL", "PM_RTT_SQUARE"]
# test_table_list = ["PM_NPR"]

q_fetch = """
    SELECT
        *
    FROM
        {}
    WHERE
        st_contains(geomfromtext('polygon((28.621964 77.245142, 28.621964 77.210483, 28.602121 77.210483, 28.602121 77.245142, 28.621964 77.245142))'), geom);
"""

q_count = """
    SELECT
        count(*)
    FROM
        {}
    WHERE
        st_contains(geomfromtext('polygon((28.621964 77.245142, 28.621964 77.210483, 28.602121 77.210483, 28.602121 77.245142, 28.621964 77.245142))'), geom);

"""

for table in test_table_list:
    start = time.time()
    print("================{}================".format(table))
    c.Execute2(q_fetch.format(table))
    print("select: {}".format(time.time() - start))
    start = time.time()
    c.Execute2(q_count.format(table))
    print("count: {}".format(time.time() - start))
    print("")
    print("")

c.Close()
conn.close()
