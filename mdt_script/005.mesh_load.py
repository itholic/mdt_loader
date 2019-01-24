#!/bin/env python
# coding: utf-8

import sys
import os

import API.M6 as M6
import connection_info as info

try:
    schema_path = sys.argv[1]
    table_name = sys.argv[1].split("/")[-1].upper()
    mesh_level = int(sys.argv[2])
    X = 1 if mesh_level == 1 \
            else 2 if mesh_level == 2 \
            else 200
except:
    raise Exception("MISSING TABLE_NAME, python 005.mesh_load.py [SCHEMA_PATH] [GEOM_LEVEL]")

# data_path = "parsed_data/"
data_path = "mesh_data/"


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
import glob


# FIXME level에따라 path명 바꿔주기
# data_list = glob.glob(data_path+"/*")
data = "{}/mesh_lv{}".format(data_path, mesh_level)
# print(data_list)
print(data)

start = time.time()

table_name = "JP_MESH_TEST"
# for data in data_list:
with open(data) as f:
    dat = ""
    key = 1
    full_line = int(os.popen('cat {} | wc -l'.format(data)).read().rstrip())
    load_per_once = full_line // X
    for i, line in enumerate(f):
        dat += line
        if (i+1) % load_per_once == 0 and (i+1) != full_line:
            print(c.LoadString(table_name, "K{}_{}".format(mesh_level, key), "20190117000000", ctl, dat))
            print("({}/{})".format(i+1, full_line))
            dat = ""
            key += 1
        elif (i+1) == full_line:
            print(c.LoadString(table_name, "K{}_{}".format(mesh_level, key), "20190117000000", ctl, dat))

print(time.time() - start)

c.Close()
conn.close()
