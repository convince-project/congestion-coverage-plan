import warnings
from tqdm import tqdm
from simulator import Simulator, simulate_tsp, simulate_lrtdp
import csv
from OccupancyMap import OccupancyMap
from MDP import State
from PredictorCreator import create_iit_cliff_predictor, create_atc_cliff_predictor


def simulate_generic(filename, time_list, initial_state_name, predictor_creator_function, time_bound_lrtdp):
    warnings.filterwarnings("ignore")
    for level_number in range(2, 8):
        with open('results/steps_'+filename+ "_" + str(level_number) + '_levels.csv', 'w') as file:
            writer = csv.writer(file)

            for time in tqdm(time_list):
                time = float(time)
                predictor = predictor_creator_function()
                occupancy_map = OccupancyMap(predictor)

                occupancy_map.load_occupancy_map("data/"+filename+ "_" + str(level_number) + "_levels.yaml")
                simulator = Simulator(occupancy_map, 0) 
                simulate_tsp(simulator, time, occupancy_map, initial_state_name, writer, file)
                simulate_lrtdp(simulator, time, occupancy_map, initial_state_name, writer, file, time_bound_lrtdp)


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

    return time_list


def create_iit_small():

    time_list = [1717314314.0 , 1717314458.0, 1717314208.0, 1717314728.0, 1717314942.0, 1717215222.0, 1717218339.0]
    # with open('times_higher_7_iit.csv', 'r') as file:
    #    reader = csv.reader(file)
    #    for row in reader:
    #        time_list = row
    # time_list = [1717314314]
    times = []
    with open('dataset/iit/85_june_occupancy_over_time-09-28-2024_06:59:02_millisecond_tracked.csv', 'r') as file:
    # with open('dataset/iit/iit.csv', 'r') as file:
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
    filename = "small_occupancy_maps_atc_corridor/small_occupancy_map_atc_corridor"
    initial_state_name = "vertex1"
    time_bound_lrtdp = 70
    predictor_creator_function = create_atc_cliff_predictor
    simulate_generic(filename, time_list, initial_state_name, predictor_creator_function, time_bound_lrtdp)


def create_atc_medium_corridor():
    time_list = get_times_atc()
    filename = "medium_occupancy_maps_atc_corridor/medium_occupancy_map_atc_corridor"
    initial_state_name = "vertex1"
    time_bound_lrtdp = 70
    predictor_creator_function = create_atc_cliff_predictor
    simulate_generic(filename, time_list, initial_state_name, predictor_creator_function, time_bound_lrtdp)


def create_atc_medium_square():
    time_list = get_times_atc()
    filename = "medium_occupancy_maps_atc_square/medium_occupancy_map_atc_square"
    initial_state_name = "vertex1"
    time_bound_lrtdp = 70
    predictor_creator_function = create_atc_cliff_predictor
    simulate_generic(filename, time_list, initial_state_name, predictor_creator_function, time_bound_lrtdp)


def create_iit_medium():
    time_list = [1717314314.0 , 1717314458.0, 1717314208.0, 1717314728.0, 1717314942.0, 1717215222.0, 1717218339.0]
    # with open('times_higher_7_iit.csv', 'r') as file:
    #    reader = csv.reader(file)
    #    for row in reader:
    #        time_list = row
    # time_list = [1717314314]
    times = []
    with open('dataset/iit/85_june_occupancy_over_time-09-28-2024_06:59:02_millisecond_tracked.csv', 'r') as file:
    # with open('dataset/iit/iit.csv', 'r') as file:
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
    #create_iit_small()
    create_atc_small()
    #create_iit_medium()
    create_atc_medium_corridor()
    create_atc_medium_square()
    # create_iit_large()
    # create_atc_large()
    # pass
