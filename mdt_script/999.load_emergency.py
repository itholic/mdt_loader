#!/bin/env python
# coding: utf-8

import sys
import os
import time

import API.M6 as M6
import connection_info as info

table_name = sys.argv[1]
data = "parsed_data/{}".format(table_name)
schema = "table_schema/{}".format(table_name)
conn = M6.Connection(info.host, info.user_id, info.user_passwd, Direct=info.direct, Database=info.database)
c = conn.Cursor()
c.SetFieldSep(info.field_sep)
c.SetRecordSep(info.record_sep)

# ctl파일은 스키마 파일 컬럼목록의 GEOM앞에 +를 붙여주고, Record Seperator를 지정해주면 된다.
# TODO: GEOM replace 규칙 정규식으로 바꾸기
with open(schema) as f:
    ctl = f.readline()\
            .rstrip()\
            .replace("\"", "")\
            .replace("GEOM","+GEOM")\
            .replace("+GEOM_LEVEL","GEOM_LEVEL")\
            .replace("+GEOM_JSON","GEOM_JSON")\
            .replace(",", "\n")


with open(data) as f:
    dat = ""
    key = 0
    partition_date = "20181101000000"
    load_dict = {}
    file_line = int(os.popen('cat {} | wc -l'.format(data)).read().rstrip())
    for i, line in enumerate(f):
        if partition_date == line.split(info.field_sep)[0][:10] + "0000":
            dat += line
        else:
            print("LOAD : {}".format(partition_date))
            print(c.LoadString(table_name, "0", partition_date, ctl, dat))
            # time.sleep(2)
            dat = line
            partition_date = line.split(info.field_sep)[0][:10] + "0000"

        print("({}/{})".format(i+1, file_line))

c.Close()
conn.close()

