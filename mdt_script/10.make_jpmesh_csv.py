# -*- coding: utf-8 -*-

from jpmesh import Angle, Coordinate, FirstMesh, SecondMesh, parse_mesh_code

coordinate = Coordinate(
    lon=Angle.from_degree(140.0), 
    lat=Angle.from_degree(35.0)
)

# mesh_code = "5240"

# mesh = FirstMesh.from_coordinate(coordinate)
# print("FirstMesh code: {}".format(mesh.code))
# print("FirstMesh lon: {}".format(mesh.south_west.lon.degree))
# print("FirstMesh lat: {}".format(mesh.south_west.lat.degree))
# print(dir(mesh))

# mesh = SecondMesh.from_coordinate(coordinate)
# print("SecondMesh code: {}".format(mesh.code))
# print("SecondMesh lon: {}".format(mesh.south_west.lon.degree))
# print("SecondMesh lat: {}".format(mesh.south_west.lat.degree))
# print("SecondMesh lat: {}".format(mesh.south_west.lat.degree))
# print("SecondMesh size: {}".format(mesh.size.lon.degree))
# print("SecondMesh size: {}".format(mesh.size.lat.degree))
# print("")
# print("SecondMesh size: {}".format(mesh.south_west.lon.degree + mesh.size.lon.degree))
# print("SecondMesh size: {}".format(mesh.south_west.lat.degree + mesh.size.lat.degree))
# print("SecondMesh Parantmesh: {}".format(dir(mesh.ParentMesh)))
# print("SecondMesh Parantmesh lon: {}".format(mesh.ParentMesh.south_west))
# print("SecondMesh Parantmesh lat: {}".format(mesh.ParentMesh.south_west.lat.degreee))
# print(dir(mesh))
# print(mesh.code)

# mesh = parse_mesh_code(mesh_code)

# print(mesh.south_west.lon.degree)
# print(mesh.south_west.lat.degree)

#print("code: {}".format(parse_mesh_code(mesh_code).code))
#print("code_parse_regex: {}".format(parse_mesh_code(mesh_code).code_parse_regex))
#print("code_pattern: {}".format(parse_mesh_code(mesh_code).code_pattern))
#print("code_regex: {}".format(parse_mesh_code(mesh_code).code_regex))
#print("from_code: {}".format(parse_mesh_code(mesh_code).from_code))
#print("from_coordinate: {}".format(parse_mesh_code(mesh_code).from_coordinate))
#print("size: {}".format(parse_mesh_code(mesh_code).size))
#print("south_west: {}".format(parse_mesh_code(mesh_code).south_west))

#print(type(parse_mesh_code(mesh_code).code))
#print(type(parse_mesh_code(mesh_code).code_parse_regex))
#print(type(parse_mesh_code(mesh_code).code_pattern))
#print(type(parse_mesh_code(mesh_code).code_regex))
#print(type(parse_mesh_code(mesh_code).from_code))
#print(type(parse_mesh_code(mesh_code).from_coordinate))
#print(type(parse_mesh_code(mesh_code).size))
#print(type(parse_mesh_code(mesh_code).south_west))

data = """"PARTITION_DATE","PARTITION_KEY","POPULATION","CODE","GEOM","GEOM_LEVEL","GEOM_JSON"\n"""

start_1_mesh = "0000"
start_2_mesh = "000000"
start_3_mesh = "00000000"


