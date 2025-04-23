
import datetime
import time
import csv
from tqdm import tqdm
from simulator import Simulator, simulate_tsp, simulate_lrtdp
from OccupancyMap import OccupancyMap
import math
from MDP import State
import warnings
import matplotlib.pyplot as plt
from PredictorCreator import create_atc_cliff_predictor



def create_atc_square(step_length):
    for x in range(2, 4):

        predictor = create_atc_cliff_predictor()
        occupancy_map = OccupancyMap(predictor)
        filename = "medium_occupancy_map_atc_square_"+str(x)+"_levels"
        occupancy_map.load_occupancy_map("data/"+filename+".yaml")
        simulator = Simulator(occupancy_map, 0) 
        # occupancy_map.plot_topological_map()

        # plt.show()
        # for edge in occupancy_map.get_edges_list():
            # print(edge.get_area())
        initial_state_name = "vertex1"
        # load the time list from the csv file
        # time_list = [1351651057.177]
        time_list = []
        time_list.append(1351651349.547)
        time_list.append(1351647527.338)
        # time_list.append(1351650999.49)
        # time_list.append(1351646766.203)
        # time_list.append(1351647047.0)
        # time_list.append(1351648463.573)
        # time_list.append(1351646024.421)
        # time_list.append(1351648569.311)
        # time_list.append(1351646175.766)
        # time_list.append(1351644262.636)
        # time_list.append(1351643495.253)
        # time_list.append(1351648943.591)
        # time_list.append(1351650423.0)
        # time_list.append(1351647935.174)
        # time_list.append(1351644186.617)
        # time_list.append(1351645749.881)
        # time_list.append(1351651158.674)
        # time_list.append(1351649955.723)
        # time_list.append(1351648517.098)
        # time_list.append(1351649339.27)
        # time_list.append(1351647770.436)
        # time_list.append(1351647808.246)
        # time_list.append(1351646115.197)
        # time_list.append(1351651058.863)
        # time_list.append(1351644080.68)
        # time_list.append(1351647475.0)
        # time_list.append(1351644411.427)
        # time_list.append(1351650423.271)
        # time_list.append(1351645952.929)
        # time_list.append(1351649169.963)
        # time_list.append(1351651036.338)
        # time_list.append(1351650538.285)
        # time_list.append(1351648873.953)
        # time_list.append(1351643664.117)
        # time_list.append(1351648641.592)
        # time_list.append(1351642058.707)
        # time_list.append(1351651158.0)
        # time_list.append(1351643063.064)
        # time_list.append(1351647438.026)
        # time_list.append(1351651316.591)
        # time_list.append(1351644992.298)
        # time_list.append(1351648037.488)
        # time_list.append(1351650953.42)
        # time_list.append(1351648165.169)
        # time_list.append(1351643001.929)
        # time_list.append(1351648130.394)
        # time_list.append(1351642699.771)
        # time_list.append(1351650881.671)
        # time_list.append(1351644687.166)
        # time_list.append(1351642504.783)
        # time_list.append(1351647575.408)
        # time_list.append(1351649017.308)
        # time_list.append(1351648301.82)
        # time_list.append(1351649616.224)
        # time_list.append(1351642239.57)

        with open('steps_'+filename+'.csv', 'w') as file:
            writer = csv.writer(file)

            for time in tqdm(time_list):
                time = float(time)
                simulate_tsp(simulator, time, occupancy_map, initial_state_name, writer, file)
                simulate_lrtdp(simulator, time, occupancy_map, initial_state_name, writer, file, 55)


if __name__ == "__main__":
    # print(matrix)
    # print(datetime.datetime.now())
    warnings.filterwarnings("ignore")
    create_atc_square(2000)