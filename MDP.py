# create an MDP class that has the same functionality as the OccupancyMap class
from typing import Any
from OccupancyMap import OccupancyMap
import networkx as nx
import matplotlib.pyplot as plt
from graphviz import Digraph

# in the states I need to have the vertex, the time and the position
class State:
    def __init__(self, vertex, time, position, visited_vertices):
        self._vertex = vertex
        self._position = position
        self._time = time
        self._visited_vertices = visited_vertices

    def __eq__(self, other):
        return self._vertex == other.get_() and self._time == other.get_time() and self._position == other.get_position()
    
    def __hash__(self):
        return hash((self._vertex, self._time, self._position))
    
    def __str__(self):
        return str(self._vertex) + " " + str(self._time) + " " + str(self._position) + " " + str(self._visited_vertices)

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
        cost = self.occupancy_map.get_edge_traverse_time(edge.get_id())
        if self.occupancy_map.get_edge_expected_occupancy(state.get_time(), edge.get_id()) is None:
            self.occupancy_map.predict_occupancies_for_edge(state.get_time(), edge.get_id())
        return Transition(edge.get_start(), 
                          edge.get_end(), 
                          edge.get_end(),
                          cost[occupancy_level],
                          self.occupancy_map.get_edge_expected_occupancy(state.get_time(), edge.get_id())[occupancy_level],
                          occupancy_level)


    def calculate_transitions_from_action(self, state, action):
        transitions = []
        # if action == "wait":
        #     transitions.append(Transition(state.get_vertex(), state.get_vertex(), "wait", 0, 1, "none"))
        #     return transitions
        # print(state.get_vertex(), action)
        for edge in self.occupancy_map.get_edges_list():
            # print(edge.get_start(), edge.get_end())
            if edge.get_start() == state.get_vertex() and edge.get_end() == action:
                for occupancy_level in ['high', 'low']:
                    transition = self.compute_transition(state, edge, occupancy_level)
                    # print(transition.get_start(), transition.get_end(), transition.get_action(), transition.get_cost(), transition.get_probability(), transition.get_occupancy_level())
                    transitions.append(transition)
        return transitions

    def calculate_transitions(self, state):
        transitions = []
        for edge in self.occupancy_map.get_edges_list():
            if edge.get_start() == state.get_vertex():
                for transition in self.calculate_transitions_from_action(state, edge.get_end()):
                    transitions.append(transition)
        return transitions

    def get_possible_actions(self, state):
        actions = []
        for edge in self.occupancy_map.get_edges_list():
            if edge.get_start() == state.get_vertex():
                actions.append(edge.get_end())
        actions.append("wait")
        return actions
    
    def get_possible_next_states(self, state):
        next_states = []
        for transition in self.calculate_transitions(state):
            print(state.get_visited_vertices())
            sample = self.calculate_next_state(state, transition)
            next_states.append(sample)
        return next_states
    
    def calculate_next_state(self, state, transition):
        next_state = None
        for vertex in self.occupancy_map.get_vertices_list():
            if vertex.get_id() == transition.get_end():
                visited_vertices = state.get_visited_vertices().copy()
                if vertex.get_id() not in state.get_visited_vertices():
                    visited_vertices.append(vertex.get_id())
                position = (vertex.get_posx(), vertex.get_posy())
                next_state = State(transition.get_end(), state.get_time() + transition.get_cost(), position, visited_vertices)
        return next_state

    def solved(self, state):
        return len(state.get_visited_vertices()) == len(self.occupancy_map.get_vertices_list())

























    
    # def sample_next_state(self, state, action):
    #     low = None
    #     self.calculate_transitions(state)
    #     for transition in self.calculate_transitions_from_action(state, action):
    #         if low is None:
    #             low = transition
    #         else:
    #             if transition.get_probability() > low.get_probability():
    #                 low = transition
    #     return self.calculate_next_state(state, low)


    # def get_possible_next_states_with_action(self, state, action):
    #     next_states = []
    #     for transition in self.calculate_transitions_from_action(state, action):
    #         sample = self.calculate_next_state(state, transition)
    #         next_states.append(sample)
    #     return next_states

    # state = None
    # for vertex in occupancy_map.get_vertices_list():
    #     if vertex.get_id() == initial_state:
    #         state = State(vertex.get_id(), 0, (vertex.get_posx(), vertex.get_posy()), [vertex.get_id()])
    #         self.states.append(state)
                
    # def check_goal(self):
    #     for vertex in self.occupancy_map.get_vertices_list():
    #         if not vertex.get_id() in self.solved[0]:
    #             return False
    #     return True

    # def get_current_state(self):
    #     return self.current_state

    # def get_possible_actions_from_current_state(self):
    #     return self.get_possible_actions(self.current_state)
    
    # def print_states(self):
    #     for state in self.states:
    #         print(state.get_id())

    # def print_transitions(self):
    #     for transition in self.transitions:
    #         print(transition.get_id())

    # def execute_action(self, action):
    #     self.current_state.set_visited_vertices(self.current_state.get_visited_vertices() + [self.current_state.get_vertex()])
        
    #     self.current_state = action
    #     self.occupancy_map.reset_occupancies()
    #     self.occupancy_map.calculate_current_vertices_occupancy()
    #     self.occupancy_map.calculate_current_edges_occupancy()
    #     return self.get_transition_cost(self.current_state, action)

    # def plot_as_graph(self):
    #     G = nx.DiGraph()
    #     for state in self.states:
    #         G.add_node(state.get_id())
    #     for transition in self.transitions:
    #         G.add_edge(transition.get_start(), transition.get_end())
    #     pos = nx.spring_layout(G)
    #     nx.draw(G, pos, with_labels=True)
    #     plt.show()

    
    # def get_transition_cost(self, state, action, time):
    #     for transition in self.transitions:
    #         if transition.get_start() == state and transition.get_end() == action:
    #             edge = self.occupancy_map.find_edge(transition.get_start(), transition.get_end())
    #             if transition.get_start() == self.current_state:
    #                 return self.occupancy_map.get_edge_traverse_time(edge.get_id())[self.occupancy_map.get_current_occupancy(time, edge.get_id())]
    #             # this is a hack to get the edge traverse time for the edge
    #             if time < 0:
    #                 return None
    #             if self.occupancy_map.predict_occupancies_for_edge(time, edge.get_id()):
    #                 edge_expected_occupancy = self.occupancy_map.get_edge_expected_occupancy(time, edge.get_id())
    #                 transition_cost = edge_expected_occupancy['high'] * self.occupancy_map.get_edge_traverse_time(edge.get_id())['high'] + edge_expected_occupancy['low'] * self.occupancy_map.get_edge_traverse_time(edge.get_id())['low']
    #                 return transition_cost
    #     return None
    

    # def get_transition_cost_from_current_state(self, action, time):
    #     return self.get_transition_cost(self.current_state, action, time)
    

        
    # def find_state(self, vertex, time):
        # for state in self.states:
        #     if state.get_id() == vertex.get_id() and state.get_time() == time:
        #         return state
        # return None
