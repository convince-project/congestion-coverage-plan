from OccupancyMap import OccupancyMap
import utils
import matplotlib.pyplot as plt
from tsp import create_matrix_from_occupancy_map, create_matrix_from_occupancy_map_current_occupancy, solve_tsp
import csv
from cliff_predictor import CliffPredictor
from PredictorCreator import create_atc_cliff_predictor
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



def create_medium_topological_map_atc_square(occupancy_map):
    occupancy_map.set_name('medium_occupancy_map_atc_square')
    occupancy_map.add_vertex_with_id("vertex1", -17.9, 4.9)
    occupancy_map.add_vertex_with_id("vertex2", 1, 4.5)
    occupancy_map.add_vertex_with_id("vertex3", -4.5, -2.2)
    occupancy_map.add_vertex_with_id("vertex4", -6.3, -4.8)
    occupancy_map.add_vertex_with_id("vertex5", -11.1, 2.5)
    occupancy_map.add_vertex_with_id("vertex6", -16.5, 0)
    occupancy_map.add_vertex_with_id("vertex7", -11.1, 0)
    occupancy_map.add_vertex_with_id("vertex8", -6.3, 2.5)

    occupancy_map.add_edge_with_id("edge1", "vertex1", "vertex2")
    occupancy_map.add_edge_with_id("edge2", "vertex1", "vertex5")
    occupancy_map.add_edge_with_id("edge3", "vertex1", "vertex6")

    occupancy_map.add_edge_with_id("edge4", "vertex2", "vertex3")
    occupancy_map.add_edge_with_id("edge5", "vertex2", "vertex5")
    occupancy_map.add_edge_with_id("edge6", "vertex2", "vertex8")

    

    occupancy_map.add_edge_with_id("edge7", "vertex3", "vertex4")
    occupancy_map.add_edge_with_id("edge8", "vertex3", "vertex5")
    occupancy_map.add_edge_with_id("edge9", "vertex3", "vertex7")
    occupancy_map.add_edge_with_id("edge10", "vertex3", "vertex8")

    occupancy_map.add_edge_with_id("edge11", "vertex4", "vertex6")
    occupancy_map.add_edge_with_id("edge12", "vertex4", "vertex7")
    occupancy_map.add_edge_with_id("edge13", "vertex4", "vertex8")

    occupancy_map.add_edge_with_id("edge14", "vertex5", "vertex6")
    occupancy_map.add_edge_with_id("edge15", "vertex5", "vertex7")
    occupancy_map.add_edge_with_id("edge16", "vertex5", "vertex8")
    
    occupancy_map.add_edge_with_id("edge17", "vertex6", "vertex7")

    occupancy_map.add_edge_with_id("edge18", "vertex7", "vertex8")

    # add also the opposite edges

    occupancy_map.add_edge_with_id("edge19", "vertex2", "vertex1")
    occupancy_map.add_edge_with_id("edge20", "vertex5", "vertex1")
    occupancy_map.add_edge_with_id("edge21", "vertex6", "vertex1")

    occupancy_map.add_edge_with_id("edge22", "vertex3", "vertex2")
    occupancy_map.add_edge_with_id("edge23", "vertex5", "vertex2")
    occupancy_map.add_edge_with_id("edge24", "vertex8", "vertex2")

    occupancy_map.add_edge_with_id("edge25", "vertex4", "vertex3")
    occupancy_map.add_edge_with_id("edge26", "vertex5", "vertex3")
    occupancy_map.add_edge_with_id("edge27", "vertex7", "vertex3")
    occupancy_map.add_edge_with_id("edge28", "vertex8", "vertex3")

    occupancy_map.add_edge_with_id("edge29", "vertex6", "vertex4")
    occupancy_map.add_edge_with_id("edge30", "vertex7", "vertex4")
    occupancy_map.add_edge_with_id("edge31", "vertex8", "vertex4")

    occupancy_map.add_edge_with_id("edge32", "vertex6", "vertex5")
    occupancy_map.add_edge_with_id("edge33", "vertex7", "vertex5")
    occupancy_map.add_edge_with_id("edge34", "vertex8", "vertex5")

    occupancy_map.add_edge_with_id("edge35", "vertex7", "vertex6")

    occupancy_map.add_edge_with_id("edge36", "vertex8", "vertex7")



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



def create_medium_occupancy_map_atc_corridor(occupancy_map):
    create_medium_topological_map_atc_corridor(occupancy_map)
    times = get_times_atc()

    for edge in occupancy_map.get_edges_list():
        occupancy_map.add_edge_limit(edge.get_id(), {"zero": [0,0], "one": [1,2], "two": [2, 9999999]})
    occupancy_map.calculate_average_edge_traverse_times(3000)
    filename = 'data/'+occupancy_map.get_name()+"_mixed.yaml"
    occupancy_map.save_occupancy_map(filename)
    



def create_medium_occupancy_map_atc_square(occupancy_map):
    create_medium_topological_map_atc_square(occupancy_map)
    times = get_times_atc()

    # occupancy_map.calculate_average_edge_occupancy_with_times(times)
    # occupancy_map.calculate_average_edge_occupancy(100)
    for edge in occupancy_map.get_edges_list():
        occupancy_map.add_edge_limit(edge.get_id(), {"zero": [0,0], "one": [1,2], "two": [2, 9999999]})
    occupancy_map.calculate_average_edge_traverse_times(100)
    filename = 'data/'+occupancy_map.get_name()+"_mixed.yaml"
    occupancy_map.save_occupancy_map(filename)


def create_medium_occupancy_map_iit(occupancy_map):

    create_medium_topological_map_iit(occupancy_map)
    num_iterations = 1000
    # occupancy_map.calculate_average_edge_occupancy(num_iterations)
    for edge in occupancy_map.get_edges_list():
        occupancy_map.add_edge_limit(edge.get_id(), {"zero": [0,0], "one": [1,2], "two": [2, 9999999]})

    occupancy_map.calculate_average_edge_traverse_times(num_iterations)
    # save the occupancy map
    filename = 'data/occupancy_map_iit_medium_'+str(num_iterations)+'.yaml'
    occupancy_map.save_occupancy_map(filename)


def create_small_occupancy_map_iit(occupancy_map):
    create_small_topological_map_iit(occupancy_map)
    num_iterations = 1000
    for edge in occupancy_map.get_edges_list():
        occupancy_map.add_edge_limit(edge.get_id(), {"zero": [0,0], "one": [1,2], "two": [2, 9999999]})
    occupancy_map.calculate_average_edge_traverse_times(num_iterations)
    # save the occupancy map
    filename = 'data/occupancy_map_iit_small_'+str(num_iterations)+'.yaml'
    occupancy_map.save_occupancy_map(filename)

    

if __name__ == "__main__":
    # print(matrix)
    warnings.filterwarnings("ignore")
    predictor = create_atc_cliff_predictor()
    # predictor.display_cliff_map()
    occupancy_map = OccupancyMap(predictor, ["zero", "one", "two"])
    create_medium_occupancy_map_atc_corridor(occupancy_map)
    # create_small_occupancy_map_iit(occupancy_map)
    # occupancy_map.load_occupancy_map('data/medium_occupancy_map_atc_square_mixed.yaml')
    # occupancy_map.plot_topological_map()
    # plt.show()