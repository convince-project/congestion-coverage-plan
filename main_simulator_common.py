import warnings
from tqdm import tqdm
from simulator import Simulator, simulate_tsp, simulate_lrtdp
import csv
from OccupancyMap import OccupancyMap
from MDP import State
from PredictorCreator import create_iit_cliff_predictor, create_atc_cliff_predictor
import sys
import utils
from tsp import *
import Logger
from hamiltonian_path import * 
def simulate_generic(filename, time_list, initial_state_name, predictor_creator_function, time_bound_lrtdp):
    warnings.filterwarnings("ignore")
    folder = 'results/' + filename.split("/")[1]
    utils.create_folder(folder)
    # predictor = predictor_creator_function()
    # occupancy_map = OccupancyMap(predictor)
    # occupancy_map.load_occupancy_map(filename+ "_" + str(2) + "_levels.yaml")
    # occupancy_map.plot_topological_map(predictor.map_file, predictor.fig_size, occupancy_map.get_name())
    # simulator = Simulator(occupancy_map, 0)
    # simulate_lrtdp(simulator, time_list[0], occupancy_map, initial_state_name, None, None, time_bound_lrtdp)
    with open(folder + "/" + filename.split("/")[1] + '.csv', 'w') as file:
        writer = csv.writer(file)

        # for time in tqdm([0.0]):
        #     for level_number in range(2, 4):
        
        for time in tqdm(time_list):
            for level_number in range(2, 6):
                time = float(time)
                predictor = predictor_creator_function()
                logger = Logger.Logger(print_time_elapsed=False)
                occupancy_map = OccupancyMap(predictor)
                occupancy_map.set_logger(logger)
                occupancy_map.load_occupancy_map(filename+ "_" + str(level_number) + "_levels.yaml")
                # occupancy_map.plot_topological_map(predictor.map_file, predictor.fig_size, occupancy_map.get_name())
                simulator = Simulator(occupancy_map, 0) 
                simulate_tsp(simulator, time, occupancy_map, initial_state_name, writer, file)
                
                # print(create_matrix_from_occupancy_map_length(occupancy_map,  initial_state_name))
                # solve_with_google(occupancy_map, 0 ,initial_state_name, create_matrix_from_occupancy_map_current_occupancy)
                # print(matrix)
                # graph = create_graph(occupancy_map)
                # hamiltonian_path = hamilton(graph, initial_state_name)
                # print("Hamiltonian Path:", hamiltonian_path)
                # # hamiltonian_cost = compute_solution_cost(hamiltonian_path, occupancy_map)
                # hamiltonian_cost = simulator.simulate_hamiltonian(time,
                #                                           State(
                #                                               initial_state_name,
                #                                               0,
                #                                               set([initial_state_name])
                #                                           ),
                #                                           hamiltonian_path)
                # print("Hamiltonian Path Cost:", hamiltonian_cost)
                # for x in matrix:
                #     for y in x:
                #         print(y, end=",")
                #     print("+")
                print("Simulating LRTDP TVMA for time:", time, "and level:", level_number)
                simulate_lrtdp(simulator, time, occupancy_map, initial_state_name, writer, file, time_bound_lrtdp, logger)


def get_times_atc():
    time_list = []
    time_list.append(1351651349.547)
    time_list.append(1351647527.338)
    time_list.append(1351650999.49)
    time_list.append(1351646766.203)
    time_list.append(1351647047.0)
    time_list.append(1351648463.573)
    time_list.append(1351646024.421)
    time_list.append(1351648569.311)
    time_list.append(1351646175.766)
    time_list.append(1351644262.636)
    time_list.append(1351643495.253)
    time_list.append(1351648943.591)
    time_list.append(1351650423.0)
    time_list.append(1351647935.174)
    time_list.append(1351644186.617)
    time_list.append(1351645749.881)
    time_list.append(1351651158.674)
    time_list.append(1351649955.723)
    time_list.append(1351648517.098)
    time_list.append(1351649339.27)
    time_list.append(1351647770.436)
    time_list.append(1351647808.246)
    time_list.append(1351646115.197)
    time_list.append(1351651058.863)
    time_list.append(1351644080.68)
    time_list.append(1351647475.0)
    time_list.append(1351644411.427)
    time_list.append(1351650423.271)
    time_list.append(1351645952.929)
    time_list.append(1351649169.963)
    time_list.append(1351651036.338)
    time_list.append(1351650538.285)
    time_list.append(1351648873.953)
    time_list.append(1351643664.117)
    time_list.append(1351648641.592)
    time_list.append(1351642058.707)
    time_list.append(1351651158.0)
    time_list.append(1351643063.064)
    time_list.append(1351647438.026)
    time_list.append(1351651316.591)
    time_list.append(1351644992.298)
    time_list.append(1351648037.488)
    time_list.append(1351650953.42)
    time_list.append(1351648165.169)
    time_list.append(1351643001.929)
    time_list.append(1351648130.394)
    time_list.append(1351642699.771)
    time_list.append(1351650881.671)
    time_list.append(1351644687.166)
    time_list.append(1351642504.783)
    time_list.append(1351647575.408)
    time_list.append(1351649017.308)
    time_list.append(1351648301.82)
    time_list.append(1351649616.224)
    time_list.append(1351642239.57)
    times = []
    # with open('dataset/atc/atc_reduced.csv', 'r') as file:
    #     reader = csv.reader(file)
    #     for row in reader:
    #         times.append(row[0])
    # for time_index in tqdm(range(0, len(times), len(times)//130)):
    #     time_list.append(times[time_index])
    # time_list.append(1351648301.82)
    return time_list


def create_iit_small():

    time_list = [1717314314.0 , 1717314458.0, 1717314208.0, 1717314728.0, 1717314942.0, 1717215222.0, 1717218339.0]
    # with open('times_higher_7_iit.csv', 'r') as file:
    #    reader = csv.reader(file)
    #    for row in reader:
    #        time_list = row
    # time_list = [1717314314]
    times = []
    with open('dataset/iit/iit.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            times.append(row[0])
    time_list = []
    for time_index in tqdm(range(0, len(times), 2500)):
        time_list.append(times[time_index])

    filename = "small_occupancy_maps_iit/small_occupancy_map_iit"
    initial_state_name = "vertex1"
    time_bound_lrtdp = 70
    predictor_creator_function = create_iit_cliff_predictor
    simulate_generic(filename, time_list, initial_state_name, predictor_creator_function, time_bound_lrtdp)

def create_atc_small():
    time_list = get_times_atc()
    filename = "data/occupancy_maps_small_atc_corridor/occupancy_map_small_atc_corridor"
    initial_state_name = "vertex1"
    time_bound_lrtdp = 70
    predictor_creator_function = create_atc_cliff_predictor
    simulate_generic(filename, time_list, initial_state_name, predictor_creator_function, time_bound_lrtdp)


def create_atc_medium_corridor():
    time_list = get_times_atc()
    filename = "data/occupancy_maps_medium_atc_corridor/occupancy_map_medium_atc_corridor"
    initial_state_name = "vertex1"
    time_bound_lrtdp = 200
    predictor_creator_function = create_atc_cliff_predictor
    simulate_generic(filename, time_list, initial_state_name, predictor_creator_function, time_bound_lrtdp)

def create_atc_medium_large_corridor():
    time_list = get_times_atc()
    filename = "data/occupancy_maps_medium_large_atc_corridor/occupancy_map_medium_large_atc_corridor"
    initial_state_name = "vertex1"
    time_bound_lrtdp = 200
    predictor_creator_function = create_atc_cliff_predictor
    simulate_generic(filename, time_list, initial_state_name, predictor_creator_function, time_bound_lrtdp)

def create_atc_large_corridor():
    time_list = get_times_atc()
    filename = "data/occupancy_maps_large_atc_corridor/occupancy_map_large_atc_corridor"
    initial_state_name = "vertex1"
    time_bound_lrtdp = 600
    predictor_creator_function = create_atc_cliff_predictor
    simulate_generic(filename, time_list, initial_state_name, predictor_creator_function, time_bound_lrtdp)

def create_atc_medium_square():
    time_list = get_times_atc()
    filename = "data/occupancy_maps_medium_atc_square/occupancy_map_medium_atc_square"
    initial_state_name = "vertex1"
    time_bound_lrtdp = 450
    predictor_creator_function = create_atc_cliff_predictor
    simulate_generic(filename, time_list, initial_state_name, predictor_creator_function, time_bound_lrtdp)

def create_atc_large_square():
    time_list = get_times_atc()
    filename = "data/occupancy_maps_large_atc_square/occupancy_map_large_atc_square"
    initial_state_name = "vertex1"
    time_bound_lrtdp = 450
    predictor_creator_function = create_atc_cliff_predictor
    simulate_generic(filename, time_list, initial_state_name, predictor_creator_function, time_bound_lrtdp)

def create_atc_large_corridor_19():
    time_list = get_times_atc()
    filename = "data/occupancy_maps_large_atc_corridor_19/occupancy_map_large_atc_corridor_19"
    initial_state_name = "vertex1"
    time_bound_lrtdp = 350
    predictor_creator_function = create_atc_cliff_predictor
    simulate_generic(filename, time_list, initial_state_name, predictor_creator_function, time_bound_lrtdp)

def create_atc_with_name(filename, time_bound_lrtdp):
    time_list = get_times_atc()
    initial_state_name = "vertex1"
    predictor_creator_function = create_atc_cliff_predictor
    simulate_generic(filename, time_list, initial_state_name, predictor_creator_function, time_bound_lrtdp)

def create_iit_medium():
    # time_list = [1717314314.0 , 1717314458.0, 1717314208.0, 1717314728.0, 1717314942.0, 1717215222.0, 1717218339.0]
    # with open('times_higher_7_iit.csv', 'r') as file:
    #    reader = csv.reader(file)
    #    for row in reader:
    #        time_list = row
    # time_list = [1717314314]
    times = []
    with open('dataset/iit/iit.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            times.append(row[0])
    time_list = []
    for time_index in tqdm(range(0, len(times), 2500)):
        time_list.append(times[time_index])

    filename = "medium_occupancy_maps_iit/medium_occupancy_map_iit"
    initial_state_name = "vertex1"
    time_bound_lrtdp = 70
    predictor_creator_function = create_iit_cliff_predictor
    simulate_generic(filename, time_list, initial_state_name, predictor_creator_function, time_bound_lrtdp)


if __name__ == "__main__":
    # if the argument is the name of the function, then execute the function
    args = sys.argv[1:]
    if len(args) == 0:
        print("No function name provided. Running all functions.")
        args = ["create_iit_small", "create_atc_small", "create_iit_medium", "create_atc_medium_corridor", "create_atc_large_corridor", "create_iit_large", "create_atc_large"]
    elif len(args) == 2 and args[0] == "show":

        predictor = create_atc_cliff_predictor()
        occupancy_map = OccupancyMap(predictor)
        occupancy_map.load_occupancy_map(args[1])
        occupancy_map.plot_topological_map(predictor.map_file, predictor.fig_size, occupancy_map.get_name())

    elif len(args) == 2 and args[0] == "run":
        arg = args[1]
        if arg == "create_iit_small":
            create_iit_small()
        elif arg == "create_atc_small":
            create_atc_small()
        elif arg == "create_iit_medium":
            create_iit_medium()
        elif arg == "create_atc_medium_corridor":
            create_atc_medium_corridor()
        elif arg == "create_atc_medium_square":
            create_atc_medium_square()
        elif arg == "create_atc_medium_large_corridor":
            create_atc_medium_large_corridor()
        elif arg == "create_atc_large_corridor":
            create_atc_large_corridor()
        elif arg == "create_atc_large_corridor_19":
            create_atc_with_name("data/occupancy_maps_large_atc_corridor_19/occupancy_map_large_atc_corridor_19", 350)
        elif arg == "create_atc_large_corridor_20":
            create_atc_with_name("data/occupancy_maps_large_atc_corridor_20/occupancy_map_large_atc_corridor_20", 350)
        elif arg == "create_atc_large_corridor_21":
            create_atc_with_name("data/occupancy_maps_large_atc_corridor_21/occupancy_map_large_atc_corridor_21", 350)
        elif arg == "create_atc_large_corridor_22":
            create_atc_with_name("data/occupancy_maps_large_atc_corridor_22/occupancy_map_large_atc_corridor_22", 350)
        elif arg == "create_atc_large_corridor_23":
            create_atc_with_name("data/occupancy_maps_large_atc_corridor_23/occupancy_map_large_atc_corridor_23", 350)
        elif arg == "create_atc_large_corridor_24":
            create_atc_with_name("data/occupancy_maps_large_atc_corridor_24/occupancy_map_large_atc_corridor_24", 350)
        elif arg == "create_atc_large_corridor_25":
            create_atc_with_name("data/occupancy_maps_large_atc_corridor_25/occupancy_map_large_atc_corridor_25", 350)
        elif arg == "create_atc_large_corridor_26":
            create_atc_with_name("data/occupancy_maps_large_atc_corridor_26/occupancy_map_large_atc_corridor_26", 350)
        elif arg == "create_atc_large_corridor_27":
            create_atc_with_name("data/occupancy_maps_large_atc_corridor_27/occupancy_map_large_atc_corridor_27", 350)
        elif arg == "create_atc_large_corridor_28":
            create_atc_with_name("data/occupancy_maps_large_atc_corridor_28/occupancy_map_large_atc_corridor_28", 350)
        elif arg == "create_atc_large_corridor_29":
            create_atc_with_name("data/occupancy_maps_large_atc_corridor_29/occupancy_map_large_atc_corridor_29", 350)
        elif arg == "create_atc_large_square":
            create_atc_large_square()
        elif arg == "create_iit_large":
            pass
        elif arg == "create_atc_large":
            pass
        else:
            print("Function not found: ", arg)    


    #create_iit_small()
    # create_atc_small()
    # create_iit_medium()
    # create_atc_medium_corridor()
    # create_atc_medium_square()
    # create_atc_large_corridor()
    # create_iit_large()
    # create_atc_large()
    # pass
    
