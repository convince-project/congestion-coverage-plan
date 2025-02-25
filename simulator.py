from MDP import MDP, State, Transition
from LrtdpTvmaAlgorithm import LrtdpTvmaAlgorithm
from OccupancyMap import OccupancyMap
import utils
import warnings
import matplotlib.pyplot as plt
from OccupancyMapCreator import *
from PredictorCreator import *
from tsp import *
from tqdm import *
import copy
import csv
import math
from cliff_predictor import CliffPredictor

class Simulator:

    def __init__(self, occupancy_map, time_for_occupancies):
        self._time_for_occupancies = time_for_occupancies
        self._occupancy_map = occupancy_map
        self._robot_min_speed = 0.6
        self._robot_max_speed = 1.2


    def set_time_for_occupancies(self, time):
        self._time_for_occupancies = time

    def execute_step(self,state, action):
        # print("state", state.get_vertex(), "action", action)
        # print("edge", self._occupancy_map.find_edge_from_position(state.get_vertex(), action))
        if action == "wait":
            return State(state.get_vertex(), state.get_time() + 4, state.get_position(), state.get_visited_vertices().copy())
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
        

    def calculate_traverse_time(self, state, action):
        occupancies = self.get_current_occupancies(state)
        edge_name = self._occupancy_map.find_edge_from_position(state.get_vertex(), action)
        edge_occupancy = 0
        # print("time", state.get_time(),  "occupancies", occupancies)
        # print(state.get_vertex())
        # print(action)
        if edge_name in occupancies.keys():
            edge_occupancy = occupancies[edge_name]
        # print(")
        # print("edge_occupancy", edge_occupancy, "edge_limit", self._occupancy_map.find_edge_limit(edge_name))
        edge_traverse_time = self._occupancy_map.get_edge_traverse_time(edge_name)
        # print("edge_traverse_time", edge_traverse_time)
        traverse_time = edge_traverse_time['low'] + edge_occupancy*1.2
        return traverse_time
    

    def simulate_tsp_curr(self, start_time, initial_state, robot_min_speed = None, robot_max_speed = None):
        matrix = create_matrix_from_occupancy_map_current_occupancy(self._occupancy_map, start_time, initial_state.get_vertex())
        # print(matrix)
        policy = solve_tsp(matrix)
        return self.simulate_tsp(start_time, initial_state, policy, robot_min_speed, robot_max_speed)


    def simulate_tsp_avg(self, start_time, initial_state, robot_min_speed = None, robot_max_speed = None):
        matrix = create_matrix_from_occupancy_map(self._occupancy_map, "average", initial_state.get_vertex())
        # print(matrix)
        policy = solve_tsp(matrix)
        return self.simulate_tsp(start_time, initial_state, policy, robot_min_speed, robot_max_speed)

    def simulate_tsp_max(self, start_time, initial_state, robot_min_speed = None, robot_max_speed = None):
        matrix = create_matrix_from_occupancy_map(self._occupancy_map, "high", initial_state.get_vertex())
        # print(matrix)
        policy = solve_tsp(matrix)
        return self.simulate_tsp(start_time, initial_state, policy, robot_min_speed, robot_max_speed)

    def simulate_tsp_min(self, start_time, initial_state, robot_min_speed = None, robot_max_speed = None):
        matrix = create_matrix_from_occupancy_map(self._occupancy_map, "low", initial_state.get_vertex())
        # print(matrix)
        policy = solve_tsp(matrix)
        return self.simulate_tsp(start_time, initial_state, policy, robot_min_speed, robot_max_speed)

    def simulate_tsp(self, start_time, initial_state, policy, robot_min_speed = None, robot_max_speed = None):
        state = initial_state
        # state.set_time(start_time)
        self.set_time_for_occupancies(start_time)
        # self._occupancy_map.predict_occupancies(time, 50)
        if robot_max_speed is not None:
            self._robot_max_speed = robot_max_speed
        if robot_min_speed is not None:
            self._robot_min_speed = robot_min_speed
        steps = []

        for step in policy[1][1:]:
            vertex_number = step+1
            vertex_name = "vertex" + str(vertex_number)
        prev_step = ""
        # print(policy)
        for step in policy[1][1:]:
            vertex_number = step + 1
            vertex_name = "vertex" + str(vertex_number)
            if (not self._occupancy_map.find_vertex_from_id(vertex_name) is None) and (prev_step == "" or not self._occupancy_map.find_vertex_from_id(prev_step) is None):
                
                state = self.execute_step(state, vertex_name)
                steps.append(vertex_name)
            else:
                state.set_vertex(vertex_name)
                vertices_list = state.get_visited_vertices()
                vertices_list.add(vertex_name)
                state.set_visited_vertices(vertices_list)
            prev_step = vertex_name
        return (state.get_time(), steps)
        # return copy.deepcopy(state.get_time()), copy.deepcopy(policy[0][1:])


    # def execute_step_lrtdp()


    def simulate_lrtdp(self, start_time, initial_state, planner_time_bound, robot_min_speed = None, robot_max_speed = None ):
        # print("start_time", start_time)
        self.set_time_for_occupancies(start_time)
        completed = False
        state = initial_state
        # self._occupancy_map.predict_occupancies(time, 50)

        if robot_max_speed is not None:
            self._robot_max_speed = robot_max_speed
        if robot_min_speed is not None:
            self._robot_min_speed = robot_min_speed
        executed_steps = []
        while not completed:
            # # print("state before", state)
            # print("#####################################################################################")
            # print("init", self.get_current_occupancies(state))
            policy = self.plan(state, planner_time_bound)
            # print(policy)
            if policy[0] == False:
                return False
            if policy[1] is not None:
                # print(policy)
                print("policy for current state", policy[1][str(state)])
                action = policy[1][str(state)]
                # print("action", action[2])
                state = self.execute_step(state, action[2])
                # print(state.get_time(), state.get_vertex())

                executed_steps.append(action[2])
                # print(state.get_time(), state.get_vertex())
                # print("state after", state)
            else:
                # print(state.get_visited_vertices())
                if len(state.get_visited_vertices()) == len(self._occupancy_map.get_vertices_list()):
                    completed = True
        # print (state.get_time(), executed_steps)
        return (state.get_time(), executed_steps)

    def get_current_occupancies(self, state):
        current_time = self._time_for_occupancies + state.get_time()
        return self._occupancy_map.get_current_occupancies(current_time)
         
        

    def plan(self, current_state, planner_time_bound):
        # print("current_state", current_state)
        # print("start_time", self._start_time)
        # print("planning time", self._time_for_occupancies,  current_state.get_time())

        lrtdp = LrtdpTvmaAlgorithm(occupancy_map=self._occupancy_map, 
                                   initial_state_name=current_state.get_vertex(), 
                                   convergence_threshold=0.5, 
                                   time_bound_real=100000, 
                                   planner_time_bound=planner_time_bound, 
                                   time_for_occupancies=self._time_for_occupancies + current_state.get_time(),
                                   time_start=current_state.get_time(),
                                   vinitState=current_state)
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


def simulate_tsp(simulator, time, occupancy_map,  initial_state_name, writer, file):
    stes_curr = simulator.simulate_tsp_curr(time, State(initial_state_name,
                0, 
                (occupancy_map.find_vertex_from_id(initial_state_name).get_posx(), 
                occupancy_map.find_vertex_from_id(initial_state_name).get_posy()), 
                set([initial_state_name])))
    writer.writerow([time, "steps_curr", stes_curr])
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
    file.flush()


def simulate_lrtdp(simulator, time, occupancy_map,  initial_state_name, writer, file, planner_time_bound):
    print("-------------------------------------lrtdp----------------------------------")
    steps_lrtdp = simulator.simulate_lrtdp(time, 
                                           State(initial_state_name, 
                                                0, 
                                                (occupancy_map.find_vertex_from_id(initial_state_name).get_posx(), 
                                                occupancy_map.find_vertex_from_id(initial_state_name).get_posy()), 
                                                set([initial_state_name])), 
                                            planner_time_bound)
    print("=====================================end lrtdp==============================")
    writer.writerow([time, "steps_lrtdp", steps_lrtdp])
    file.flush()

