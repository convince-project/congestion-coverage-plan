from congestion_coverage_plan_museum.map_utils.OccupancyMap import OccupancyMap
import congestion_coverage_plan_museum.utils.dataset_utils as dataset_utils
import matplotlib.pyplot as plt
import csv
from congestion_coverage_plan_museum.cliff_predictor.CliffPredictor import CliffPredictor
from congestion_coverage_plan_museum.cliff_predictor.PredictorCreator import create_atc_cliff_predictor,  create_madama_cliff_predictor
import warnings

def create_madama_topological_map_doors_16(occupancy_map):
    occupancy_map.set_name('madama3_doors_16_experiments')
    occupancy_map.add_vertex_with_id("vertex1", -0.15, 0.39)  # start poi
    occupancy_map.add_vertex_with_id("vertex2", 6.42, -2.93, poi_number=1)
    occupancy_map.add_vertex_with_id("vertex3", 7.27, 1.47, poi_number=1)
    occupancy_map.add_vertex_with_id("vertex4", 17.05, 2.1, poi_number=2)
    occupancy_map.add_vertex_with_id("vertex5", 19.05, -3.0, poi_number=2)
    occupancy_map.add_vertex_with_id("vertex6", 15.68, -15.96, poi_number=3)
    occupancy_map.add_vertex_with_id("vertex7", 25.65, -15.88, poi_number=3)
    occupancy_map.add_vertex_with_id("vertex8", 20.15, -31.55, poi_number=4)
    occupancy_map.add_vertex_with_id("vertex9", 17.72, -33.59, poi_number=4)
    occupancy_map.add_vertex_with_id("vertex10", 1.16, -29.4, poi_number=5)
    occupancy_map.add_vertex_with_id("vertex11", 4.97, -28.47, poi_number=5)
    occupancy_map.add_vertex_with_id("vertex12", 13.94, -0.68) # door 1
    occupancy_map.add_vertex_with_id("vertex13", 16.09, -6.91) # door 2
    occupancy_map.add_vertex_with_id("vertex14", 15.65, -28.25) # door 3
    occupancy_map.add_vertex_with_id("vertex15", 12.09, -33.66) # door 4
    occupancy_map.add_vertex_with_id("vertex16", 0.97, -26.7, is_final_goal=True)  # final goal


    # start poi
    occupancy_map.add_edge_with_incremental_id("vertex1", "vertex2")
    occupancy_map.add_edge_with_incremental_id("vertex1", "vertex3")




    # first door
    occupancy_map.add_edge_with_incremental_id("vertex2", "vertex12")
    occupancy_map.add_edge_with_incremental_id("vertex3", "vertex12")

    occupancy_map.add_edge_with_incremental_id("vertex12", "vertex4")
    occupancy_map.add_edge_with_incremental_id("vertex12", "vertex5")

    # second door

    occupancy_map.add_edge_with_incremental_id("vertex4", "vertex13")
    occupancy_map.add_edge_with_incremental_id("vertex5", "vertex13")

    occupancy_map.add_edge_with_incremental_id("vertex13", "vertex6")
    occupancy_map.add_edge_with_incremental_id("vertex13", "vertex7")

    # third door

    occupancy_map.add_edge_with_incremental_id("vertex6", "vertex14")
    occupancy_map.add_edge_with_incremental_id("vertex7", "vertex14")

    occupancy_map.add_edge_with_incremental_id("vertex14", "vertex8")
    occupancy_map.add_edge_with_incremental_id("vertex14", "vertex9")

    # fourth door

    occupancy_map.add_edge_with_incremental_id("vertex8", "vertex15")
    occupancy_map.add_edge_with_incremental_id("vertex9", "vertex15")

    occupancy_map.add_edge_with_incremental_id("vertex15", "vertex10")
    occupancy_map.add_edge_with_incremental_id("vertex15", "vertex11")

    # final poi

    occupancy_map.add_edge_with_incremental_id("vertex10", "vertex16")
    occupancy_map.add_edge_with_incremental_id("vertex11", "vertex16")




def get_times_madama():
    # read the file times_higher_7_madama.csv and put into a list
    filename = 'times_higher_7_madama.csv'
    time_list = []
    with open(filename) as f:
        for line in f:
            time_list.append(float(line.strip()))
    return time_list


def create_occupancy_map(occupancy_map, level, topological_map_creator_function, num_iterations=3000):
    topological_map_creator_function(occupancy_map)
    edges = occupancy_map.get_edges()
    for edge_key in edges:
        occupancy_map.add_edge_limit(edges[edge_key].get_id(), level)
    occupancy_map.calculate_average_edge_traverse_times(num_iterations)
    folder = 'data/occupancy_maps_' + occupancy_map.get_name()
    dataset_utils.create_folder(folder)

    filename = folder + '/occupancy_map_' + occupancy_map.get_name() + "_" + str(len(level))+'_levels.yaml'
    occupancy_map.save_occupancy_map(filename)



# def create_occupancy_map_madama(occupancy_map, level, topological_map_creator_function, num_iterations=1000):
#     topological_map_creator_function(occupancy_map)
#     edges = occupancy_map.get_edges()
#     for edge_key in edges:
#         occupancy_map.add_edge_limit(edges[edge_key].get_id(), level)
#     occupancy_map.calculate_average_edge_traverse_times(num_iterations)
#     folder = 'data/occupancy_maps_' + occupancy_map.get_name()
#     utils.create_folder(folder)

#     filename = folder + '/occupancy_map_' + occupancy_map.get_name() + "_" + str(len(level))+'_levels.yaml'
#     occupancy_map.save_occupancy_map(filename)


if __name__ == "__main__":
    # print(matrix)
    warnings.filterwarnings("ignore")
    # predictor = create_atc_cliff_predictor()
    predictor_madama = create_madama_cliff_predictor()
    # topological_map_creator_function = [create_large_topological_map_atc_corridor, create_medium_large_topological_map_atc_corridor]
    # topological_map_creator_function = [create_large_topological_map_atc_corridor, create_medium_topological_map_atc_corridor, create_small_topological_map_atc_corridor,
    #                                      create_large_topological_map_atc_square, create_medium_topological_map_atc_square]
    # topological_map_creator_function_madama = [create_madama_topological_map_26, create_madama_topological_map_21, create_madama_topological_map_16, create_madama_topological_map_11]
    topological_map_creator_function_madama_doors = [create_madama_topological_map_doors_16]
    # two levels
    occupancy_levels = [(["zero", "one"], {"zero": [0,1], "one": [1,9999999]}),
                        (["zero", "one", "two"], {"zero": [0,1], "one": [1,3], "two": [3,9999999]}),
                        (["zero", "one", "two", "three"], {"zero": [0,1], "one": [1,3], "two": [3,6], "three": [6,9999999]}),
                        (["zero", "one", "two", "three", "four"], {"zero": [0,1], "one": [1,3], "two": [3,5], "three": [5,7], "four": [7,9999999]}),
                        (["zero", "one", "two", "three", "four", "five"], {"zero": [0,1], "one": [1,3], "two": [3,5], "three": [5,7], "four": [7,9], "five": [9,9999999]}),
                        (["zero", "one", "two", "three", "four", "five", "six"], {"zero": [0,1], "one": [1,3], "two": [3,5], "three": [5,7], "four": [7,9], "five": [9,12], "six": [12,9999999]}),
                        (["zero", "one", "two", "three", "four", "five", "six", "seven"], {"zero": [0,1], "one": [1,2], "two": [2,3], "three": [3,4], "four": [4,5], "five": [5,6], "six": [6,7], "seven": [7,9999999]})
                        ]



    for function_name in topological_map_creator_function_madama_doors:
        for levels in occupancy_levels:
            occupancy_map = OccupancyMap(predictor_madama, levels[0])
            create_occupancy_map(occupancy_map, levels[1], function_name, 3000)
            # occupancy_map.plot_topological_map(predictor_madama.map_file, predictor_madama.fig_size, occupancy_map.get_name(), show_vertex_names=True)
            # occupancy_map.display_topological_map()

    # for levels in  occupancy_levels:  # just two levels
    #     for vertex_number in [26]:
    #         occupancy_map = OccupancyMap(predictor, levels[0])
    #         function_name_map = globals()[f'create_topological_map_atc_corridor_{vertex_number}']
    #         create_occupancy_map_atc(occupancy_map, levels[1], function_name_map)
            # occupancy_map.plot_topological_map(predictor.map_file, predictor.fig_size, occupancy_map.get_name())
