#!/bin/env python
# coding: utf-8

import glob
import threading

import API.M6 as M6
import connection_info as info

schema_path = "table_schema/JP_MESH_TEST"
table_name = "JP_MESH_TEST"
mesh_level = 3
path_list = glob.glob("mesh_data/mesh_lv3/*")
path_list.sort()
sema = threading.Semaphore(30)

def loader(path, table_name, key, ctl):
    sema.acquire()

    print("start {}".format(path))
    with open(path, "r") as f:
        partition_key = "K3_{}".format(key)
        partition_date = "20190117000000"
        dat = f.read().rstrip()
        conn = M6.Connection(info.host, info.user_id, info.user_passwd, Direct=info.direct, Database=info.database)
        c = conn.Cursor()
        c.SetFieldSep(info.field_sep)
        c.SetRecordSep(info.record_sep)
        print(c.LoadString(table_name, partition_key, partition_date, ctl, dat))

    print("end {}".format(partition_key))

    sema.release()

def load_all():
    with open(schema_path, 'r') as f:
        ctl = f.readline()\
                .rstrip()\
                .replace("\"", "")\
                .replace("GEOM","+GEOM")\
                .replace("+GEOM_LEVEL","GEOM_LEVEL")\
                .replace("+GEOM_JSON","GEOM_JSON")\
                .replace(",", "\n")

    thread_list = [threading.Thread(target=loader, args=(path, table_name, key+1, ctl)) for key, path in enumerate(path_list)]

    for thread in thread_list:
        thread.start()

    for thread in thread_list:
        thread.join()


if __name__ == "__main__":
    load_all()
