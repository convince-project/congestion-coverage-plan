import warnings
from tqdm import tqdm
from simulator import Simulator, simulate_tsp, simulate_lrtdp, simulate_lrtdp_planning_while_moving
import csv
from OccupancyMap import OccupancyMap
from MDP import State
from PredictorCreator import create_iit_cliff_predictor, create_atc_cliff_predictor, create_madama_cliff_predictor
import sys
import utils
from tsp import *
import Logger
from hamiltonian_path import * 
def simulate_generic(filename, time_list, initial_state_name, predictor_creator_function, time_bound_lrtdp, simulate_tsp_bool=True, simulate_lrtdp_bool=True, simulate_lrtdp_pwm_bool=True, convergence_threshold=2.5):
    warnings.filterwarnings("ignore")
    folder = 'results/' + filename.split("/")[1]
    utils.create_folder(folder)
    # predictor = predictor_creator_function()
    # occupancy_map = OccupancyMap(predictor)
    # occupancy_map.load_occupancy_map(filename+ "_" + str(2) + "_levels.yaml")
    # occupancy_map.plot_topological_map(predictor.map_file, predictor.fig_size, occupancy_map.get_name())
    # simulator = Simulator(occupancy_map, 0)
    # simulate_lrtdp(simulator, time_list[0], occupancy_map, initial_state_name, None, None, time_bound_lrtdp)
    writer_tsp = None
    writer_lrtdp = None
    writer_lrtdp_pwm = None
    # create files for results
    if simulate_tsp_bool:
        with open(folder + "/" + filename.split("/")[1] + '_tsp.csv', 'w') as file_tsp:
            writer_tsp = csv.writer(file_tsp)
    if simulate_lrtdp_bool:
        with open(folder + "/" + filename.split("/")[1] + '_lrtdp.csv', 'w') as file_lrtdp:
            writer_lrtdp = csv.writer(file_lrtdp)
    if simulate_lrtdp_pwm_bool:
        with open(folder + "/" + filename.split("/")[1] + '_lrtdp_pwm.csv', 'w') as file_lrtdp_pwm:
            writer_lrtdp_pwm = csv.writer(file_lrtdp_pwm)
        # for time in tqdm([0.0]):
        #     for level_number in range(2, 4):
    for time in tqdm(time_list):
        for level_number in [2,5,8]:
            if simulate_tsp_bool:
                time = float(time)
                predictor = predictor_creator_function()
                logger = Logger.Logger(print_time_elapsed=False)
                occupancy_map = OccupancyMap(predictor)
                occupancy_map.set_logger(logger)
                occupancy_map.load_occupancy_map(filename+ "_" + str(level_number) + "_levels.yaml")
                # occupancy_map.plot_topological_map(predictor.map_file, predictor.fig_size, occupancy_map.get_name())
                simulator = Simulator(occupancy_map, 0) 
                with open(folder + "/" + filename.split("/")[1] + '_tsp.csv', 'a') as file_tsp:
                    writer_tsp = csv.writer(file_tsp)
                    print("Simulating TSP for time:", time, "and level:", level_number)
                    simulate_tsp(simulator, time, occupancy_map, initial_state_name, writer_tsp, file_tsp)
            if simulate_lrtdp_bool:
                time = float(time)
                predictor = predictor_creator_function()
                logger = Logger.Logger(print_time_elapsed=False)
                occupancy_map = OccupancyMap(predictor)
                occupancy_map.set_logger(logger)
                occupancy_map.load_occupancy_map(filename+ "_" + str(level_number) + "_levels.yaml")
                # occupancy_map.plot_topological_map(predictor.map_file, predictor.fig_size, occupancy_map.get_name())
                simulator = Simulator(occupancy_map, 0)
                with open(folder + "/" + filename.split("/")[1] + '_lrtdp.csv', 'a') as file_lrtdp:
                    writer_lrtdp = csv.writer(file_lrtdp)
                    print("Simulating LRTDP TVMA for time:", time, "and level:", level_number)
                    simulate_lrtdp(simulator, time, occupancy_map, initial_state_name, writer_lrtdp, file_lrtdp, time_bound_lrtdp, logger, convergence_threshold=convergence_threshold)
            if simulate_lrtdp_pwm_bool:
                time = float(time)
                predictor = predictor_creator_function()
                logger = Logger.Logger(print_time_elapsed=False)
                occupancy_map = OccupancyMap(predictor)
                occupancy_map.set_logger(logger)
                occupancy_map.load_occupancy_map(filename+ "_" + str(level_number) + "_levels.yaml")
                # occupancy_map.plot_topological_map(predictor.map_file, predictor.fig_size, occupancy_map.get_name())
                simulator = Simulator(occupancy_map, 0)
                with open(folder + "/" + filename.split("/")[1] + '_lrtdp_pwm.csv', 'a') as file_lrtdp_pwm:
                    writer_lrtdp_pwm = csv.writer(file_lrtdp_pwm)
                    print("Simulating LRTDP TVMA while moving for time:", time, "and level:", level_number)
                    simulate_lrtdp_planning_while_moving(simulator, time, occupancy_map, initial_state_name, writer_lrtdp_pwm, file_lrtdp_pwm, time_bound_lrtdp, logger, convergence_threshold=convergence_threshold)
                        # break


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


def create_atc_with_name(filename, time_bound_lrtdp, simulate_tsp=True, simulate_lrtdp=True, simulate_lrtdp_pwm=True, convergence_threshold=2.5):
    time_list = get_times_atc()
    initial_state_name = "vertex1"
    predictor_creator_function = create_atc_cliff_predictor
    simulate_generic(filename, time_list, initial_state_name, predictor_creator_function, time_bound_lrtdp, simulate_tsp, simulate_lrtdp, simulate_lrtdp_pwm, convergence_threshold)

def create_madama_with_name(filename, time_bound_lrtdp, simulate_tsp=True, simulate_lrtdp=True, simulate_lrtdp_pwm=True, convergence_threshold=2.5):
    time_list = []
    with open('dataset/madama/detections_november_tracked_fixed.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            time_list.append(row[0])
    selected_time_list = []
    for time_index in tqdm(range(0, len(time_list), 20000)):
        selected_time_list.append(time_list[time_index])
    initial_state_name = "vertex1"
    predictor_creator_function = create_madama_cliff_predictor
    simulate_generic(filename, selected_time_list, initial_state_name, predictor_creator_function, time_bound_lrtdp, simulate_tsp, simulate_lrtdp, simulate_lrtdp_pwm, convergence_threshold)



if __name__ == "__main__":
    # if the argument is the name of the function, then execute the function
    args = sys.argv[1:]
    if len(args) >= 2 and args[0] == "show":
        show_vertex_names = True
        if len(args) > 2 and args[2] == "show_vertex_names":
            show_vertex_names = True
        predictor = None
        if "atc" in args[1]:
            predictor = create_atc_cliff_predictor()
        elif "madama" in args[1]:
            predictor = create_madama_cliff_predictor()
        path = "data/occupancy_maps_" + args[1] + "/occupancy_map_" + args[1] + "_2_levels.yaml"
        print("Loading occupancy map from:", path)
        occupancy_map = OccupancyMap(predictor)
        occupancy_map.load_occupancy_map(path)
        occupancy_map.plot_topological_map(predictor.map_file, predictor.fig_size, "", show_vertex_names) # occupancy_map.get_name())
        occupancy_map.display_topological_map()
    elif len(args) >= 2 and args[0] == "save":
        show_vertex_names = False
        if len(args) > 2 and args[2] == "show_vertex_names":
            show_vertex_names = True
        predictor = None
        if "atc" in args[1]:
            predictor = create_atc_cliff_predictor()
        elif "madama" in args[1]:
            predictor = create_madama_cliff_predictor()
        path = "data/occupancy_maps_" + args[1] + "/occupancy_map_" + args[1] + "_2_levels.yaml"
        print("Loading occupancy map from:", path)
        occupancy_map = OccupancyMap(predictor)
        occupancy_map.load_occupancy_map(path)
        
        occupancy_map.plot_topological_map(predictor.map_file, predictor.fig_size,"") # occupancy_map.get_name())
        occupancy_map.save_figure(occupancy_map.get_name() + ".png")

    elif len(args) > 2 and args[0] == "run":
        run_tsp = False
        run_lrtdp = False
        run_lrtdp_pwm = False

        if "tsp" in args:
            run_tsp = True

        if "lrtdp" in args:
            run_lrtdp = True

        if "lrtdp_pwm" in args:
            run_lrtdp_pwm = True
        path = "data/occupancy_maps_" + args[1] + "/occupancy_map_" + args[1] 

        arg = args[1]
        if "atc" in args[1]:
            create_atc_with_name(path, 350, run_tsp, run_lrtdp, run_lrtdp_pwm, float(args[-1]) if "." in args[-1] else 2.5)
        if "madama" in args[1]:
            create_madama_with_name(path, 350, run_tsp, run_lrtdp, run_lrtdp_pwm, float(args[-1]) if "." in args[-1] else 2.5)
        else:
            print("Function not found: ", arg)

    else:
        print("Invalid arguments.")
        print("Usage: python main_simulator_common.py show <occupancy_map_file> or")
        print("python main_simulator_common.py run <function_name> [tsp] [lrtdp] [lrtdp_pwm] [convergence_threshold]")
        print("Example: python main_simulator_common.py run atc_corridor_11 tsp lrtdp 2.5")
        print("convergence_threshold is optional and defaults to 2.5, it is used for LRTDP methods. It is a float value (need to include a dot).")
        print("Available functions: ")
        print("atc_corridor_11")
        print("atc_corridor_16")
        print("atc_corridor_21")
        print("atc_corridor_26")
        print("madama_11")
        print("madama_16")
        print("madama_21")
        print("madama_26")
        print("madama_doors_16")
        print("madama_doors_21")
        print("madama_doors_26")
        print("madama_sequential_11")
        print("madama_sequential_16")
        print("madama_sequential_21")
        print("madama_sequential_26")