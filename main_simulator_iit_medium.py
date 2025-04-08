import matplotlib.pyplot as plt
import datetime
import time
import csv
from tqdm import tqdm
from simulator import Simulator, simulate_tsp, simulate_lrtdp
from OccupancyMap import OccupancyMap
import math
from MDP import State
import warnings
from PredictorCreator import create_iit_cliff_predictor

def create_iit():
    predictor = create_iit_cliff_predictor()
    occupancy_map = OccupancyMap(predictor)
    occupancy_map.load_occupancy_map("data/occupancy_map_iit_medium_latest_10000000.yaml")
    simulator = Simulator(occupancy_map, 0)
    # occupancy_map.plot_topological_map()

    # plt.show()
    # for edge in occupancy_map.get_edges_list():
        # print(edge.get_area())
    initial_state_name = "vertex1"
    initial_state = State(initial_state_name, 
                          0, 
                          (occupancy_map.find_vertex_from_id(initial_state_name).get_posx(), 
                           occupancy_map.find_vertex_from_id(initial_state_name).get_posy()), 
                           set([initial_state_name]))
    # time_list = [1717314314.0, 1717314458.0, 1717314208.0, 1717314728.0, 1717314942.0, 1717215222.0, 1717218339.0]
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
    for time_index in tqdm(range(0, len(times), 1357)):
        time_list.append(times[time_index])
    with open('steps_iit_time_iter.csv', 'w') as file:
        writer = csv.writer(file)

        for time in tqdm(time_list):
            time = float(time)
            # print(time)
            simulate_tsp(simulator, time, occupancy_map, initial_state_name, writer, file)
            simulate_lrtdp(simulator, time, occupancy_map, initial_state_name, writer, file, 30)



if __name__ == "__main__":
    # print(matrix)
    warnings.filterwarnings("ignore")
    # data/occupancy_map_atc_corridor_latest_times_higher_17_atc_reduced.yaml
    create_iit()


