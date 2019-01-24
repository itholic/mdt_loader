#!/bin/env python
# coding: utf-8

import glob
import sys
import datetime
import os

import connection_info as info

try:
    data_path = sys.argv[1]
    full_line = int(os.popen('cat {} | wc -l'.format(data_path)).read().rstrip()) - 1
    mesh_level = int(list(data_path)[-5])
    X = 1 if mesh_level == 1 \
            else 2 if mesh_level == 2 \
            else 200
except:
    raise Exception("MISSING CSV_PATH")

schema_path = "table_schema/JP_MESH_TEST"
parsed_data_path = "mesh_data/{}".format(data_path.split("/")[-1].replace(".csv", ""))

try:
    os.remove(parsed_data_path)
except:
    pass

# 스키마 파일에는 컬럼 목록, 컬럼타입 목록, partition_key, partition_date 관련정보, geom 관련정보가 각각 한줄에 적혀있다.
geom_info_list = []
with open(schema_path, 'r') as f:
    for i, line in enumerate(f):
        if i == 3:
            # time_idx번째 컬럼에 변형할 event_time 존재
            time_idx = int(line.rstrip().split(",")[1])
        if i >= 4:
            # geom_type, LATI, LONGI
            geom_info_list.append(line.rstrip().split(","))

############################################################################################
""" 스키마 파일에서 뽑아온 정보를 기반으로 실제 삽입할 데이터 만들기
"""
import time
import codecs
import json

start = time.time()
with codecs.open(data_path, 'r', encoding='utf-8-sig') as f:
    with open(parsed_data_path, 'a') as pf:
        f.readline()  # csv의 맨 첫째줄 버리기
        line = 1  # 라인수 초기화
        key = 1
        full_line_div_x = full_line // X
        for origin_data in f:
            origin_data = origin_data.replace("\"", "").replace(",", info.field_sep).rstrip()
            print("({}/{})".format(line, full_line))
            data_list = origin_data.split(info.field_sep)

            # time_idx가 -1이면 GLOBAL테이블이므로 partition_date 없음
            if time_idx != -1:
                partition_date = "20190117000000"  # partition date는 고정
            else:
                partition_date = None

            if line % full_line_div_x == 0 and line != full_line:
                key += 1

            partition_key = "K{}_{}".format(mesh_level, key)
            geom_level = str(mesh_level)

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


############################################################################################
            """ 각 컬럼에 들어갈 데이터 생성 완료후, 최종 삽입 데이터 한 줄로 나열해 String으로 만들기
            """

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

            pf.write(parsed_data)
            line += 1

print(time.time() - start)
