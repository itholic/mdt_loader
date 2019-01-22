import random
from jpmesh import Angle, Coordinate, FirstMesh, parse_mesh_code



mesh_lv1_list = [str(i).zfill(4) for i in range(10000)]

mesh_lv2_list = [mesh_lv1 + str(i).zfill(2) \
                    for mesh_lv1 in mesh_lv1_list
                    for i in range(78)
                        if str(i).find("8") == -1
                        and str(i).find("9") == -1]

mesh_lv3_list = [mesh_lv2 + str(i).zfill(2) \
                    for mesh_lv2 in mesh_lv2_list \
                    for i in range(100)]

def make_min_max_lat_lon(mesh):
    start_lat = mesh.south_west.lat.degree
    start_lon = mesh.south_west.lon.degree 
    end_lat = mesh.south_west.lat.degree + mesh.size.lat.degree
    end_lon = mesh.south_west.lon.degree + mesh.size.lon.degree

    return(start_lat, start_lon, end_lat, end_lon)

with open("mesh_csv/mesh_lv3.csv","w") as f:
    f.write(""""POPULATION","CODE","START_LAT","START_LON","END_LAT","END_LON"\n""")
    for i, mesh_code in enumerate(mesh_lv3_list):
        print("{}/{}".format(i, len(mesh_lv3_list)))
        population = random.randrange(1000000)
        code = mesh_code
    
        mesh = parse_mesh_code(mesh_code)
        start_lat, start_lon, end_lat, end_lon = make_min_max_lat_lon(mesh)
    
        f.write(""""{population}","{code}","{start_lat}","{start_lon}","{end_lat}","{end_lon}"\n""" \
                    .format(population=population, code=code, start_lat=start_lat, start_lon=start_lon, end_lat=end_lat, end_lon=end_lon))
