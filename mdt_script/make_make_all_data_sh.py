import glob

csv_list = glob.glob("../201901/*")

with open("100.make_all_data.sh", "w") as f:
    for csv in csv_list:
        f.write("python 50.make_data_from_csv_nogeom.py {}\n".format(csv))
