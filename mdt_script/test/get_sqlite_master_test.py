# -*- coding: utf-8 -*-

"""sqlite 데이터 파일에서 RTREE인덱스 테이블 이름을 뽑아오기 위한 쿼리"""

import sqlite3

con = sqlite3.connect('DAT_SAMPLE')
cursor = con.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")

for row in cursor:
    if row[0].endswith("_parent"):
        table_name = row[0].replace("_parent", "")

print(table_name)
