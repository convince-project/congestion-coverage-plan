# create an MDP class that has the same functionality as the OccupancyMap class
from OccupancyMap import OccupancyMap
import networkx as nx
import matplotlib.pyplot as plt

class MDP:
    def __init__(self, occupancy_map, initial_state):
        self.occupancy_map = occupancy_map
        self.states = []
        self.transitions = []
        for node in self.occupancy_map.get_nodes_list():
            self.states.append(node['id'])
        self.states.append('terminal')
        self.solved = set()
        # add transitions from the terminal state of the occupancy map to the terminal state of the MDP with cost 0
        for node in self.occupancy_map.get_nodes_list():
            if self.occupancy_map.is_terminal_node(node['id']):
                self.transitions.append({'id': node['id'] + 'terminal', 'occupancy': 'low', 'start': node['id'], 'end': 'terminal', 'cost': 0})
        for edge in self.occupancy_map.get_edges_list():
            cost = self.occupancy_map.get_edge_traverse_time(edge['id'])
            self.transitions.append({'id': edge['start'] + edge['end'] + 'high', 'occupancy': 'high', 'start': edge['start'], 'end': edge['end'], 'cost': cost['high']})
            self.transitions.append({'id': edge['start'] + edge['end'] + 'low', 'occupancy': 'low', 'start': edge['start'], 'end': edge['end'], 'cost': cost['low']})
        self.initial_state = initial_state
        self.current_state = initial_state
        self.terminal_states = ['terminal']

    def get_current_state(self):
        return self.current_state

    def get_possible_actions_from_current_state(self):
        return self.get_possible_actions(self.current_state)
    
    def get_possible_actions(self, state):
        actions = []
        for transition in self.transitions:
            if transition['start'] == state:
                actions.append(transition)
        return actions

    def get_terminal_states(self):
        return self.terminal_states
    
    def is_terminal_state(self, state):
        return state in self.terminal_states
    
    def get_transition_cost_from_current_state(self, action, time):
        return self.get_transition_cost(self.current_state, action, time)
    
    def solved(self, state_id, time):
        return (state_id, time) in self.solved
    
    def sample_next_state(self, state, action):
        pass        

    
    def get_transition_cost(self, state, action, time):
        for transition in self.transitions:
            if transition['start'] == state and transition['end'] == action:
                if transition['end'] == 'terminal':
                    return 0
                edge = self.occupancy_map.find_edge(transition['start'], transition['end'])
                if transition['start'] == self.current_state:
                    return self.occupancy_map.get_edge_traverse_time(edge['id'])[self.occupancy_map.get_current_occupancy(time, edge['id'])]
                # this is a hack to get the edge traverse time for the edge
                if time < 0:
                    return self.occupancy_map.get_edge_traverse_time(edge['id'])['low']
                if self.occupancy_map.predict_occupancies_for_edge(time, edge['id']):
                    edge_expected_occupancy = self.occupancy_map.get_edge_expected_occupancy(time, edge['id'])
                    transition_cost = edge_expected_occupancy['high'] * self.occupancy_map.get_edge_traverse_time(edge['id'])['high'] + edge_expected_occupancy['low'] * self.occupancy_map.get_edge_traverse_time(edge['id'])['low']
                    return transition_cost
                # choose a "random" occupancy leve
        return None

    def execute_action(self, action, time):
        self.current_state = action
        self.occupancy_map.reset_occupancies()
        self.occupancy_map.calculate_current_nodes_occupancy()
        self.occupancy_map.calculate_current_edges_occupancy()
        return self.get_transition_cost(self.current_state, action, time)
    
    def get_states(self):
        return self.states
    
    def get_transitions(self):
        return self.transitions

