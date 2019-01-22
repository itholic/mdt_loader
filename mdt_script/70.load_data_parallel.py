#!/bin/env python
# coding: utf-8

import glob
import threading
import multiprocessing

import API.M6 as M6
import connection_info as info

path_list = glob.glob("nogeom_dat/*")
sema = threading.Semaphore(50)

# 테이블 정보가 있는 경로와 파싱된 데이터가 저장될 경로 지정
schema_path = "table_schema/JP_MESH_TEST"
table_name = "JP_MESH_TEST"

def loader(path, table_name, partition_key, ctl):
    sema.acquire()

    print("start {}".format(path))
    with open(path, "r") as f:
        # partition_date = path.split("/")[-1].split(".")[0].replace("_","") + "0000"
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
        ctl = f.readline().rstrip().replace("\"", "").replace(",","\n")

    thread_list = [threading.Thread(target=loader, args=(path, table_name, "0", ctl)) for path in path_list]

    for thread in thread_list:
        thread.start()

    for thread in thread_list:
        thread.join()    


if __name__ == "__main__":
    load_all()
