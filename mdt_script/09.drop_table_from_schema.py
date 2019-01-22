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

table_name = schema_path.split("/")[-1]

q = "DROP TABLE {}".format(table_name)

print(c.Execute2(q), table_name)
    
c.Close()
conn.close()
