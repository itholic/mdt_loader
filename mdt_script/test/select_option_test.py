# -*- coding: utf-8 -*-
"""쿼리에서 GEOMFROMTEXT에 해당하는 부분만 뽑아내기 위한 기능 테스트"""

import re

query = "SELECT PARTITION_DATE, PARTITION_KEY, EVENT_TIME, IMSI, MCC, MNC, ENB_ID, CELL_ID, SYN_ACK_FIRST_TIME, ACK_TIME, LATITUDE, LONGITUDE, ARTT, ARTT_SCORE, GEOM, GEOM_LEVEL, GEOM_JSON FROM    A0.  PM_RTT_SCORE WHERE ST_CONTAINS(GEOMFROMTEXT('polygon((28.621964 77.245142, 28.621964 77.210483, 28.602121 77.210483, 28.602121 77.245142, 28.621964 77.245142))'), GEOM) ;"

p = re.compile("(GEOMFROMTEXT.+'\s*\)\s*),")

feature = p.findall(query)[0]

test_s = "mbrminx({feature})".format(feature=feature)

print(test_s)
