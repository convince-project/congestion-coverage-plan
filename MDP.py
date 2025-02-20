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
        self._vertices_visited_ordered = [vertex]

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

    def set_ordered_visited_vertex(self, list_or):
        for x in list_or:
            self._vertices_visited_ordered.append(x)

    def add_ordered_visited_vertex(self, vertex):
        self._vertices_visited_ordered.append(vertex)
    
    def get_ordered_visited_vertex(self):
        return self._vertices_visited_ordered

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
    def __init__(self, occupancy_map, time_for_occupancies , time_start):
        self.occupancy_map = occupancy_map
        self.time_start = time_start
        self.time_for_occupancies = time_for_occupancies
        

    def compute_transition(self, state,  edge, occupancy_level):
        # if self.occupancy_map.get_edge_expected_occupancy(state.get_time(), edge.get_id()) is None:
        #     self.occupancy_map.predict_occupancies_for_edge_fixed(state.get_time(), edge.get_id())
            # self.occupancy_map.predict_occupancies_for_edge_random(state.get_time(), edge.get_id())
            # print(state.get_time())
            # assert False # for now this should not happen
        # if occupancy_level == "none":
        #     return Transition(start=edge.get_start(),
        #                         end=edge.get_end(),
        #                         action=edge.get_end(),
        #                         cost=self.occupancy_map.get_edge_traverse_time(edge.get_id())["low"],
        #                         probability=1,
        #                         occupancy_level="low")
        transition_cost = self.calculate_transition_cost(edge,self.time_for_occupancies + state.get_time() - self.time_start , occupancy_level)
        transition_probability = self.calculate_transition_probability(edge,self.time_for_occupancies + state.get_time() - self.time_start, occupancy_level)
        print("cost", transition_cost, "prob", transition_probability)
        return Transition(start=edge.get_start(), 
                          end=edge.get_end(), 
                          action=edge.get_end(),
                          cost=transition_cost,
                          probability=transition_probability,
                          occupancy_level=occupancy_level)

    def calculate_transition_probability(self, edge, time, occupancy_level):
        print("calculate_transition_probability::time", time, self.time_for_occupancies)
        if time - self.time_for_occupancies < 1:
            occupancies = self.occupancy_map.get_current_occupancies(time)
            edge_occupancy = 0
            if edge.get_id() in occupancies.keys():
                edge_occupancy = occupancies[edge.get_id()]
            print("get_current_occupancies", edge_occupancy)
            if  occupancy_level =="high":
                if edge_occupancy >= self.occupancy_map.find_edge_limit(edge.get_id()):
                    print("high, 1")
                    return 1
                else:
                    print("high, 0")
                    return 0
            elif occupancy_level =="low":
                if edge_occupancy < self.occupancy_map.find_edge_limit(edge.get_id()):
                    print("low, 1")
                    return 1
                else:
                    print("low, 0")
                    return 0
        else:
            occupancies = self.occupancy_map.get_edge_expected_occupancy(time,  edge.get_id())
            if (occupancies):
                sum_poisson_binomial = 0
                if occupancy_level =="high":
                    for x in range(self.occupancy_map.find_edge_limit(edge.get_id()) - 1, len(occupancies["poisson_binomial"])):
                        sum_poisson_binomial = sum_poisson_binomial + occupancies["poisson_binomial"][x]
                    print("sum_poisson_binomial_high", sum_poisson_binomial)
                elif occupancy_level == "low":
                    for x in range(0, min(len(occupancies["poisson_binomial"]), self.occupancy_map.find_edge_limit(edge.get_id()))):
                        sum_poisson_binomial = sum_poisson_binomial + occupancies["poisson_binomial"][x]
                    print("sum_poisson_binomial_low", sum_poisson_binomial)
                return sum_poisson_binomial
            elif occupancy_level =="high":
                return 0
            return 1


    def calculate_transition_cost(self, edge, time, occupancy_level):
        
        edge_traverse_time = self.occupancy_map.get_edge_traverse_time(edge.get_id())["low"]
        if time - self.time_for_occupancies < 1:
            occupancies = self.occupancy_map.get_current_occupancies(time)

            edge_occupancy = 0
            if edge.get_id() in occupancies.keys():
                edge_occupancy = occupancies[edge.get_id()]
            return edge_traverse_time + 1.2*edge_occupancy
        
        occupancies = self.occupancy_map.get_edge_expected_occupancy(time,  edge.get_id())
        if occupancy_level =="high":
            if (occupancies):
                if len(occupancies["poisson_binomial"]) >= self.occupancy_map.find_edge_limit(edge.get_id()) - 1:
                    sum_poisson_binomial = 0
                    additional_traverse_time = 0
                    for x in range(self.occupancy_map.find_edge_limit(edge.get_id()) - 1, len(occupancies["poisson_binomial"])):
                        sum_poisson_binomial = sum_poisson_binomial + occupancies["poisson_binomial"][x]
                    # print("sum_poisson_binomial_high", sum_poisson_binomial)
                    for x in range(self.occupancy_map.find_edge_limit(edge.get_id()) - 1, len(occupancies["poisson_binomial"])):
                        additional_traverse_time = ((x)*1.2) * (occupancies["poisson_binomial"][x]) * sum_poisson_binomial

                    print(additional_traverse_time)
                    return edge_traverse_time + additional_traverse_time
            return self.occupancy_map.get_edge_traverse_time(edge.get_id())["high"]
        elif occupancy_level == "low":
            if (occupancies):
                sum_poisson_binomial = 0
                additional_traverse_time = 0
                for x in range(0, min(len(occupancies["poisson_binomial"]), self.occupancy_map.find_edge_limit(edge.get_id()))):
                    sum_poisson_binomial = sum_poisson_binomial + occupancies["poisson_binomial"][x]
                # print("sum_poisson_binomial_low", sum_poisson_binomial)

                for x in range(0, min(len(occupancies["poisson_binomial"]), self.occupancy_map.find_edge_limit(edge.get_id()))):
                    additional_traverse_time = ((x)*1.2) * (occupancies["poisson_binomial"][x]) * sum_poisson_binomial
                    
                print(additional_traverse_time)
                return edge_traverse_time + additional_traverse_time
        return self.occupancy_map.get_edge_traverse_time(edge.get_id())["low"]
        print("errorrrrrr")        

        
        


    def get_possible_transitions_from_action(self, state, action):
        #returns a set of transitions
        transitions = set()
        if action == "wait":
            transitions.add(Transition(state.get_vertex(), state.get_vertex(), "wait", 3, 1, "none"))
        else:        
            for edge in self.occupancy_map.get_edges_list():
                if edge.get_start() == state.get_vertex() and edge.get_end() == action:
                    # print(self.time_for_occupancies)
                    # self.occupancy_map.predict_occupancies(self.time_for_occupancies + state.get_time(), self.time_for_occupancies + state.get_time() + 50)
                        # print(state.get_time())
                    
                    # if self.occupancy_map.get_edge_expected_occupancy(self.time_for_occupancies + state.get_time(), edge.get_id()) is not None:
                    for occupancy_level in ['high', 'low']:
                        transition = self.compute_transition(state, edge, occupancy_level)
                        transitions.add(transition)
                    # else:
                    #     transition = self.compute_transition(state, edge, "none")
                    #     transitions.add(transition)
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
        return sorted(actions)
    
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
                next_state = State(transition.get_end(), state.get_time() + transition.get_cost(), position, visited_vertices)
                next_state.set_ordered_visited_vertex(state.get_ordered_visited_vertex())
                next_state.add_ordered_visited_vertex(vertex.get_id())
        return next_state

    def solved(self, state):
        return len(state.get_visited_vertices()) == len(self.occupancy_map.get_vertices_list())
