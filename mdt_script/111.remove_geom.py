import glob

csv_list = glob.glob("../tmp/*")
print(csv_list)

for i, csv in enumerate(csv_list):
    print("({}/{})".format(i+1, len(csv_list)))
    with open(csv) as f:
        with open("nogeom_dat/{}".format(csv.split("/")[-1]), "w") as nf:
            for line in f:
                data = "|^|".join(line.rstrip().split("|^|")[:23])
                nf.write(data+"\n")
