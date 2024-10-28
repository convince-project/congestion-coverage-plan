# create an MDP class that has the same functionality as the OccupancyMap class
from typing import Any
from OccupancyMap import OccupancyMap
# import networkx as nx
import matplotlib.pyplot as plt
# from graphviz import Digraph

# in the states I need to have the vertex, the time and the position
class State:
    def __init__(self, vertex, time, position, visited_vertices):
        self._vertex = vertex
        self._position = position
        self._time = time
        self._visited_vertices = visited_vertices

    def __eq__(self, other):
        return self._vertex == other.get_vertex() and self._time == other.get_time() and self._position == other.get_position()
    
    def __hash__(self):
        visited_vertices_string = ""
        for vertex in sorted(self._visited_vertices):
            visited_vertices_string = visited_vertices_string + " " + str(vertex)

        return hash((self._vertex, self._time, self._position, visited_vertices_string))
    
    def __str__(self):
        return self.to_string()

    def to_string(self):
        visited_vertices_string = ""
        for vertex in sorted(self._visited_vertices):
            visited_vertices_string = visited_vertices_string + " " + str(vertex)
        return "--current vertex:-- " + str(self._vertex) + " --current time:-- " + str(self._time) + " --already visited vertices:-- " + visited_vertices_string
    
    # create getters and setters for the class
    def get_vertex(self):
        return self._vertex  
    
    def get_time(self):
        return self._time
    
    def get_position(self):
        return self._position
    
    def get_visited_vertices(self):
        return self._visited_vertices
    
    def set_vertex(self, vertex):
        self._vertex = vertex

    def set_time(self, time):
        self._time = time

    def set_position(self, position):
        self._position = position  

    def set_visited_vertices(self, visited_vertices):
        self._visited_vertices = visited_vertices


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
    def __init__(self, occupancy_map):
        self.occupancy_map = occupancy_map
        

    def compute_transition(self, state,  edge, occupancy_level):
        #returns a single transition
        cost = self.occupancy_map.get_edge_traverse_time(edge.get_id())
        # print(state.get_time())
        if self.occupancy_map.get_edge_expected_occupancy(state.get_time(), edge.get_id()) is None:
            self.occupancy_map.predict_occupancies_for_edge_fixed(state.get_time(), edge.get_id())
            # self.occupancy_map.predict_occupancies_for_edge_random(state.get_time(), edge.get_id())
            # print(state.get_time())
            # assert False # for now this should not happen
        return Transition(start=edge.get_start(), 
                          end=edge.get_end(), 
                          action=edge.get_end(),
                          cost=cost[occupancy_level],
                          probability=self.occupancy_map.get_edge_expected_occupancy(state.get_time(), edge.get_id())[occupancy_level],
                          occupancy_level=occupancy_level)


    def get_possible_transitions_from_action(self, state, action):
        #returns a set of transitions
        transitions = set()
        if action == "wait":
            transitions.add(Transition(state.get_vertex(), state.get_vertex(), "wait", 5, 1, "none"))
        else:        
            for edge in self.occupancy_map.get_edges_list():
                if edge.get_start() == state.get_vertex() and edge.get_end() == action:
                    for occupancy_level in ['high', 'low']:
                        transition = self.compute_transition(state, edge, occupancy_level)
                        transitions.add(transition)
        return transitions

    def get_possible_transitions(self, state):
        #returns a set of transitions
        transitions = set()
        actions = self.get_possible_actions(state)
        for action in actions:
            for transition in self.get_possible_transitions_from_action(state, action):
                transitions.add(transition)
        return transitions

    def get_possible_actions(self, state):
        #returns a set of actions
        actions = set()
        for edge in self.occupancy_map.get_edges_list():
            if edge.get_start() == state.get_vertex():
                actions.add(edge.get_end())
        # actions.add("wait")
        # actions.sort()
        return actions
    
    def get_possible_next_states(self, state):
        #returns a set of next states
        next_states = set()        
        for transition in self.get_possible_transitions(state):
            sample = self.compute_next_state(state, transition)
            next_states.add(sample)
        return next_states
    
    def compute_next_state(self, state, transition):
        #returns a single next state
        next_state = None
        for vertex in self.occupancy_map.get_vertices_list():
            if vertex.get_id() == transition.get_end():
                visited_vertices = state.get_visited_vertices().copy()
                if vertex.get_id() not in state.get_visited_vertices():
                    visited_vertices.add(vertex.get_id())
                position = (vertex.get_posx(), vertex.get_posy())
                next_state = State(transition.get_end(), int(state.get_time() + transition.get_cost()), position, visited_vertices)
        return next_state

    def solved(self, state):
        return len(state.get_visited_vertices()) == len(self.occupancy_map.get_vertices_list())
