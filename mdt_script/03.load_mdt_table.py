# -*- coding: utf-8 -*-

"""02.make_data_from_csv.py를 통해 만든 데이터를 실제로 로딩하기 위한 프로그램"""

import sys
import os

import API.M6 as M6
import connection_info as info

try:
    schema_path = sys.argv[1]
    table_name = sys.argv[1].split("/")[-1].upper()
except:
    raise Exception("MISSING TABLE_NAME, python 06.load_mdt_table.py [TABLE_NAME]")

# 한 번에 로딩할 데이터 갯수
load_per_once = 10000
data_path = "parsed_data/"

# 분할할 key 갯수
X = 40

conn = M6.Connection(info.host, info.user_id, info.user_passwd, Direct=info.direct, Database=info.database)
c = conn.Cursor()
c.SetFieldSep(info.field_sep)
c.SetRecordSep(info.record_sep)

# ctl파일은 스키마 파일 컬럼목록의 GEOM앞에 +를 붙여주고, Record Seperator를 지정해주면 된다.
# TODO: GEOM replace 규칙 정규식으로 바꾸기
with open(schema_path) as f:
    ctl = f.readline()\
            .rstrip()\
            .replace("\"", "")\
            .replace("GEOM","+GEOM")\
            .replace("+GEOM_LEVEL","GEOM_LEVEL")\
            .replace("+GEOM_JSON","GEOM_JSON")\
            .replace(",", "\n")

# ==============================================================================================

print(ctl)

import time
start = time.time()
# dat파일은 parsed_data 경로에 있는 데이터 파일 자체이다.
with open(data_path + table_name) as f:
    print(data_path + table_name)
    file_line = int(os.popen('cat {} | wc -l'.format(data_path + table_name)).read().rstrip())
    file_line_div_x = file_line // X
    dat = ""
    key = 1
    for i, line in enumerate(f):
        dat += line
        if (i+1) % file_line_div_x == 0:
            key += 1

        if (i+1) % load_per_once == 0:
            print(c.LoadString(table_name, "K{}".format(key), '20190110000000', ctl, dat))
            print("({}/{}), KEY: {}".format(i+1, file_line, "K{}".format(key)))
            dat = ""
        elif (i+1) == file_line:
            print(c.LoadString(table_name, "K{}".format(key), '20190110000000', ctl, dat)) 

print(time.time() - start)

c.Close()
conn.close()

