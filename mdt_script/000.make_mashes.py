import time

start = time.time()

mesh_lv1_list = [str(i).zfill(4) for i in range(10000)]

print("count mesh 1: {}".format(len(mesh_lv1_list)))
print("first mesh 1: {}".format(mesh_lv1_list[0]))
print("last mesh 1: {}".format(mesh_lv1_list[-1]))
print("")

#mesh_lv2_list = []
#for mesh_lv1 in mesh_lv1_list:
#    for i in range(78):
#        if str(i).find("8") == -1 and str(i).find("9") == -1:
#            mesh_lv2_list.append(mesh_lv1 + str(i).zfill(2))
mesh_lv2_list = [mesh_lv1 + str(i).zfill(2) \
                    for mesh_lv1 in mesh_lv1_list
                    for i in range(78) 
                        if str(i).find("8") == -1 
                        and str(i).find("9") == -1]

print("count mesh 2: {}".format(len(mesh_lv2_list)))
print("first mesh 2: {}".format(mesh_lv2_list[0]))
print("last mesh 2: {}".format(mesh_lv2_list[-1]))
print("")


mesh_lv3_list = [mesh_lv2 + str(i).zfill(2) \
                    for mesh_lv2 in mesh_lv2_list \
                    for i in range(100)]

print("count mesh 3: {}".format(len(mesh_lv3_list)))
print("first mesh 3: {}".format(mesh_lv3_list[0]))
print("last mesh 3: {}".format(mesh_lv3_list[-1]))
print("")

print(time.time() - start)
