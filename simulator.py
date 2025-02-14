from MDP import MDP, State, Transition
from LrtdpTvmaAlgorithm import LrtdpTvmaAlgorithm
from OccupancyMap import OccupancyMap
import utils
import matplotlib.pyplot as plt
from test_occupancy_map import *
from tsp import *
from tqdm import *
import copy
import csv

from cliff_predictor import CliffPredictor

class Simulator:

    def __init__(self, occupancy_map):
        self._start_time = 0
        self._occupancy_map = occupancy_map
        self._robot_min_speed = 0.6
        self._robot_max_speed = 1.2
        self._mdp = MDP(occupancy_map)


    def execute_step(self,state, action):
        calculated_traverse_time = self.calculate_traverse_time(state, action)
        # print("calculated_traverse_time", calculated_traverse_time)
        next_time = state.get_time() + calculated_traverse_time
        next_vertex = action
        next_position = (self._occupancy_map.find_vertex_from_id(next_vertex).get_posx(), self._occupancy_map.find_vertex_from_id(next_vertex).get_posy())
        visited_vertices = state.get_visited_vertices().copy()
        if next_vertex not in state.get_visited_vertices():
            visited_vertices.add(next_vertex)
        next_state = State(next_vertex, next_time, next_position, visited_vertices)
        return next_state
        # return self._mdp.compute_next_state(state, action)44
        

    def calculate_traverse_time(self, state, action):
        occupancies = self.get_current_occupancies(state)
        edge_name = self._occupancy_map.find_edge_from_position(state.get_vertex(), action)
        edge_occupancy = 0
        
        # print(action)
        if edge_name in occupancies.keys():
            edge_occupancy = occupancies[edge_name]
        edge_traverse_time = self._occupancy_map.get_edge_traverse_time(edge_name)
        # print("edge_traverse_time", edge_traverse_time)
        traverse_time = edge_traverse_time['low'] + edge_occupancy*1.2
        return traverse_time
    

    def simulate_tsp_avg(self, start_time, initial_state, robot_min_speed = None, robot_max_speed = None):
        matrix = create_matrix_from_occupancy_map_current_occupancy(self._occupancy_map, start_time)
        policy = solve_tsp(matrix)
        return self.simulate_tsp(start_time, initial_state, policy, robot_min_speed, robot_max_speed)


    def simulate_tsp_max(self, start_time, initial_state, robot_min_speed = None, robot_max_speed = None):
        matrix = create_matrix_from_occupancy_map(self._occupancy_map, "high")
        policy = solve_tsp(matrix)
        return self.simulate_tsp(start_time, initial_state, policy, robot_min_speed, robot_max_speed)

    def simulate_tsp_min(self, start_time, initial_state, robot_min_speed = None, robot_max_speed = None):
        matrix = create_matrix_from_occupancy_map(self._occupancy_map, "low")
        policy = solve_tsp(matrix)
        return self.simulate_tsp(start_time, initial_state, policy, robot_min_speed, robot_max_speed)

    def simulate_tsp(self, start_time, initial_state, policy, robot_min_speed = None, robot_max_speed = None):
        self._mdp = MDP(self._occupancy_map)
        completed = False
        self._start_time = start_time
        state = initial_state
        # self._occupancy_map.predict_occupancies(time, 50)
        if robot_max_speed is not None:
            self._robot_max_speed = robot_max_speed
        if robot_min_speed is not None:
            self._robot_min_speed = robot_min_speed
        steps = []
        for step in policy[0][1:]:
            vertex_number = step+1
            vertex_name = "vertex" + str(vertex_number)
            # print(vertex_name)
            state = self.execute_step(state, vertex_name)
            steps.append(vertex_name)
        return (state.get_time(), steps)
        # return copy.deepcopy(state.get_time()), copy.deepcopy(policy[0][1:])





    def simulate_lrtdp(self, start_time, initial_state, robot_min_speed = None, robot_max_speed = None ):
        self._mdp = MDP(self._occupancy_map)
        completed = False
        self._start_time = start_time
        state = initial_state
        # self._occupancy_map.predict_occupancies(time, 50)
        if robot_max_speed is not None:
            self._robot_max_speed = robot_max_speed
        if robot_min_speed is not None:
            self._robot_min_speed = robot_min_speed
        executed_steps = []
        while not completed:
            # occupancies = self.get_current_occupancies(state)
            # print("state before", state)
            policy = self.plan(state)
            if policy[0] == False:
                return False
            if policy[1] is not None:
                action = policy[1][str(state)]
                # print("action", action[2])
                state = self.execute_step(state, action[2])
                executed_steps.append(action[2])
                # print("state after", state)
            elif len(state.get_visited_vertices()) == len(self._occupancy_map.get_vertices_list()):
                completed = True
        # print (state.get_time(), executed_steps)
        return (state.get_time(), executed_steps)

    def get_current_occupancies(self, state):
        current_time = self._start_time + state.get_time()
        # print("current_time", current_time)
        return self._occupancy_map.get_current_occupancies(float(int(current_time)))
         
        

    def plan(self, current_state):
        # print("current_state", current_state)
        # print("start_time", self._start_time)

        lrtdp = LrtdpTvmaAlgorithm(occupancy_map=self._occupancy_map, 
                                   initial_state_name=current_state.get_vertex(), 
                                   convergence_threshold=0.5, 
                                   time_bound_real=10000, 
                                   planner_time_bound=50, 
                                   time_for_occupancies=self._start_time + current_state.get_time(),
                                   vinitState=current_state,)
        result = lrtdp.lrtdp_tvma()
        # print("Result---------------------------------------------------")
        # print(result)
        # print("lrtdp.policy", lrtdp.policy)
        # print("current_state", current_state)
        # --current vertex:-- vertex1 --current time:-- 0 --already visited vertices:--  vertex1
        # --current vertex:-- vertex1 --current time:-- 0 --already visited vertices:--  vertex1
        # print("lrtdp.policy.keys()", lrtdp.policy.keys())
        # print("lrtdp.policy[current_state]", lrtdp.policy[str(current_state)])
        if not result:
            return (False, None)
        if lrtdp.policy == {}:
            return (True, None)
        return (True, lrtdp.policy)


def create_iit():
    predictor = create_iit_cliff_predictor()
    occupancy_map = OccupancyMap(predictor)
    occupancy_map.load_occupancy_map("data/occupancy_map_iit_medium_latest_10000000.yaml")
    simulator = Simulator(occupancy_map)
    # for edge in occupancy_map.get_edges_list():
        # print(edge.get_area())
    initial_state_name = "vertex1"
    initial_state = State(initial_state_name, 
                          0, 
                          (occupancy_map.find_vertex_from_id(initial_state_name).get_posx(), 
                           occupancy_map.find_vertex_from_id(initial_state_name).get_posy()), 
                           set([initial_state_name]))
    time_list = [1717314314.0, 1717314458.0, 1717314208.0, 1717314728.0, 1717314942.0]
    with open('steps_iit.csv', 'w') as file:
        writer = csv.writer(file)

        for time in tqdm(time_list):

            steps_avg = simulator.simulate_tsp_avg(time, State(initial_state_name, 
                            0, 
                            (occupancy_map.find_vertex_from_id(initial_state_name).get_posx(), 
                            occupancy_map.find_vertex_from_id(initial_state_name).get_posy()), 
                            set([initial_state_name])))
            writer.writerow([time, "steps_avg", steps_avg])
            steps_max = simulator.simulate_tsp_max(time, State(initial_state_name, 
                            0, 
                            (occupancy_map.find_vertex_from_id(initial_state_name).get_posx(), 
                            occupancy_map.find_vertex_from_id(initial_state_name).get_posy()), 
                            set([initial_state_name])))
            writer.writerow([time, "steps_max", steps_max])
            steps_min = simulator.simulate_tsp_min(time, State(initial_state_name, 
                            0, 
                            (occupancy_map.find_vertex_from_id(initial_state_name).get_posx(), 
                            occupancy_map.find_vertex_from_id(initial_state_name).get_posy()), 
                            set([initial_state_name])))
            writer.writerow([time, "steps_min", steps_min])
            steps_lrtdp = simulator.simulate_lrtdp(time, State(initial_state_name, 
                                0, 
                                (occupancy_map.find_vertex_from_id(initial_state_name).get_posx(), 
                                occupancy_map.find_vertex_from_id(initial_state_name).get_posy()), 
                                set([initial_state_name])))
            writer.writerow([time, "steps_lrtdp", steps_lrtdp])


def create_atc_2000():
    predictor = create_atc_cliff_predictor()
    occupancy_map = OccupancyMap(predictor)
    occupancy_map.load_occupancy_map("data/occupancy_map_atc_corridor_latest_times_higher_17.yaml")
    simulator = Simulator(occupancy_map)
    # for edge in occupancy_map.get_edges_list():
        # print(edge.get_area())
    initial_state_name = "vertex1"
    initial_state = State(initial_state_name, 
                          0, 
                          (occupancy_map.find_vertex_from_id(initial_state_name).get_posx(), 
                           occupancy_map.find_vertex_from_id(initial_state_name).get_posy()), 
                           set([initial_state_name]))
    # load the time list from the csv file
    time_list = [1351651057.177,1351651057.598,1351651058.030,1351651058.444,1351651058.863]
    # with open('times_higher_17.csv', 'r') as file:
    #     reader = csv.reader(file)
    #     for row in reader:
    #         time_list = row
    # steps = []
    # save the data to a csv file
    with open('steps_atc_2000.csv', 'w') as file:
        writer = csv.writer(file)

        for time in tqdm(time_list):

            # steps_avg = simulator.simulate_tsp_avg(time, State(initial_state_name, 
            #                 0, 
            #                 (occupancy_map.find_vertex_from_id(initial_state_name).get_posx(), 
            #                 occupancy_map.find_vertex_from_id(initial_state_name).get_posy()), 
            #                 set([initial_state_name])))
            # writer.writerow([time, "steps_avg", steps_avg])
            # steps_max = simulator.simulate_tsp_max(time, State(initial_state_name, 
            #                 0, 
            #                 (occupancy_map.find_vertex_from_id(initial_state_name).get_posx(), 
            #                 occupancy_map.find_vertex_from_id(initial_state_name).get_posy()), 
            #                 set([initial_state_name])))
            # writer.writerow([time, "steps_max", steps_max])
            # steps_min = simulator.simulate_tsp_min(time, State(initial_state_name, 
            #                 0, 
            #                 (occupancy_map.find_vertex_from_id(initial_state_name).get_posx(), 
            #                 occupancy_map.find_vertex_from_id(initial_state_name).get_posy()), 
            #                 set([initial_state_name])))
            # writer.writerow([time, "steps_min", steps_min])
            steps_lrtdp = simulator.simulate_lrtdp(time, State(initial_state_name, 
                                0, 
                                (occupancy_map.find_vertex_from_id(initial_state_name).get_posx(), 
                                occupancy_map.find_vertex_from_id(initial_state_name).get_posy()), 
                                set([initial_state_name])))
            writer.writerow([time, "steps_lrtdp", steps_lrtdp])
            # row = [("steps_avg", steps_avg), ("steps_max",steps_max), ("steps_min", steps_min), ("steps_lrtdp", steps_lrtdp)]
            # steps.append(row)
 
        # for row in steps:
        #     for algorithm in row:
        #         print(algorithm [0], algorithm[1])
        #     print ("===========================================")


if __name__ == "__main__":
    create_atc_2000()