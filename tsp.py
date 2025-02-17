from OccupancyMap import OccupancyMap
import utils
import matplotlib.pyplot as plt
from python_tsp.exact import solve_tsp_dynamic_programming
import numpy as np





def create_matrix_from_occupancy_map_current_occupancy_bak(occupancy_map, time, initial_vertex_id):
    matrix = []
    occupancies = occupancy_map.get_current_occupancies(time)
    initial_vertex = occupancy_map.find_vertex_from_id(initial_vertex_id)
    vertices_list = occupancy_map.get_vertices_list()
    for i in range(0, len(vertices_list) + 2):
        row = []
        for j in range(0, len(vertices_list) + 2):
            if i == 0:
                #first row
                if j == initial_vertex or j == len(vertices_list) + 1:
                    row.append(0)
                else:
                    row.append(99999999)
            elif j == 0:
                if i == initial_vertex or i == len(vertices_list) + 1:
                    row.append(0)
                else:
                    row.append(99999999)
            elif i == len(vertices_list) + 1:
                row.append(0)
            elif j == len(vertices_list) + 1:
                row.append(0)
                
            elif i == j:
                row.append(0)
            else:

                edge = occupancy_map.find_edge_from_position(i.get_id(), j.get_id())
                if edge is None:
                    edge = occupancy_map.find_edge_from_position(j.get_id(), i.get_id())
                if edge is None:
                    row.append(99999999)
                else:
                    traverse_time =occupancy_map.get_edge_traverse_time(edge)
                    if edge in occupancies.keys():
                        if occupancies[edge] >= occupancy_map.find_edge_limit(edge):
                            row.append(traverse_time["high"])
                        else:
                            row.append(traverse_time["low"])
                    else:
                        row.append(traverse_time["low"])
        matrix.append(row)
    return np.array(matrix)






def create_matrix_from_occupancy_map_current_occupancy(occupancy_map, time, initial_vertex_id):
    matrix = []
    occupancies = occupancy_map.get_current_occupancies(time)

    vertices_list = occupancy_map.get_vertices_list()
    initial_vertex = occupancy_map.find_vertex_from_id(initial_vertex_id)
    for i in range(0, len(vertices_list)+1):
        row = []
        for j in range(0,len(vertices_list)+1):
            if i == j:
                row.append(0)
            if i == 0 or j == 0:
                row.append(0)
            else:
                edge = occupancy_map.find_edge_from_position(vertices_list[i-1].get_id(), vertices_list[j-1].get_id())
                if edge is None:
                    edge = occupancy_map.find_edge_from_position(vertices_list[j-1].get_id(), vertices_list[i-1].get_id())
                if edge is None:
                    row.append(99999999)
                else:
                    traverse_time =occupancy_map.get_edge_traverse_time(edge)
                    if edge in occupancies.keys():
                        if occupancies[edge] >= occupancy_map.find_edge_limit(edge):
                            row.append(traverse_time["high"])
                        else:
                            row.append(traverse_time["low"])
                    else:
                        row.append(traverse_time["low"])
        matrix.append(row)
    return np.array(matrix)





def create_matrix_from_occupancy_map(occupancy_map, level, initial_vertex_id):
    matrix = []

    vertices_list = occupancy_map.get_vertices_list()
    initial_vertex = occupancy_map.find_vertex_from_id(initial_vertex_id)
    for i in range(0, len(vertices_list)+1):
        row = []
        for j in range(0,len(vertices_list)+1):
            if i == j:
                row.append(0)
            if i == 0 or j == 0:
                row.append(0)
            else:
                edge = occupancy_map.find_edge_from_position(vertices_list[i-1].get_id(), vertices_list[j-1].get_id())
                if edge is None:
                    edge = occupancy_map.find_edge_from_position(vertices_list[j-1].get_id(), vertices_list[i-1].get_id())
                if edge is None:
                    row.append(99999999)
                else:

                    traverse_time =occupancy_map.get_edge_traverse_time(edge)
                    if level == "high":
                        row.append(traverse_time["high"])
                    elif level == "low":
                        row.append(traverse_time["low"])
                    elif level == "average":
                        row.append((traverse_time["high"] + traverse_time["low"])/2)

        matrix.append(row)
    return np.array(matrix)





def create_matrix_from_occupancy_map_length(occupancy_map, initial_vertex_id):
    matrix = []

    vertices_list = occupancy_map.get_vertices_list()
    initial_vertex = occupancy_map.find_vertex_from_id(initial_vertex_id)
    for i in range(0, len(vertices_list)+1):
        row = []
        for j in range(0,len(vertices_list)+1):
            if i == j:
                row.append(0)
            if i == 0 or j == 0:
                row.append(0)
            else:
                edge = occupancy_map.find_edge_from_position(vertices_list[i-1].get_id(), vertices_list[j-1].get_id())
                if edge is None:
                    edge = occupancy_map.find_edge_from_position(vertices_list[j-1].get_id(), vertices_list[i-1].get_id())
                if edge is None:
                    row.append(99999999)
                else:
                    row.append(occupancy_map.find_edge_from_id(edge).get_length())

        matrix.append(row)
    print(matrix)
    return np.array(matrix)


def create_matrix_from_occupancy_map_length_test(occupancy_map, initial_vertex_id):
    matrix = []

    vertices_list = occupancy_map.get_vertices_list()
    initial_vertex = occupancy_map.find_vertex_from_id(initial_vertex_id)
    for i in range(0, len(vertices_list)+1):
        row = []
        for j in range(0,len(vertices_list)+1):
            if i == j:
                row.append(0)
            if i == 0 or j == 0:
                row.append(0)
            else:
                edge = occupancy_map.find_edge_from_position(vertices_list[i-1].get_id(), vertices_list[j-1].get_id())
                if edge is None:
                    edge = occupancy_map.find_edge_from_position(vertices_list[j-1].get_id(), vertices_list[i-1].get_id())
                if edge is None:
                    row.append(99999999)
                else:
                    row.append(occupancy_map.find_edge_from_id(edge).get_length())

        matrix.append(row)

    print(matrix)
    return np.array(matrix)


def solve_tsp(matrix):
    return solve_tsp_dynamic_programming(matrix)



