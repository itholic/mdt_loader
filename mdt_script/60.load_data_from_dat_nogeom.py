#!/bin/env python
# coding: utf-8

import sys
import time

import API.M6 as M6
import connection_info as info

# 데이터 경로 받고, 처리할 전체 라인 저장
try:
    data_path = sys.argv[1]
except:
    raise Exception("MISSING DAT_PATH")

conn = M6.Connection(info.host, info.user_id, info.user_passwd, Direct=info.direct, Database=info.database)
c = conn.Cursor()
c.SetFieldSep(info.field_sep)
c.SetRecordSep(info.record_sep)

# 테이블 정보가 있는 경로와 파싱된 데이터가 저장될 경로 지정
schema_path = "table_schema/MDT_JAPAN_LOAD"  # 125기가짜리 넣을때
table_name = "MDT_JAPAN_LOAD"

with open(schema_path, 'r') as f:
    ctl = f.readline().rstrip().replace("\"", "").replace(",","\n")

start = time.time()

with open(data_path, "r") as f:
    dat = f.read().rstrip()
    print(c.LoadString(table_name, data_path[-6:-4], "20190116000000", ctl, dat))

print(time.time() - start)
