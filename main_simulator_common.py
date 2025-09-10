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
def simulate_generic(filename, time_list, initial_state_name, predictor_creator_function, time_bound_lrtdp, simulate_tsp_bool=True, simulate_lrtdp_bool=True, simulate_lrtdp_pwm_bool=True):
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
        with open(folder + "/" + filename.split("/")[1] + '_lrtdp_plan_while_moving.csv', 'w') as file_lrtdp_pwm:
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
                    simulate_lrtdp(simulator, time, occupancy_map, initial_state_name, writer_lrtdp, file_lrtdp, time_bound_lrtdp, logger)
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
                    simulate_lrtdp_planning_while_moving(simulator, time, occupancy_map, initial_state_name, writer_lrtdp_pwm, file_lrtdp_pwm, time_bound_lrtdp, logger)
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


def create_atc_with_name(filename, time_bound_lrtdp, simulate_tsp=True, simulate_lrtdp=True, simulate_lrtdp_pwm=True):
    time_list = get_times_atc()
    initial_state_name = "vertex1"
    predictor_creator_function = create_atc_cliff_predictor
    simulate_generic(filename, time_list, initial_state_name, predictor_creator_function, time_bound_lrtdp, simulate_tsp, simulate_lrtdp, simulate_lrtdp_pwm)

def create_madama_with_name(filename, time_bound_lrtdp, simulate_tsp=True, simulate_lrtdp=True, simulate_lrtdp_pwm=True):
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
    simulate_generic(filename, selected_time_list, initial_state_name, predictor_creator_function, time_bound_lrtdp, simulate_tsp, simulate_lrtdp, simulate_lrtdp_pwm)



if __name__ == "__main__":
    # if the argument is the name of the function, then execute the function
    args = sys.argv[1:]
    if len(args) == 2 and args[0] == "show":

        predictor = create_atc_cliff_predictor()
        occupancy_map = OccupancyMap(predictor)
        occupancy_map.load_occupancy_map(args[1])
        occupancy_map.plot_topological_map(predictor.map_file, predictor.fig_size, occupancy_map.get_name())

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

        arg = args[1]
        if arg == "create_atc_corridor_6":
            create_atc_with_name("data/occupancy_maps_atc_corridor_6/occupancy_map_atc_corridor_6", 350, run_tsp, run_lrtdp, run_lrtdp_pwm)
        elif arg == "create_atc_corridor_11":
            create_atc_with_name("data/occupancy_maps_atc_corridor_11/occupancy_map_atc_corridor_11", 500, run_tsp, run_lrtdp, run_lrtdp_pwm)
        elif arg == "create_atc_corridor_16":
            create_atc_with_name("data/occupancy_maps_atc_corridor_16/occupancy_map_atc_corridor_16", 700, run_tsp, run_lrtdp, run_lrtdp_pwm)
        elif arg == "create_atc_corridor_21":
            create_atc_with_name("data/occupancy_maps_atc_corridor_21/occupancy_map_atc_corridor_21", 700, run_tsp, run_lrtdp, run_lrtdp_pwm)
        elif arg == "create_atc_corridor_26":
            create_atc_with_name("data/occupancy_maps_atc_corridor_26/occupancy_map_atc_corridor_26", 700, run_tsp, run_lrtdp, run_lrtdp_pwm)
        elif arg == "create_madama_11":
            create_madama_with_name("data/occupancy_maps_madama_11/occupancy_map_madama_11", 350, run_tsp, run_lrtdp, run_lrtdp_pwm)
        elif arg == "create_madama_16":
            create_madama_with_name("data/occupancy_maps_madama_16/occupancy_map_madama_16", 500, run_tsp, run_lrtdp, run_lrtdp_pwm)
        elif arg == "create_madama_21":
            create_madama_with_name("data/occupancy_maps_madama_21/occupancy_map_madama_21", 700, run_tsp, run_lrtdp, run_lrtdp_pwm)
        elif arg == "create_madama_26":
            create_madama_with_name("data/occupancy_maps_madama_26/occupancy_map_madama_26", 700, run_tsp, run_lrtdp, run_lrtdp_pwm)
        else:
            print("Function not found: ", arg)

    else:
        print("Invalid arguments.")
        print("Usage: python main_simulator_common.py show <occupancy_map_file> or")
        print("python main_simulator_common.py run <function_name> [tsp] [lrtdp] [lrtdp_pwm]")
        print("Available functions: ")
        print("create_atc_corridor_6")
        print("create_atc_corridor_11")
        print("create_atc_corridor_16")
        print("create_atc_corridor_21")
        print("create_atc_corridor_26")
        print("create_madama_11")
        print("create_madama_16")
        print("create_madama_21")
        print("create_madama_26")