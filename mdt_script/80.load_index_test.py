#!/bin/env python
# coding: utf-8

import sys
import time

import API.M6 as M6
import connection_info as info


def load(dat_path, table_name, ctl, dat):
    partition_date = dat_path.split("/")[-1].split(".")[0].replace("_","") + "0000"
    conn = M6.Connection(info.host, info.user_id, info.user_passwd, Direct=info.direct, Database=info.database)
    c = conn.Cursor()
    c.SetFieldSep(info.field_sep)
    c.SetRecordSep(info.record_sep)
    start = time.time()
    print(c.LoadString(table_name, "0", partition_date, ctl, dat))
    print(time.time() - start)

if __name__ == "__main__":
    try:
        dat_path = sys.argv[1]
        table_name = sys.argv[2].upper()
        schema_path = "table_schema/{}".format(table_name)
        with open(schema_path) as f:
            ctl = f.readline().rstrip().replace("\"", "").replace(",","\n")
        with open(dat_path) as f:
            dat = f.read().rstrip()

    except Exception as e:
        raise e

    load(dat_path, table_name, ctl, dat)
