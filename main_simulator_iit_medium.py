
import csv
from tqdm import tqdm
from simulator import Simulator, simulate_lrtdp, simulate_tsp
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
    # for edge in occupancy_map.get_edges_list():
        # print(edge.get_area())
    initial_state_name = "vertex1"
    initial_state = State(initial_state_name, 
                          0, 
                          (occupancy_map.find_vertex_from_id(initial_state_name).get_posx(), 
                           occupancy_map.find_vertex_from_id(initial_state_name).get_posy()), 
                           set([initial_state_name]))
    # time_list = [1717314314.0, 1717314458.0, 1717314208.0, 1717314728.0, 1717314942.0]
    with open('times_higher_7_iit.csv', 'r') as file:
       reader = csv.reader(file)
       for row in reader:
           time_list = row
    with open('steps_iit_time_iter.csv', 'w') as file:
        writer = csv.writer(file)

        for time in tqdm(time_list):
            time = math.trunc(float(time))
            # print(time)
            simulate_tsp(simulator, time, occupancy_map, initial_state_name, writer, file)
            simulate_lrtdp(simulator, time, occupancy_map, initial_state_name, writer, file, 60)



if __name__ == "__main__":
    # print(matrix)
    warnings.filterwarnings("ignore")
    # data/occupancy_map_atc_corridor_latest_times_higher_17_atc_reduced.yaml
    create_iit()


