#!/bin/env python
# coding: utf-8

import sys

import API.M6 as M6
import connection_info as info

try:
    schema_path = sys.argv[1]
except:
    raise Exception("MISSING TABLE_SCHEMA")

conn = M6.Connection(info.host, info.user_id, info.user_passwd, Direct=info.direct, Database=info.database)
c = conn.Cursor()
c.SetFieldSep('|^|')
c.SetRecordSep('|^-^|')

q_create_global = """
    CREATE TABLE {} (
        {}
    )
    datascope       GLOBAL
    ramexpire       0
    diskexpire      0
    partitionkey    None
    partitiondate   None
    partitionrange  0
    {}
    ;
"""

q_create_local = """
    CREATE TABLE {} (
        {}
    )
    datascope       LOCAL
    ramexpire       30
    diskexpire      259200
    partitionkey    {}
    partitiondate   {}
    partitionrange  60
    {}
    ;
"""

q_create_geo_idx = "CREATE INDEX {0}_GEO_IDX ON {0} (GEOM RTREE);"

extension_option = "extension geospatial"

table_name = schema_path.split("/")[-1]

with open(schema_path, 'r') as f:
    col_name_list = [col_string.replace("\"", "") for col_string in f.readline().rstrip().split(",")]
    col_type_list = [type_string for type_string in f.readline().rstrip().split(",")]

    col_string = ",".join([col_name + " " + col_type for col_name, col_type in zip(col_name_list, col_type_list)])
    partitionkey = f.readline().rstrip()
    partitiondate = f.readline().rstrip().split(",")[0]

if partitiondate == "GLOBAL":
    if "GEOM" in col_name_list:
        q_create_table = q_create_global.format(table_name, col_string, extension_option)
        q_create_index = q_create_geo_idx.format(table_name)
        print(c.Execute2(q_create_table), "CREATE GLOBAL TABLE, {}".format(table_name))
        print(c.Execute2(q_create_index), "CREATE GEO INDEX, {}_GEO_IDX".format(table_name))
    else:
        q_create_table = q_create_global.format(table_name, col_string, "")
        print(c.Execute2(q_create_table), "CREATE GLOBAL TABLE, {}".format(table_name))
else:
    if "GEOM" in col_name_list:
        q_create_table = q_create_local.format(table_name, col_string, partitionkey, partitiondate, extension_option)
        q_create_index = q_create_geo_idx.format(table_name)
        print(c.Execute2(q_create_table), "CREATE LOCAL TABLE, {}".format(table_name))
        print(c.Execute2(q_create_index), "CREATE GEO INDEX, {}_GEO_IDX".format(table_name))
    else:
        q_create_table = q_create_local.format(table_name, col_string, partitionkey, partitiondate, "")
        print(c.Execute2(q_create_table), "CREATE LOCAL TABLE, {}".format(table_name))

c.Close()
conn.close()
