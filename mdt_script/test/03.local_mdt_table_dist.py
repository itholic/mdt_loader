# -*- coding: utf-8 -*-

"""대용량 csv 데이터를 분산처리하기 위한 프로그램"""

import os
import glob

data = "data/SAMPLE_DATA"

number_of_key = 10
load_per_once = 100

os.system("split -l {param} {src} {src}_".format(param=load_per_once, src=data))
os.system("sed -i 1d {src}_aa".format(src=data))

file_list = (glob.glob(data + "_*"))

