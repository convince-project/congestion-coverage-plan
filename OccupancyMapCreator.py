from OccupancyMap import OccupancyMap
import utils
import matplotlib.pyplot as plt
from tsp import create_matrix_from_occupancy_map, create_matrix_from_occupancy_map_current_occupancy, solve_tsp
import csv
from cliff_predictor import CliffPredictor
from PredictorCreator import create_atc_cliff_predictor, create_iit_cliff_predictor
import warnings

def create_medium_topological_map_atc_corridor(occupancy_map):
    occupancy_map.set_name('medium_atc_corridor')
    occupancy_map.add_vertex_with_id("vertex1", 43.89, -22.09)
    occupancy_map.add_vertex_with_id("vertex2", 40.03, -18.72)
    occupancy_map.add_vertex_with_id("vertex3", 34.15, -17.47)
    occupancy_map.add_vertex_with_id("vertex4", 19.79, -13.51)
    occupancy_map.add_vertex_with_id("vertex5", 27.7, -17.37)
    occupancy_map.add_vertex_with_id("vertex6", 35.52, -20.16)
    
    occupancy_map.add_edge_with_id("edge1", "vertex1", "vertex2")
    occupancy_map.add_edge_with_id("edge2", "vertex1", "vertex6")
    occupancy_map.add_edge_with_id("edge3", "vertex2", "vertex3")
    occupancy_map.add_edge_with_id("edge4", "vertex2", "vertex6")
    occupancy_map.add_edge_with_id("edge5", "vertex3", "vertex4")
    occupancy_map.add_edge_with_id("edge6", "vertex3", "vertex5")
    occupancy_map.add_edge_with_id("edge7", "vertex3", "vertex6")
    occupancy_map.add_edge_with_id("edge8", "vertex4", "vertex5")
    occupancy_map.add_edge_with_id("edge9", "vertex5", "vertex6")

    # add also the opposite edges
    occupancy_map.add_edge_with_id("edge10", "vertex2", "vertex1")
    occupancy_map.add_edge_with_id("edge11", "vertex6", "vertex1")
    occupancy_map.add_edge_with_id("edge12", "vertex3", "vertex2")
    occupancy_map.add_edge_with_id("edge13", "vertex6", "vertex2")
    occupancy_map.add_edge_with_id("edge14", "vertex4", "vertex3")
    occupancy_map.add_edge_with_id("edge15", "vertex5", "vertex3")
    occupancy_map.add_edge_with_id("edge16", "vertex6", "vertex3")
    occupancy_map.add_edge_with_id("edge17", "vertex5", "vertex4")
    occupancy_map.add_edge_with_id("edge18", "vertex6", "vertex5")

def create_large_topological_map_atc_corridor(occupancy_map):
    occupancy_map.set_name('large_atc_corridor')
    occupancy_map.add_vertex_with_id("vertex1", 42.88, -24.13)
    occupancy_map.add_vertex_with_id("vertex2", 40.03, -18.72)
    occupancy_map.add_vertex_with_id("vertex3", 34.15, -17.47)
    occupancy_map.add_vertex_with_id("vertex4", 21.91, -16.2)
    occupancy_map.add_vertex_with_id("vertex5", 27.88, -18.22)
    occupancy_map.add_vertex_with_id("vertex6", 35.64, -21.17)
    occupancy_map.add_vertex_with_id("vertex7", 27.0, -15.14)
    occupancy_map.add_vertex_with_id("vertex8", 19.79, -13.51)
    occupancy_map.add_vertex_with_id("vertex9", 38.29, -20.0)
    occupancy_map.add_vertex_with_id("vertex10", 31.7, -18.0)
    occupancy_map.add_vertex_with_id("vertex11", 24.71, -16.0)
    # fig, ax = plt.subplot(111, facecolor='grey')

    # ax.set_xlim(fig_size[0], fig_size[1])
    # ax.set_ylim(fig_size[2], fig_size[3])
    # occupancy_map.plot_topological_map()
    # plt.show()
    occupancy_map.add_edge_with_incremental_id("vertex1", "vertex2")
    occupancy_map.add_edge_with_incremental_id("vertex1", "vertex6")
    occupancy_map.add_edge_with_incremental_id("vertex1", "vertex9")
    occupancy_map.add_edge_with_incremental_id("vertex2", "vertex3")
    occupancy_map.add_edge_with_incremental_id("vertex2", "vertex9")

    occupancy_map.add_edge_with_incremental_id("vertex3", "vertex6")
    occupancy_map.add_edge_with_incremental_id("vertex3", "vertex7")
    occupancy_map.add_edge_with_incremental_id("vertex3", "vertex9")
    occupancy_map.add_edge_with_incremental_id("vertex3", "vertex10")

    occupancy_map.add_edge_with_incremental_id("vertex4", "vertex5")
    occupancy_map.add_edge_with_incremental_id("vertex4", "vertex8")
    occupancy_map.add_edge_with_incremental_id("vertex4", "vertex11")

    occupancy_map.add_edge_with_incremental_id("vertex5", "vertex6")
    occupancy_map.add_edge_with_incremental_id("vertex5", "vertex7")
    occupancy_map.add_edge_with_incremental_id("vertex5", "vertex10")
    occupancy_map.add_edge_with_incremental_id("vertex5", "vertex11")

    occupancy_map.add_edge_with_incremental_id("vertex6", "vertex9")
    occupancy_map.add_edge_with_incremental_id("vertex6", "vertex10")

    occupancy_map.add_edge_with_incremental_id("vertex7", "vertex8")
    occupancy_map.add_edge_with_incremental_id("vertex7", "vertex10")
    occupancy_map.add_edge_with_incremental_id("vertex7", "vertex11")

    occupancy_map.add_edge_with_incremental_id("vertex8", "vertex11")

    # add also the opposite edges
    occupancy_map.add_edge_with_incremental_id("vertex2", "vertex1")
    occupancy_map.add_edge_with_incremental_id("vertex6", "vertex1")
    occupancy_map.add_edge_with_incremental_id("vertex9", "vertex1")
    occupancy_map.add_edge_with_incremental_id("vertex3", "vertex2")
    occupancy_map.add_edge_with_incremental_id("vertex9", "vertex2")
    occupancy_map.add_edge_with_incremental_id("vertex6", "vertex3")
    occupancy_map.add_edge_with_incremental_id("vertex7", "vertex3")
    occupancy_map.add_edge_with_incremental_id("vertex9", "vertex3")
    occupancy_map.add_edge_with_incremental_id("vertex10", "vertex3")
    occupancy_map.add_edge_with_incremental_id("vertex5", "vertex4")
    occupancy_map.add_edge_with_incremental_id("vertex8", "vertex4")
    occupancy_map.add_edge_with_incremental_id("vertex11", "vertex4")
    occupancy_map.add_edge_with_incremental_id("vertex6", "vertex5")
    occupancy_map.add_edge_with_incremental_id("vertex7", "vertex5")
    occupancy_map.add_edge_with_incremental_id("vertex10", "vertex5")
    occupancy_map.add_edge_with_incremental_id("vertex11", "vertex5")
    occupancy_map.add_edge_with_incremental_id("vertex9", "vertex6")
    occupancy_map.add_edge_with_incremental_id("vertex10", "vertex6")
    occupancy_map.add_edge_with_incremental_id("vertex8", "vertex7")
    occupancy_map.add_edge_with_incremental_id("vertex10", "vertex7")
    occupancy_map.add_edge_with_incremental_id("vertex11", "vertex7")
    occupancy_map.add_edge_with_incremental_id("vertex11", "vertex8")

def create_small_topological_map_atc_corridor(occupancy_map):
    occupancy_map.set_name('small_atc_corridor')
    occupancy_map.add_vertex_with_id("vertex1", 43.89, -22.09)
    occupancy_map.add_vertex_with_id("vertex2", 40.03, -18.72)
    occupancy_map.add_vertex_with_id("vertex3", 34.15, -17.47)
    occupancy_map.add_vertex_with_id("vertex4", 35.52, -20.16)
    
    occupancy_map.add_edge_with_id("edge1", "vertex1", "vertex2")
    occupancy_map.add_edge_with_id("edge2", "vertex1", "vertex3")
    occupancy_map.add_edge_with_id("edge3", "vertex1", "vertex4")
    occupancy_map.add_edge_with_id("edge4", "vertex2", "vertex3")
    occupancy_map.add_edge_with_id("edge5", "vertex2", "vertex4")
    occupancy_map.add_edge_with_id("edge6", "vertex3", "vertex4")

    # add also the opposite edges
    occupancy_map.add_edge_with_id("edge7", "vertex2", "vertex1")
    occupancy_map.add_edge_with_id("edge8", "vertex3", "vertex1")
    occupancy_map.add_edge_with_id("edge9", "vertex4", "vertex1")
    occupancy_map.add_edge_with_id("edge10", "vertex3", "vertex2")
    occupancy_map.add_edge_with_id("edge11", "vertex4", "vertex2")
    occupancy_map.add_edge_with_id("edge12", "vertex4", "vertex3")

def create_medium_topological_map_atc_square(occupancy_map):
    occupancy_map.set_name('medium_atc_square')
    occupancy_map.add_vertex_with_id("vertex1", -4.5, -2.2)
    occupancy_map.add_vertex_with_id("vertex2", -6.3, -4.8)
    occupancy_map.add_vertex_with_id("vertex3", -11.1, 2.5)
    occupancy_map.add_vertex_with_id("vertex4", -16.5, 0)
    occupancy_map.add_vertex_with_id("vertex5", -11.1, 0)
    occupancy_map.add_vertex_with_id("vertex6", -6.3, 2.5)
    

    occupancy_map.add_edge_with_id("edge1", "vertex1", "vertex2")
    occupancy_map.add_edge_with_id("edge2", "vertex1", "vertex3")
    occupancy_map.add_edge_with_id("edge3", "vertex1", "vertex5")
    occupancy_map.add_edge_with_id("edge4", "vertex1", "vertex6")
    occupancy_map.add_edge_with_id("edge5", "vertex2", "vertex4")
    occupancy_map.add_edge_with_id("edge6", "vertex2", "vertex5")
    occupancy_map.add_edge_with_id("edge7", "vertex2", "vertex6")
    occupancy_map.add_edge_with_id("edge8", "vertex3", "vertex4")
    occupancy_map.add_edge_with_id("edge9", "vertex3", "vertex5")
    occupancy_map.add_edge_with_id("edge10", "vertex3", "vertex6")
    occupancy_map.add_edge_with_id("edge11", "vertex4", "vertex5")
    occupancy_map.add_edge_with_id("edge12", "vertex5", "vertex6")


    occupancy_map.add_edge_with_id("edge13", "vertex2", "vertex1")
    occupancy_map.add_edge_with_id("edge14", "vertex3", "vertex1")
    occupancy_map.add_edge_with_id("edge15", "vertex5", "vertex1")
    occupancy_map.add_edge_with_id("edge16", "vertex6", "vertex1")
    occupancy_map.add_edge_with_id("edge17", "vertex4", "vertex2")
    occupancy_map.add_edge_with_id("edge18", "vertex5", "vertex2")
    occupancy_map.add_edge_with_id("edge19", "vertex6", "vertex2")
    occupancy_map.add_edge_with_id("edge20", "vertex4", "vertex3")
    occupancy_map.add_edge_with_id("edge21", "vertex5", "vertex3")
    occupancy_map.add_edge_with_id("edge22", "vertex6", "vertex3")
    occupancy_map.add_edge_with_id("edge23", "vertex5", "vertex4")
    occupancy_map.add_edge_with_id("edge24", "vertex6", "vertex5")

def create_large_topological_map_atc_square(occupancy_map):
    occupancy_map.set_name('large_atc_square')
    occupancy_map.add_vertex_with_id("vertex1", -4.5, -2.2)
    occupancy_map.add_vertex_with_id("vertex2", -6.3, -4.8)
    occupancy_map.add_vertex_with_id("vertex3", -11.1, 2.5)
    occupancy_map.add_vertex_with_id("vertex4", -16.5, 0)
    occupancy_map.add_vertex_with_id("vertex5", -11.1, 0)
    occupancy_map.add_vertex_with_id("vertex6", -6.3, 2.5)
    occupancy_map.add_vertex_with_id("vertex7", -11.87, -4.97)
    occupancy_map.add_vertex_with_id("vertex8", -4.95, 5.48)
    occupancy_map.add_vertex_with_id("vertex9", 0, 2)
    occupancy_map.add_vertex_with_id("vertex10", -2.4, -3.31)
    occupancy_map.add_vertex_with_id("vertex11", -7.91, -1.63)
    occupancy_map.add_vertex_with_id("vertex12", -3.78, 0.63)

    occupancy_map.add_edge_with_incremental_id("vertex1", "vertex2")
    occupancy_map.add_edge_with_incremental_id( "vertex1", "vertex9")
    occupancy_map.add_edge_with_incremental_id("vertex1", "vertex10")
    occupancy_map.add_edge_with_incremental_id("vertex1", "vertex11")
    occupancy_map.add_edge_with_incremental_id("vertex1", "vertex12")
    occupancy_map.add_edge_with_incremental_id("vertex2", "vertex4")
    occupancy_map.add_edge_with_incremental_id("vertex2", "vertex5")
    occupancy_map.add_edge_with_incremental_id("vertex2", "vertex7")
    occupancy_map.add_edge_with_incremental_id("vertex2", "vertex10")
    occupancy_map.add_edge_with_incremental_id("vertex2", "vertex11")
    occupancy_map.add_edge_with_incremental_id("vertex3", "vertex4")
    occupancy_map.add_edge_with_incremental_id("vertex3", "vertex5")
    occupancy_map.add_edge_with_incremental_id("vertex3", "vertex6")
    occupancy_map.add_edge_with_incremental_id("vertex3", "vertex8")
    occupancy_map.add_edge_with_incremental_id("vertex4", "vertex5")
    occupancy_map.add_edge_with_incremental_id("vertex4", "vertex7")
    occupancy_map.add_edge_with_incremental_id("vertex5", "vertex6")
    occupancy_map.add_edge_with_incremental_id("vertex5", "vertex7")
    occupancy_map.add_edge_with_incremental_id("vertex5", "vertex11")
    occupancy_map.add_edge_with_incremental_id("vertex6", "vertex8")
    occupancy_map.add_edge_with_incremental_id("vertex6", "vertex9")
    occupancy_map.add_edge_with_incremental_id("vertex6", "vertex12")
    occupancy_map.add_edge_with_incremental_id("vertex8", "vertex9")
    occupancy_map.add_edge_with_incremental_id("vertex8", "vertex12")
    occupancy_map.add_edge_with_incremental_id("vertex9", "vertex10")
    occupancy_map.add_edge_with_incremental_id("vertex9", "vertex12")
    occupancy_map.add_edge_with_incremental_id("vertex10", "vertex12")

    # add also the opposite edges

    occupancy_map.add_edge_with_incremental_id("vertex2", "vertex1")
    occupancy_map.add_edge_with_incremental_id("vertex9", "vertex1")
    occupancy_map.add_edge_with_incremental_id("vertex10", "vertex1")
    occupancy_map.add_edge_with_incremental_id("vertex11", "vertex1")
    occupancy_map.add_edge_with_incremental_id("vertex12", "vertex1")
    occupancy_map.add_edge_with_incremental_id("vertex4", "vertex2")
    occupancy_map.add_edge_with_incremental_id("vertex5", "vertex2")
    occupancy_map.add_edge_with_incremental_id("vertex7", "vertex2")
    occupancy_map.add_edge_with_incremental_id("vertex10", "vertex2")
    occupancy_map.add_edge_with_incremental_id("vertex11", "vertex2")
    occupancy_map.add_edge_with_incremental_id("vertex4", "vertex3")
    occupancy_map.add_edge_with_incremental_id("vertex5", "vertex3")
    occupancy_map.add_edge_with_incremental_id("vertex6", "vertex3")
    occupancy_map.add_edge_with_incremental_id("vertex8", "vertex3")
    occupancy_map.add_edge_with_incremental_id("vertex5", "vertex4")
    occupancy_map.add_edge_with_incremental_id("vertex7", "vertex4")
    occupancy_map.add_edge_with_incremental_id("vertex6", "vertex5")
    occupancy_map.add_edge_with_incremental_id("vertex7", "vertex5")
    occupancy_map.add_edge_with_incremental_id("vertex11", "vertex5")
    occupancy_map.add_edge_with_incremental_id("vertex8", "vertex6")
    occupancy_map.add_edge_with_incremental_id("vertex9", "vertex6")
    occupancy_map.add_edge_with_incremental_id("vertex12", "vertex6")
    occupancy_map.add_edge_with_incremental_id("vertex9", "vertex8")
    occupancy_map.add_edge_with_incremental_id("vertex12", "vertex8")
    occupancy_map.add_edge_with_incremental_id("vertex10", "vertex9")
    occupancy_map.add_edge_with_incremental_id("vertex12", "vertex9")
    occupancy_map.add_edge_with_incremental_id("vertex12", "vertex10")

def create_medium_topological_map_iit(occupancy_map):
    occupancy_map.set_name('medium_iit')
    
    # add the vertices
    assert occupancy_map.add_vertex_with_id("vertex1", 0, -12)
    assert occupancy_map.add_vertex_with_id("vertex2", 1, -2)
    assert occupancy_map.add_vertex_with_id("vertex3", 3, -6)
    assert occupancy_map.add_vertex_with_id("vertex4", 8, -10)
    assert occupancy_map.add_vertex_with_id("vertex5", 6, -3)

    # add the edges
    assert occupancy_map.add_edge_with_id("edge1", "vertex1", "vertex2")
    assert occupancy_map.add_edge_with_id("edge9", "vertex2", "vertex1")
    assert occupancy_map.add_edge_with_id("edge2", "vertex1", "vertex3")
    assert occupancy_map.add_edge_with_id("edge10", "vertex3", "vertex1")
    assert occupancy_map.add_edge_with_id("edge3", "vertex1", "vertex4")
    assert occupancy_map.add_edge_with_id("edge11", "vertex4", "vertex1")
    assert occupancy_map.add_edge_with_id("edge4", "vertex2", "vertex3")
    assert occupancy_map.add_edge_with_id("edge12", "vertex3", "vertex2")
    assert occupancy_map.add_edge_with_id("edge5", "vertex3", "vertex4")
    assert occupancy_map.add_edge_with_id("edge13", "vertex4", "vertex3")
    assert occupancy_map.add_edge_with_id("edge6", "vertex2", "vertex5")
    assert occupancy_map.add_edge_with_id("edge14", "vertex5", "vertex2")
    assert occupancy_map.add_edge_with_id("edge7", "vertex3", "vertex5")
    assert occupancy_map.add_edge_with_id("edge15", "vertex5", "vertex3")
    assert occupancy_map.add_edge_with_id("edge8", "vertex4", "vertex5")
    assert occupancy_map.add_edge_with_id("edge16", "vertex5", "vertex4")

def create_small_topological_map_iit(occupancy_map):
    occupancy_map.set_name('small_iit')
    
    # add the vertices
    assert occupancy_map.add_vertex_with_id("vertex1", 0, 0)
    assert occupancy_map.add_vertex_with_id("vertex2", 1, 6)
    assert occupancy_map.add_vertex_with_id("vertex3", 5, 5)
    assert occupancy_map.add_vertex_with_id("vertex4", 7, 0)

    # add the edges
    assert occupancy_map.add_edge_with_id("edge1", "vertex1", "vertex2")
    assert occupancy_map.add_edge_with_id("edge9", "vertex2", "vertex1")
    assert occupancy_map.add_edge_with_id("edge2", "vertex1", "vertex3")
    assert occupancy_map.add_edge_with_id("edge10", "vertex3", "vertex1")
    assert occupancy_map.add_edge_with_id("edge3", "vertex1", "vertex4")
    assert occupancy_map.add_edge_with_id("edge11", "vertex4", "vertex1")
    assert occupancy_map.add_edge_with_id("edge4", "vertex2", "vertex3")
    assert occupancy_map.add_edge_with_id("edge12", "vertex3", "vertex2")
    assert occupancy_map.add_edge_with_id("edge5", "vertex3", "vertex4")
    assert occupancy_map.add_edge_with_id("edge13", "vertex4", "vertex3")

def get_times_atc():
    num_iterations = 2000
    # read the file times_higher_20.csv and put into a list
    filename = 'times_higher_17_atc_reduced'
    time_list = []
    with open(filename + '.csv', 'r') as f:
        reader = csv.reader(f)
        time_list = list(reader)[0]
    times = []
    with open('dataset/atc/atc_reduced.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            times.append(row[0])
    for time_index in range(0, len(times), int(len(times)/num_iterations)):
        time_list.append(times[time_index])
    return time_list

def create_occupancy_map(occupancy_map, level, topological_map_creator_function, num_iterations=1000):
    topological_map_creator_function(occupancy_map)
    for edge in occupancy_map.get_edges_list():
        occupancy_map.add_edge_limit(edge.get_id(), level)
    occupancy_map.calculate_average_edge_traverse_times(num_iterations)
    folder = 'data/occupancy_maps_' + occupancy_map.get_name()
    utils.create_folder(folder)

    filename = folder + '/occupancy_map' + occupancy_map.get_name() + "_" + str(len(level))+'_levels.yaml'
    occupancy_map.save_occupancy_map(filename)

    

if __name__ == "__main__":
    # print(matrix)
    warnings.filterwarnings("ignore")
    predictor = create_atc_cliff_predictor()
    predictor_iit = create_iit_cliff_predictor()
    topological_map_creator_function = [create_large_topological_map_atc_corridor, create_medium_topological_map_atc_corridor, create_small_topological_map_atc_corridor,
                                         create_large_topological_map_atc_square, create_medium_topological_map_atc_square]
    topological_map_creator_function_iit = [create_medium_topological_map_iit, create_small_topological_map_iit]
    # two levels
    occupancy_levels = [(["zero", "one"], {"zero": [0,1], "one": [1,9999999]}),
                        (["zero", "one", "two"], {"zero": [0,1], "one": [1,3], "two": [3,9999999]}),
                        (["zero", "one", "two", "three"], {"zero": [0,1], "one": [1,3], "two": [3,6], "three": [6,9999999]}),
                        (["zero", "one", "two", "three", "four"], {"zero": [0,1], "one": [1,3], "two": [3,5], "three": [5,7], "four": [7,9999999]}),
                        (["zero", "one", "two", "three", "four", "five"], {"zero": [0,1], "one": [1,3], "two": [3,5], "three": [5,7], "four": [7,9], "five": [9,9999999]}),
                        (["zero", "one", "two", "three", "four", "five", "six"], {"zero": [0,1], "one": [1,3], "two": [3,5], "three": [5,7], "four": [7,9], "five": [9,12], "six": [12,9999999]}),
                        (["zero", "one", "two", "three", "four", "five", "six", "seven"], {"zero": [0,1], "one": [1,2], "two": [2,3], "three": [3,4], "four": [4,5], "five": [5,6], "six": [6,7], "seven": [7,9999999]})
                        ]

    for function_name in topological_map_creator_function:
        for levels in occupancy_levels:
            occupancy_map = OccupancyMap(predictor, levels[0])
            create_occupancy_map(occupancy_map, levels[1], function_name)
    
    # for function_name in topological_map_creator_function_iit:
    #     for levels in occupancy_levels:
    #         occupancy_map = OccupancyMap(predictor_iit, levels[0])
    #         create_occupancy_map(occupancy_map, levels[1], function_name)