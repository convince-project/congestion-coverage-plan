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


def simulate_generic(filename, 
                     time_list, 
                     initial_state_name, 
                     predictor_creator_function, 
                     time_bound_lrtdp, 
                     time_bound_real, 
                     run_tsp_bool, 
                     run_lrtdp_bool, 
                     run_lrtdp_pwm_bool, 
                     convergence_threshold, 
                     wait_time):
    print("arguments:")
    print("filename:", filename)
    print("time_list:", time_list)
    print("initial_state_name:", initial_state_name)
    print("time_bound_lrtdp:", time_bound_lrtdp)
    print("time_bound_real:", time_bound_real)
    print("run_tsp_bool:", run_tsp_bool)
    print("run_lrtdp_bool:", run_lrtdp_bool)
    print("run_lrtdp_pwm_bool:", run_lrtdp_pwm_bool)
    print("convergence_threshold:", convergence_threshold)
    print("wait_time:", wait_time)

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
    logger = Logger.Logger(print_time_elapsed=False)

    if run_tsp_bool:
        with open(folder + "/" + filename.split("/")[1] + '_tsp.csv', 'w') as file_tsp:
            writer_tsp = csv.writer(file_tsp)
    if run_lrtdp_bool:
        with open(folder + "/" + filename.split("/")[1] + "_" + str(convergence_threshold).replace(".", "-")  + "_" + str(wait_time) +'_lrtdp.csv', 'w') as file_lrtdp:
            writer_lrtdp = csv.writer(file_lrtdp)
    if run_lrtdp_pwm_bool:
        with open(folder + "/" + filename.split("/")[1] +"_" + str(convergence_threshold).replace(".", "-")  + "_" + str(wait_time)  + '_lrtdp_pwm.csv', 'w') as file_lrtdp_pwm:
            writer_lrtdp_pwm = csv.writer(file_lrtdp_pwm)
        # for time in tqdm([0.0]):
        #     for level_number in range(2, 4):
    for time in tqdm(time_list):
        time = float(time)
        for level_number in [2,5,8]:
            
            if run_tsp_bool:
                predictor = predictor_creator_function()
                occupancy_map = OccupancyMap(predictor)
                occupancy_map.set_logger(logger)
                occupancy_map.load_occupancy_map(filename+ "_" + str(level_number) + "_levels.yaml")
                simulator = Simulator(occupancy_map, 0, wait_time, time_bound_real)

                with open(folder + "/" + filename.split("/")[1] + '_tsp.csv', 'a') as file_tsp:
                    writer_tsp = csv.writer(file_tsp)
                    print("Simulating TSP for time:", time, "and level:", level_number)
                    simulate_tsp(simulator=simulator, 
                                 time=time, 
                                 occupancy_map=occupancy_map, 
                                 initial_state_name=initial_state_name, 
                                 writer=writer_tsp, 
                                 file=file_tsp, 
                                 time_bound=time_bound_real)


            if run_lrtdp_bool:
                predictor = predictor_creator_function()
                occupancy_map = OccupancyMap(predictor)
                occupancy_map.set_logger(logger)
                occupancy_map.load_occupancy_map(filename+ "_" + str(level_number) + "_levels.yaml")
                simulator = Simulator(occupancy_map, 0, wait_time, time_bound_real)
                with open(folder + "/" + filename.split("/")[1] + "_" + str(convergence_threshold).replace(".", "-")  + "_" + str(wait_time) +'_lrtdp.csv', 'a') as file_lrtdp:
                    writer_lrtdp = csv.writer(file_lrtdp)
                    print("Simulating LRTDP TVMA for time:", time, "and level:", level_number)
                    simulate_lrtdp(simulator=simulator, 
                                   time=time, 
                                   occupancy_map=occupancy_map, 
                                   initial_state_name=initial_state_name, 
                                   writer=writer_lrtdp, 
                                   file=file_lrtdp, 
                                   planner_time_bound=time_bound_lrtdp, 
                                   logger=logger, 
                                   convergence_threshold=convergence_threshold)
                    

            if run_lrtdp_pwm_bool:
                predictor = predictor_creator_function()
                occupancy_map = OccupancyMap(predictor)
                occupancy_map.set_logger(logger)
                occupancy_map.load_occupancy_map(filename+ "_" + str(level_number) + "_levels.yaml")
                # occupancy_map.plot_topological_map(predictor.map_file, predictor.fig_size, occupancy_map.get_name())
                simulator = Simulator(occupancy_map, 0, wait_time, time_bound_real)
                with open(folder + "/" + filename.split("/")[1] +"_" + str(convergence_threshold).replace(".", "-")  + "_" + str(wait_time)  + '_lrtdp_pwm.csv', 'a') as file_lrtdp_pwm:
                    writer_lrtdp_pwm = csv.writer(file_lrtdp_pwm)
                    print("Simulating LRTDP TVMA while moving for time:", time, "and level:", level_number)
                    simulate_lrtdp_planning_while_moving(simulator=simulator, 
                                                           time=time, 
                                                           occupancy_map=occupancy_map, 
                                                           initial_state_name=initial_state_name, 
                                                           writer=writer_lrtdp_pwm, 
                                                           file=file_lrtdp_pwm, 
                                                           planner_time_bound=time_bound_lrtdp, 
                                                           logger=logger, 
                                                           convergence_threshold=convergence_threshold)


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


def create_atc_with_name(filename, 
                         time_bound_lrtdp, 
                         time_bound_real, 
                         run_tsp_bool, 
                         run_lrtdp_bool, 
                         run_lrtdp_pwm_bool, 
                         convergence_threshold,
                         wait_time, 
                         times = None):
    time_list = []
    if times is not None:
        time_list = times
    else:
        time_list = get_times_atc()
    print("Selected times:", time_list)
    initial_state_name = "vertex1"
    predictor_creator_function = create_atc_cliff_predictor
    simulate_generic(filename=filename, 
                     time_list=time_list, 
                     initial_state_name=initial_state_name, 
                     predictor_creator_function=predictor_creator_function, 
                     time_bound_lrtdp=time_bound_lrtdp, 
                     time_bound_real=time_bound_real, 
                     run_tsp_bool=run_tsp_bool, 
                     run_lrtdp_bool=run_lrtdp_bool, 
                     run_lrtdp_pwm_bool=run_lrtdp_pwm_bool, 
                     convergence_threshold=convergence_threshold, 
                     wait_time=wait_time)

def create_madama_with_name(filename, 
                         time_bound_lrtdp, 
                         time_bound_real, 
                         run_tsp_bool, 
                         run_lrtdp_bool, 
                         run_lrtdp_pwm_bool, 
                         convergence_threshold,
                         wait_time, 
                         times = None):
    time_list = []
    with open('dataset/madama/madama_reduced_decimals.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            time_list.append(row[0])
    selected_time_list = []
    if times is not None:
        selected_time_list = times
    else:
        for time_index in tqdm(range(0, len(time_list), 5450)):
            selected_time_list.append(time_list[time_index])
    initial_state_name = "vertex1"
    print("Selected times:", selected_time_list)
    predictor_creator_function = create_madama_cliff_predictor
    # simulate_generic(filename, [0], initial_state_name, predictor_creator_function, time_bound_lrtdp, run_tsp_bool, run_lrtdp_bool, run_lrtdp_pwm_bool, convergence_threshold)
    simulate_generic(filename=filename, 
                     time_list= selected_time_list, 
                     initial_state_name=initial_state_name, 
                     predictor_creator_function=predictor_creator_function, 
                     time_bound_lrtdp=time_bound_lrtdp, 
                     time_bound_real=time_bound_real, 
                     run_tsp_bool=run_tsp_bool, 
                     run_lrtdp_bool=run_lrtdp_bool, 
                     run_lrtdp_pwm_bool=run_lrtdp_pwm_bool, 
                     convergence_threshold=convergence_threshold, 
                     wait_time=wait_time)

def print_usage():
    print("")
    print("Usage: python main.py show <occupancy_map_file> [--show_vertex_names] or")
    print("python main.py save <occupancy_map_file> [--show_vertex_names] or")
    print("python main.py run --map <map_name> --algorithms [tsp] [lrtdp] [lrtdp_pwm] --convergence_threshold [convergence_threshold] --wait_time [wait_time] --time_bound_lrtdp [time_bound_lrtdp] --time_bound_real [time_bound_real]")
    print("Example: python main.py run --map atc_corridor_11 --algorithms lrtdp --convergence_threshold 2.5 --wait_time 20 --time_bound_lrtdp 350 --time_bound_real 10000")
    print("Example: python main.py run --map madama_21 --algorithms lrtdp --convergence_threshold 2.5 --wait_time 20 --time_bound_lrtdp 350 --time_bound_real 10000")
    print("Example: python main.py run --map madama_21 --algorithms tsp lrtdp lrtdp_pwm --convergence_threshold 2.5 --wait_time 10 --time_bound_lrtdp 350 --time_bound_real 10000")
    print("Example: python main.py run --map atc_corridor_11 --algorithms tsp lrtdp lrtdp_pwm --convergence_threshold 2.5 --wait_time 1 --time_bound_lrtdp 350 --time_bound_real 10000")
    print("Example: python main.py show --map atc_corridor_11 --show_vertex_names")
    print("Example: python main.py save --map atc_corridor_11 --show_vertex_names")
    print("occupancy_map_file is one of the files in data")
    print("function_name is one of the functions defined below")
    print("tsp, lrtdp, lrtdp_pwm are optional, if not provided, all algorithms will be run")
    print("convergence_threshold is optional, default is 2.5")
    print("wait_time is optional, default is 10")
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



if __name__ == "__main__":
    # if the argument is the name of the function, then execute the function
    args = sys.argv[1:]
    map_name = ""
    if "--map" in args:
        map_index = args.index("--map")
        if map_index + 1 < len(args):
            map_name = args[map_index + 1]
        else:
            print("Error: --map option requires a value.")
            print_usage()
            sys.exit(1)
    else:
        print("Error: --map option is required.")
        print_usage()
        sys.exit(1)

    show_vertex_names = False

    predictor = None
    if "atc" in map_name:
        predictor = create_atc_cliff_predictor()
    elif "madama" in map_name:
        predictor = create_madama_cliff_predictor()
    if args[-1] == "--show_vertex_names":
        show_vertex_names = True
    # param parser, optins are:
    # show <occupancy_map_file> [show_vertex_names]
    # save <occupancy_map_file> [show_vertex_names]
    # run <function_name> --algorithms [tsp] [lrtdp] [lrtdp_pwm] --convergence_threshold [convergence_threshold] --wait_time [wait_time] --time_bound_lrtdp [time_bound_lrtdp] --time_bound_real [time_bound_real]
    # occupancy_map_file is one of the files in data
    # function_name is one of the functions defined below
    # tsp, lrtdp, lrtdp_pwm are optional, if not provided, all algorithms will be run
    # convergence_threshold is optional, default is 2.5
    # wait_time is optional, default is 10
    # example: python main_simulator_common.py run --map atc_corridor_11 --algorithms tsp lrtdp --convergence_threshold 2.5 --wait_time 10
    # example: python main_simulator_common.py run --map madama_21 --algorithms lrtdp_pwm --convergence_threshold 2.5 --wait_time 10
    # example: python main_simulator_common.py run --map madama_21 --algorithms tsp lrtdp lrtdp_pwm --convergence_threshold 2.5 --wait_time 10
    # example: python main_simulator_common.py run --map atc_corridor_11 --algorithms tsp lrtdp lrtdp_pwm --convergence_threshold 2.5 --wait_time 1
    # example: python main_simulator_common.py show --map atc_corridor_11 --show_vertex_names
    # example: python main_simulator_common.py save --map atc_corridor_11 --show_vertex_names


    if len(args) > 2 and args[0] == "run":
        run_tsp_bool = False
        run_lrtdp_bool = False
        run_lrtdp_pwm_bool = False
        convergence_threshold = 2.5
        wait_time = 10
        time_bound_lrtdp = 350
        time_bound_real = 300
        times = None
        if "--algorithms" in args:
            print("Algorithms specified.")
            algorithms_index = args.index("--algorithms")
            for alg in args[algorithms_index + 1:]:
                if alg == "tsp":
                    run_tsp_bool = True
                elif alg == "lrtdp":
                    run_lrtdp_bool = True
                elif alg == "lrtdp_pwm":
                    run_lrtdp_pwm_bool = True
                else:
                    break
        else:
            run_tsp_bool_bool = True
            run_lrtdp_bool = True
            run_lrtdp_pwm_bool = True


        if "--convergence_threshold" in args:
            convergence_index = args.index("--convergence_threshold")
            if convergence_index + 1 < len(args):
                convergence_threshold = float(args[convergence_index + 1])

        if "--wait_time" in args:
            wait_time_index = args.index("--wait_time")
            if wait_time_index + 1 < len(args):
                wait_time = int(args[wait_time_index + 1])
        
        if "--time_bound_lrtdp" in args:
            time_bound_lrtdp_index = args.index("--time_bound_lrtdp")
            if time_bound_lrtdp_index + 1 < len(args):
                time_bound_lrtdp = int(args[time_bound_lrtdp_index + 1])

        if "--time_bound_real" in args:
            time_bound_real_index = args.index("--time_bound_real")
            if time_bound_real_index + 1 < len(args):
                time_bound_real = int(args[time_bound_real_index + 1])
        
        if "--times" in args:
            times_index = args.index("--times")
            times = []
            for time_str in args[times_index + 1:]:
                try:
                    time_val = float(time_str)
                    times.append(time_val)
                except ValueError:
                    print("Invalid time value:", time_str)
                    break
        
        print(times)
        path = "data/occupancy_maps_" + map_name + "/occupancy_map_" + map_name

        arg = map_name
        if "atc" in map_name:
            create_atc_with_name(filename=path, 
                                 time_bound_lrtdp=time_bound_lrtdp, 
                                 time_bound_real=time_bound_real,
                                 run_tsp_bool=run_tsp_bool, run_lrtdp_bool=run_lrtdp_bool, run_lrtdp_pwm_bool=run_lrtdp_pwm_bool, 
                                 convergence_threshold=convergence_threshold, wait_time=wait_time, times=times)
        elif "madama" in map_name:
            create_madama_with_name(filename=path, 
                                    time_bound_lrtdp=time_bound_lrtdp, 
                                    time_bound_real=time_bound_real,
                                    run_tsp_bool=run_tsp_bool, run_lrtdp_bool=run_lrtdp_bool, run_lrtdp_pwm_bool=run_lrtdp_pwm_bool, 
                                    convergence_threshold=convergence_threshold, wait_time=wait_time, times=times)
        else:
            print("Function not found: ", arg)
            print_usage()
            sys.exit(1)



    elif len(args) >= 2 and args[0] == "show":

        


        path = "data/occupancy_maps_" + map_name + "/occupancy_map_" + map_name + "_2_levels.yaml"
        print("Loading occupancy map from:", path)
        occupancy_map = OccupancyMap(predictor)
        occupancy_map.load_occupancy_map(path)
        occupancy_map.plot_topological_map(predictor.map_file, predictor.fig_size, "", show_vertex_names) # occupancy_map.get_name())
        occupancy_map.display_topological_map()
        
    elif len(args) >= 2 and args[0] == "save":

        path = "data/occupancy_maps_" + args[1] + "/occupancy_map_" + args[1] + "_2_levels.yaml"
        print("Loading occupancy map from:", path)
        occupancy_map = OccupancyMap(predictor)
        occupancy_map.load_occupancy_map(path)
        occupancy_map.plot_topological_map(predictor.map_file, predictor.fig_size,"") # occupancy_map.get_name())
        occupancy_map.save_figure(occupancy_map.get_name() + ".png")

    else:
        print("Invalid arguments.")
        print_usage()
        sys.exit(1)
