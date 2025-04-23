
import datetime
import time
import csv
from tqdm import tqdm
from simulator import Simulator, simulate_tsp, simulate_lrtdp
from OccupancyMap import OccupancyMap
import math
from MDP import State
import warnings
from PredictorCreator import create_atc_cliff_predictor



def create_atc_2000(step_length):
    predictor = create_atc_cliff_predictor()
    occupancy_map = OccupancyMap(predictor)
    filename = "medium_occupancy_map_atc_corridor_mixed"
    occupancy_map.load_occupancy_map("data/"+filename+".yaml")
    simulator = Simulator(occupancy_map, 0) 
    # occupancy_map.plot_topological_map()

    # plt.show()
    # for edge in occupancy_map.get_edges_list():
        # print(edge.get_area())
    initial_state_name = "vertex1"
    # load the time list from the csv file
    time_list = [1351651057.177,1351651057.598,1351651058.030,1351651058.444,1351651058.863, 1351647475]
    # time_list = [1351651057.177]
    # time_list = []
    time_list.append(1351647475)
    time_list.append(1351649228)
    time_list.append(1351651158)
    time_list.append(1351642323)
    time_list.append(1351648206)
    time_list.append(1351650423)
    time_list.append(1351643288)
    time_list.append(1351649616)
    time_list.append(1351650585)
    time_list.append(1351649577)
    time_list.append(1351651283)
    times = []
    with open('dataset/atc/atc_reduced.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            times.append(row[0])
    # time_list = []
    for time_index in tqdm(range(0, len(times), step_length)):
        time_list.append(times[time_index])

    # steps = []
    # save the data to a csv file
    # time_list = [0]
    with open('steps_'+filename+'.csv', 'w') as file:
        writer = csv.writer(file)
        writer.writerow(["time", "algorithm", "steps", "time_taken"])
        for time in tqdm(list(set(time_list))):
            time = float(time)
            simulate_tsp(simulator, time, occupancy_map, initial_state_name, writer, file)
            simulate_lrtdp(simulator, time, occupancy_map, initial_state_name, writer, file, 70)


if __name__ == "__main__":
    # print(matrix)
    
    print(datetime.datetime.now())
    warnings.filterwarnings("ignore")
    create_atc_2000(2000)