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
schema_path = "table_schema/MDT_JAPAN"  # 125기가짜리 넣을때
table_name = "MDT_JAPAN"

geom_info_list = []
with open(schema_path, 'r') as f:
    for i, line in enumerate(f):
        if i == 3:
            # time_idx번째 컬럼에 변형할 event_time 존재
            time_idx = int(line.rstrip().split(",")[1])
        if i >= 4:
            # geom_type, LATI, LONGI
            geom_info_list.append(line.rstrip().split(","))

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
            print("Now Making Data ... ({}/{})".format(line, full_line-1))
            data_list = origin_data.split(info.field_sep)
    
            # time_idx가 -1이면 GLOBAL테이블이므로 partition_date 없음
            if time_idx != -1:
                partition_date = data_list[time_idx-2].split(".")[0]  # 125GB짜리 할때
            else:
                partition_date = None
    
            # TODO: partition_key는 0으로, geo_level은 공백으로 초기화
            partition_key = "0"
            geom_level = ""
    
            # geometry 문법, geo_json 만들기
            geom_string_list = []
            geo_json = None
            for geom_info in geom_info_list:
                point_coord_list = []
                polygon_coord_list = [[]]
                geo_json_dict = {}
                if geom_info[0].upper() == "POINT":
                    if time_idx != -1:
                        latitude = int(geom_info[1]) - 2
                        longitude = int(geom_info[2]) - 2
                    else:
                        latitude = int(geom_info[1])
                        longitude = int(geom_info[2])
                    geom_string_list.append("POINT({} {})".format(data_list[latitude], data_list[longitude]))
    
                    # FIXME: geo_json, 한 테이블에 두 개 이상 공간컬럼 있을 경우, 현재 이부분을 계속 바꿔줘야함.
                    if geo_json is None:
                        point_coord_list.append(float(data_list[latitude]))
                        point_coord_list.append(float(data_list[longitude]))
                        geo_json_dict["type"] = geom_info[0].upper()
                        geo_json_dict["coordinates"] = point_coord_list
                        geo_json = json.dumps(geo_json_dict)
    
                elif geom_info[0].upper() == "POLYGON":
                    if time_idx != -1:
                        start_latitude = int(geom_info[1]) - 2
                        start_longitude = int(geom_info[2]) - 2
                        end_latitude = int(geom_info[3]) - 2
                        end_longitude = int(geom_info[4]) - 2
                    else:
                        start_latitude = int(geom_info[1])
                        start_longitude = int(geom_info[2])
                        end_latitude = int(geom_info[3])
                        end_longitude = int(geom_info[4])
                    geom_string_list.append("POLYGON(({0} {2}, {1} {2}, {1} {3}, {0} {3}, {0} {2}))" \
                            .format(data_list[start_latitude], data_list[end_latitude], data_list[start_longitude], data_list[end_longitude]))
    
                    # FIXME: geo_json, 한 테이블에 두 개 이상 공간컬럼 있을 경우, 현재 이부분을 계속 바꿔줘야함.
                    if geo_json is None:
                        polygon_coord_list[0].append([float(data_list[start_latitude]), float(data_list[start_longitude])])
                        polygon_coord_list[0].append([float(data_list[end_latitude]), float(data_list[start_longitude])])
                        polygon_coord_list[0].append([float(data_list[end_latitude]), float(data_list[end_longitude])])
                        polygon_coord_list[0].append([float(data_list[start_latitude]), float(data_list[end_longitude])])
                        polygon_coord_list[0].append([float(data_list[start_latitude]), float(data_list[start_longitude])])
                        geo_json_dict["type"] = geom_info[0].upper()
                        geo_json_dict["coordinates"] = polygon_coord_list
                        geo_json = json.dumps(geo_json_dict)
    
            # time_idx가 -1이면 GLOBAL테이블이므로 partition_key, partition_date 없음
            if time_idx != -1:
                if geom_string_list: 
                    parsed_data = partition_date + info.field_sep + partition_key + info.field_sep + origin_data.rstrip() \
                                    + info.field_sep + info.field_sep.join(geom_string_list) + info.field_sep + geom_level + info.field_sep \
                                    + geo_json + info.record_sep
                else:
                    parsed_data = partition_date + info.field_sep + partition_key + info.field_sep + origin_data.rstrip() + info.record_sep
            elif time_idx == -1:
                if geom_string_list:
                    parsed_data = origin_data.rstrip() + info.field_sep + info.field_sep.join(geom_string_list) + info.field_sep + geom_level \
                                    + info.field_sep + geo_json + info.record_sep 
                else:
                    parsed_data = origin_data.rstrip() + info.record_sep
    
            tmpwf.write(parsed_data)
            line += 1
    
        with open(tmp_path, "r") as tmprf:
            dat = tmprf.read().rstrip()
            print(c.LoadString(table_name, data_path[-6:-4], "20190116000000", ctl, dat))

os.remove(tmp_path)
print(time.time() - start)
