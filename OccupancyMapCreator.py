from OccupancyMap import OccupancyMap
import utils
import matplotlib.pyplot as plt
from tsp import create_matrix_from_occupancy_map, create_matrix_from_occupancy_map_current_occupancy, solve_tsp
import csv
from cliff_predictor import CliffPredictor
from PredictorCreator import create_atc_cliff_predictor, create_iit_cliff_predictor
import warnings

def create_medium_topological_map_atc_corridor(occupancy_map):
    occupancy_map.set_name('medium_occupancy_map_atc_corridor')
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


def create_small_topological_map_atc_corridor(occupancy_map):
    occupancy_map.set_name('small_occupancy_map_atc_corridor')
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
    occupancy_map.set_name('medium_occupancy_map_atc_square')
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



def create_medium_topological_map_iit(occupancy_map):
    occupancy_map.set_name('medium_occupancy_map_iit')
    
    # add the vertices
    assert occupancy_map.add_vertex_with_id("vertex1", 0, -11)
    assert occupancy_map.add_vertex_with_id("vertex2", 1, -4)
    assert occupancy_map.add_vertex_with_id("vertex3", 3, -6)
    assert occupancy_map.add_vertex_with_id("vertex4", 8, -11)
    assert occupancy_map.add_vertex_with_id("vertex5", 6, -2)
    assert not occupancy_map.add_vertex_with_id("vertex5", 5, -2)

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
    occupancy_map.set_name('small_occupancy_map_iit')
    
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


def create_small_occupancy_map_atc_corridor(occupancy_map, levels, iterations=1000):
    create_small_topological_map_atc_corridor(occupancy_map)

    for edge in occupancy_map.get_edges_list():
        occupancy_map.add_edge_limit(edge.get_id(), levels)
    occupancy_map.calculate_average_edge_traverse_times(iterations)
    filename = 'data/'+occupancy_map.get_name()+"_"+str(len(levels))+"_levels.yaml"
    occupancy_map.save_occupancy_map(filename)
    

def create_medium_occupancy_map_atc_corridor(occupancy_map, levels):
    create_medium_topological_map_atc_corridor(occupancy_map)
    times = get_times_atc()

    for edge in occupancy_map.get_edges_list():
        occupancy_map.add_edge_limit(edge.get_id(), levels)
    occupancy_map.calculate_average_edge_traverse_times(3000)
    filename = 'data/'+occupancy_map.get_name()+"_"+str(len(levels))+"_levels.yaml"
    occupancy_map.save_occupancy_map(filename)
    



def create_medium_occupancy_map_atc_square(occupancy_map, levels, num_iterations=500):
    create_medium_topological_map_atc_square(occupancy_map)

    # occupancy_map.calculate_average_edge_occupancy_with_times(times)
    # occupancy_map.calculate_average_edge_occupancy(100)
    print(occupancy_map.get_edges_list())    
    for edge in occupancy_map.get_edges_list():
        occupancy_map.add_edge_limit(edge.get_id(), levels)
    print(occupancy_map.edge_limits)
    occupancy_map.calculate_average_edge_traverse_times(num_iterations)
    filename = 'data/'+occupancy_map.get_name()+"_"+str(len(levels))+"_levels.yaml"
    occupancy_map.save_occupancy_map(filename)


def create_medium_occupancy_map_iit(occupancy_map, levels):

    create_medium_topological_map_iit(occupancy_map)
    num_iterations = 2000
    # occupancy_map.calculate_average_edge_occupancy(num_iterations)
    for edge in occupancy_map.get_edges_list():
        occupancy_map.add_edge_limit(edge.get_id(), levels)

    occupancy_map.calculate_average_edge_traverse_times(num_iterations)
    # save the occupancy map
    filename = 'data/medium_occupancy_map_iit_'+str(len(levels))+'_levels.yaml'
    occupancy_map.save_occupancy_map(filename)


def create_small_occupancy_map_iit(occupancy_map, levels):
    create_small_topological_map_iit(occupancy_map)
    num_iterations = 1000
    for edge in occupancy_map.get_edges_list():
        occupancy_map.add_edge_limit(edge.get_id(), levels)
    occupancy_map.calculate_average_edge_traverse_times(num_iterations)
    # save the occupancy map
    filename = 'data/small_occupancy_maps_iit/small_occupancy_map_iit'+str(len(levels))+'_levels.yaml'
    occupancy_map.save_occupancy_map(filename)

    

if __name__ == "__main__":
    # print(matrix)
    warnings.filterwarnings("ignore")
    # predictor = create_atc_cliff_predictor()
    # predictor.display_cliff_map()
    predictor = create_iit_cliff_predictor()
    # occupancy_map = OccupancyMap(predictor, ["zero", "one", "two", "three"])
    # # create_medium_occupancy_map_atc_corridor(occupancy_map)
    # # create_small_occupancy_map_iit(occupancy_map)
    # levels = {"zero": [0,1], "one": [1,4], "two": [4, 12], "three": [12,9999999]}
    # create_small_occupancy_map_atc_corridor(occupancy_map, levels)
    # two levels
    occupancy_map = OccupancyMap(predictor, ["zero", "one"])
    levels = {"zero": [0,1], "one": [1,9999999]}
    create_medium_occupancy_map_iit(occupancy_map, levels)

    # three levels
    occupancy_map = OccupancyMap(predictor, ["zero", "one", "two"])
    levels = {"zero": [0,1], "one": [1,10], "two": [10,9999999]}
    create_medium_occupancy_map_iit(occupancy_map, levels)
    # four levels
    occupancy_map = OccupancyMap(predictor, ["zero", "one", "two", "three"])
    levels = {"zero": [0,1], "one": [1,4], "two": [4, 12], "three": [12,9999999]}
    create_medium_occupancy_map_iit(occupancy_map, levels)
    # five levels
    occupancy_map = OccupancyMap(predictor, ["zero", "one", "two", "three", "four"])
    levels = {"zero": [0,1], "one": [1,4], "two": [4, 8], "three": [8,12], "four": [12,9999999]}
    create_medium_occupancy_map_iit(occupancy_map, levels)

    # six levels
    occupancy_map = OccupancyMap(predictor, ["zero", "one", "two", "three", "four", "five"])
    levels = {"zero": [0,1], "one": [1,3], "two": [3, 6], "three": [6,9], "four": [9,12], "five": [12,9999999]}
    create_medium_occupancy_map_iit(occupancy_map, levels)

    # seven levels
    occupancy_map = OccupancyMap(predictor, ["zero", "one", "two", "three", "four", "five", "six"])
    levels = {"zero": [0,1], "one": [1,3], "two": [3, 5], "three": [5,7], "four": [7,9], "five": [9,12], "six": [12,9999999]}
    create_medium_occupancy_map_iit(occupancy_map, levels)


    # create_small_topological_map_atc_corridor(occupancy_map)
    # occupancy_map.load_occupancy_map('data/medium_occupancy_map_atc_square_mixed.yaml')
    # create_medium_occupancy_map_atc_square(occupancy_map, levels)
    # occupancy_map.plot_topological_map()
    # plt.show()