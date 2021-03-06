#!/bin/env python
# coding: utf-8

import glob
import sys
import datetime
import os

import API.M6 as M6
import connection_info as info

# 데이터 경로 받고, 처리할 전체 라인 저장
try:
    data_path = sys.argv[1]
    tmp_path = "{0}/tmp/{1}".format(data_path.split("/")[0], data_path.split("/")[-1])
    full_line = int(os.popen('cat {} | wc -l'.format(data_path)).read().rstrip())
except:
    raise Exception("MISSING CSV_PATH")

# 테이블 정보가 있는 경로와 파싱된 데이터가 저장될 경로 지정
schema_path = "table_schema/LOAD_7"  # 125기가짜리 넣을때
table_name = "LOAD_7"

with open(schema_path, 'r') as f:
    ctl = f.readline()\
            .rstrip()\
            .replace("\"", "")\
            .replace("GEOM","+GEOM")\
            .replace("+GEOM_LEVEL","GEOM_LEVEL")\
            .replace("+GEOM_JSON","GEOM_JSON")\
            .replace(",", "\n")

############################################################################################
""" 스키마 파일에서 뽑아온 정보를 기반으로 실제 삽입할 데이터 만들기
"""
import time
import codecs
import json

start = time.time()
with codecs.open(data_path, 'r', encoding='utf-8-sig') as f:
    with codecs.open(tmp_path, 'w', encoding='utf-8-sig') as tmpwf:
        conn = M6.Connection(info.host, info.user_id, info.user_passwd, Direct=info.direct, Database=info.database)
        c = conn.Cursor()
        c.SetFieldSep(info.field_sep)
        c.SetRecordSep(info.record_sep)
    
        f.readline()
        line = 1
        dat = ""
        for origin_data in f:
            origin_data = origin_data.replace("\"", "").replace(",", info.field_sep).rstrip()
            print("Making Data ... ({}/{})".format(line, full_line-1))
            data_list = origin_data.split(info.field_sep)
    
            # time_idx가 -1이면 GLOBAL테이블이므로 partition_date 없음
            if time_idx != -1:
                partition_date = data_list[time_idx-2].split(".")[0]  # 125GB짜리 할때
            else:
                partition_date = None
    
            # TODO: partition_key는 0으로, geo_level은 공백으로 초기화
            partition_key = "0"
            geom_level = ""
    
            # time_idx가 -1이면 GLOBAL테이블이므로 partition_key, partition_date 없음
            if time_idx != -1:
                parsed_data = partition_date + info.field_sep + partition_key + info.field_sep + origin_data.rstrip() + info.record_sep
            elif time_idx == -1:
                parsed_data = origin_data.rstrip() + info.record_sep
    
            tmpwf.write(parsed_data)
            line += 1
    
        #with open(tmp_path, "r") as tmprf:
        #    dat = tmprf.read().rstrip()
        #    print("Making Data is Completed, Now Start Loading")
        #    print(c.LoadString(table_name, data_path[-6:-4], "20190116000000", ctl, dat))

# os.remove(tmp_path)
print(time.time() - start)
