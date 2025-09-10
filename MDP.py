# create an MDP class that has the same functionality as the OccupancyMap class
from typing import Any
from OccupancyMap import OccupancyMap
# import networkx as nx
import matplotlib.pyplot as plt
import datetime
# from graphviz import Digraph
# in the states I need to have the vertex, the time and the position
from multiprocessing.pool import ThreadPool as Pool
import concurrent.futures
import time
import math
import asyncio
import Logger  # Assuming Logger is in the same directory or properly installed
class State:
    def __init__(self, vertex, time, visited_vertices):
        self._vertex = vertex
        self._time = time
        self._visited_vertices = visited_vertices
        self._id = self._calculate_id()
        # self._vertices_visited_ordered = list(visited_vertices)

    def __eq__(self, other):
        return self._id == other.get_id()

    def __hash__(self):
        return hash(self._id)
    
    def __str__(self):
        return self.to_string()
    
    def to_string(self):
        return self._id

    def _calculate_id(self):
        visited_vertices_string = ""
        for vertex in sorted(self._visited_vertices):
            visited_vertices_string = visited_vertices_string + " " + str(vertex)
        return "--current vertex:-- " + str(self._vertex) + " --current time:-- " + str(math.floor(self._time * 100)/100) + " --already visited vertices:-- " + visited_vertices_string
    
    def get_id(self):
        return self._id
    
    # def to_string_without_time(self):
    #     visited_vertices_string = ""
    #     for vertex in sorted(self._visited_vertices):
    #         visited_vertices_string = visited_vertices_string + " " + str(vertex)
    #     return "--current vertex:-- " + str(self._vertex) + " --already visited vertices:-- " + visited_vertices_string
    
    
    # create getters and setters for the class
    def get_vertex(self):
        return self._vertex  

    def get_time(self):
        return self._time
    
    def get_visited_vertices(self):
        return self._visited_vertices
    
    # def set_vertex(self, vertex):
    #     self._vertex = vertex

    # def set_time(self, time):
    #     self._time = time

    # def set_position(self, position):
    #     self._position = position  

    # def set_visited_vertices(self, visited_vertices):
    #     self._visited_vertices = visited_vertices


class Transition:
    '''
    This class represents a transition in the MDP
    it contains the start state, the end state, the action, the cost and the probability of the transition
    '''


    def __init__(self, start, end, action, cost, probability, occupancy_level):
        self._start = start
        self._end = end
        self._action = action
        self._cost = cost
        self._probability = probability
        self._occupancy_level = occupancy_level

    def __eq__(self, other):
        return self._start == other.get_start() and self._end == other.get_end() and self._action == other.get_action() and self._cost == other.get_cost() and self._probability == other.get_probability()
    
    def __hash__(self):
        return hash(self.__str__())
    
    def __str__(self):
        return "--start:--" + str(self._start) + " --end:-- " + str(self._end) + " --action:-- " + str(self._action) + " --cost:-- " + str(self._cost) + " --probability:-- " + str(self._probability) + " --occupancy level:-- " + str(self._occupancy_level)
    # create getters for the class
    
    def to_string(self):
        return "--start:--" + str(self._start) + " --end:-- " + str(self._end) + " --action:-- " + str(self._action) + " --cost:-- " + str(self._cost) + " --probability:-- " + str(self._probability) + " --occupancy level:-- " + str(self._occupancy_level)

    def get_start(self):
        return self._start
    
    def get_end(self):
        return self._end
    
    def get_action(self):
        return self._action
    
    def get_cost(self):
        return self._cost
    
    def get_probability(self):
        return self._probability
    
    def get_occupancy_level(self):
        return self._occupancy_level


class MDP:
    def __init__(self, occupancy_map, time_for_occupancies , time_start, logger=None):
        self.occupancy_map = occupancy_map
        self.time_start = time_start
        self.time_for_occupancies = time_for_occupancies
        if logger is not None:
            self.logger = logger
        else:
            self.logger = Logger.Logger(print_time_elapsed=False)



    def compute_transition(self, state,  edge, occupancy_level, transitions_list):
        # print ("compute_transition", state, edge, occupancy_level, transitions_list)
        # cpu_time_init = datetime.datetime.now()
        if edge is None:
            print("@@@@@@@@@@@@@@@@Edge not found", state.to_string(), " +++++ ")
            return
        transition_probability = self.calculate_transition_probability(edge,self.time_for_occupancies + state.get_time() - self.time_start, occupancy_level)
        # cpu_time_end = datetime.datetime.now()
        # cpu_time = (cpu_time_end - cpu_time_init).total_seconds()
        # print("compute_transition::CPU time for calculate_transition_probability: ", cpu_time)
        # print ("transition_probability", transition_probability)
        if transition_probability < 0.000001:
            return
        # cpu_time_init = datetime.datetime.now()
        transition_cost = self.calculate_transition_cost(edge,self.time_for_occupancies + state.get_time() - self.time_start , occupancy_level)
        # if edge.get_end() in state.get_visited_vertices():
            # print("Edge already visited", edge.get_end(), "in", state.get_visited_vertices())
            # transition_cost = transition_cost * 2
        # cpu_time_end = datetime.datetime.now()
        # cpu_time = (cpu_time_end - cpu_time_init).total_seconds()
        # print("compute_transition::CPU time for calculate_transition_cost: ", cpu_time)
        transitions_list.append(Transition(start=edge.get_start(), 
                          end=edge.get_end(), 
                          action=edge.get_end(),
                          cost=transition_cost,
                          probability=transition_probability,
                          occupancy_level=occupancy_level))



    def calculate_transition_probability(self, edge, time, occupancy_level):

        edge_limits = self.occupancy_map.find_edge_limit(edge.get_id())[occupancy_level]
        if time - self.time_for_occupancies < 1:
            occupancies = self.occupancy_map.get_current_occupancies(time)
            edge_occupancy = 0
            if edge.get_id() not in occupancies.keys():
                if occupancy_level == self.occupancy_map.get_occupancy_levels()[0]:
                    return 1
                else:
                    return 0
            edge_occupancy = occupancies[edge.get_id()]
            if edge_occupancy in range(edge_limits[0], edge_limits[1]):
                return 1
            else:
                return 0
        else:
            # in this case we are in the future and we need to predict the occupancy, weighting the probability of the occupancy
            # cpu_time_init = datetime.datetime.now()
            occupancies = self.occupancy_map.get_edge_expected_occupancy(time,  edge.get_id())
            # cpu_time_end = datetime.datetime.now()
            # cpu_time = (cpu_time_end - cpu_time_init).total_seconds()
            # print("calculate_transition_probability::CPU time for get_edge_expected_occupancy: ", cpu_time)
            if (occupancies):
                # if I have predicted occupancies
                # cpu_time_init = datetime.datetime.now()
                sum_poisson_binomial = 0
                for x in range(edge_limits[0], min(edge_limits[1], len(occupancies["poisson_binomial"]))):
                    sum_poisson_binomial = sum_poisson_binomial + occupancies["poisson_binomial"][x]
                # better implementation of the poisson binomial
                # cpu_time_end = datetime.datetime.now()
                # cpu_time = (cpu_time_end - cpu_time_init).total_seconds()
                # print("calculate_transition_probability::CPU time for poisson_binomial: ", cpu_time)
                return sum_poisson_binomial
            # if I have not predicted occupancies I will return the zero occupancy
            else:
                # if I have not predicted occupancies all except the low occupancy will be zero probability
                if occupancy_level == self.occupancy_map.get_occupancy_levels()[0]:
                    return 1
                else:
                    return 0



    def calculate_transition_cost(self, edge, time, occupancy_level):
        # edge traverse time with no people
        edge_traverse_time = self.occupancy_map.get_edge_traverse_time(edge.get_id())[self.occupancy_map.get_occupancy_levels()[0]]
        # If I am at the current time I will calculate the traverse time based on the current occupancy
        if time - self.time_for_occupancies < 1:
            occupancies = self.occupancy_map.get_current_occupancies(time)
            edge_occupancy = 0
            if edge.get_id() in occupancies.keys():
                edge_occupancy = occupancies[edge.get_id()]
                return edge_traverse_time + 1.2*edge_occupancy
            return edge_traverse_time # if I have not predicted occupancies all except the low occupancy will be zero probability
        
        # if I am in the future I calculate the expected occupancy
        # self.occupancy_map.predict_occupancies_for_edge(time, edge.get_id())
        occupancies = self.occupancy_map.get_edge_expected_occupancy(time,  edge.get_id())
        # if I have not predicted occupancies I will return the traverse time of the occupancy level  
        if not occupancies:
            return self.occupancy_map.get_edge_traverse_time(edge.get_id())[occupancy_level]
        
        # Otherwise I weight the possible traverse time with the probability of the occupancy
        sum_poisson_binomial = 0
        additional_traverse_time = 0
        edge_limits = self.occupancy_map.find_edge_limit(edge.get_id())[occupancy_level]
        # here I have at least one poisson binomial for the edge
        if len(occupancies["poisson_binomial"]) >= edge_limits[0]:
            for x in range(edge_limits[0], min(edge_limits[1], len(occupancies["poisson_binomial"]))):
                sum_poisson_binomial = sum_poisson_binomial + occupancies["poisson_binomial"][x]
            for x in range(edge_limits[0], min(edge_limits[1], len(occupancies["poisson_binomial"]))):
                additional_traverse_time = ((x)*1.2) * (occupancies["poisson_binomial"][x]) * sum_poisson_binomial
            return edge_traverse_time + additional_traverse_time
        #if I have no poisson binomial for the edge I will return the traverse time of the occupancy level
        return self.occupancy_map.get_edge_traverse_time(edge.get_id())[occupancy_level]



    def get_possible_transitions_from_action(self, state, action, time_bound):
        #returns a set of transitions
        if state.get_time() > time_bound or self.solved(state):
            return []
        # print(action, "action")
        if action == "wait":
            return [Transition(state.get_vertex(), state.get_vertex(), "wait", 4, 1, "none")]
        else:
            # print("action:", action, "state", state.to_string())
            transitions = []
            pairs = []

            edge = self.occupancy_map.find_edge_from_position(state.get_vertex(), action)
            if edge is None:
                print("Edge not found", state.to_string(), " +++++ " , action)
            for occupancy_level in self.occupancy_map.get_occupancy_levels():
                pairs.append((edge, occupancy_level))
                # if we want to use synchronous computation
            cpu_time_init = datetime.datetime.now()
            # if len(pairs) > 3:
            #     print("len(pairs):", len(pairs))
            # print("pairs:", pairs)
            for item in pairs:
                # print(item[0], item[1])
                self.compute_transition(State(state.get_vertex(), state.get_time(), state.get_visited_vertices()), item[0], item[1], transitions)
            cpu_time_end = datetime.datetime.now()
            self.logger.log_time_elapsed("get_possible_transitions_from_action::CPU time for synchronous computation", (cpu_time_end - cpu_time_init).total_seconds())
            # cpu_time = (cpu_time_end - cpu_time_init).total_seconds()
                # print("get_possible_transitions_from_action::CPU time for synchronous computation: ", cpu_time)

            return transitions



    def get_possible_actions(self, state):
        actions = list(set(self.occupancy_map.get_edges_from_vertex(state.get_vertex()).copy() ) - state.get_visited_vertices()) + ["wait"]
        return actions
        # return self.occupancy_map.get_edges_from_vertex(state.get_vertex()).copy() + ["wait"]

        # return self.occupancy_map.get_edges_from_vertex(state.get_vertex())




    def compute_next_state(self, state, transition):
        #returns a single next state
        visited_vertices = state.get_visited_vertices() | set([transition.get_end()])

        return State(transition.get_end(), state.get_time() + transition.get_cost(), visited_vertices)




    def solved(self, state):
        difference = len(self.occupancy_map.get_vertices().keys()) - len(state.get_visited_vertices())
        solved = difference == 0
        # if difference < 1:
        #     print("State not solved: ", state.to_string(), "======")

        # if solved:
        #     print("Solved:", state.to_string())
        return solved
