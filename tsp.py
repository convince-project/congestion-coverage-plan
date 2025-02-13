from OccupancyMap import OccupancyMap
import utils
import matplotlib.pyplot as plt
from python_tsp.exact import solve_tsp_dynamic_programming






def create_matrix_from_occupancy_map(occupancy_map, time):
    matrix = []
    occupancies = occupancy_map.get_current_occupancies(time)
    for i in occupancy_map.get_vertices_list():
        row = []
        for j in occupancy_map.get_vertices_list():
            if i == j:
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
    return matrix



