# based on the TopologicalMap class we add information about edge and nodes occupancy, as well as the limits of the edges and nodes in order to consider them as occupied or not.
# the occupancy map is a dictionary with the following structure:
# {
#   'name': 'map_name',
#   'node_limits' : [{'id': uuidnode, 'limit': n_people}, ....],
#   'edge_limits' : [{'id': uuidedge, 'limit': n_people}, ....],
#   'edge_traverse_time': {'uuidedge': {'high': time, 'low': time}, ....}, 
#   'node_occupancy': {uuidnode: high_or_low, ....},
#   'edge_occupancy': {uuidedge: high_or_low, ....},
#   'node_expected_occupancy': {time: {uuidnode: {'high': n_people, 'low': n_people}, ....}, ....},
#   'edge_expected_occupancy': {time: {uuidedge: {'high': n_people, 'low': n_people}, ....}, ....}
# }
# The occupancy map can be saved and loaded to/from a yaml file.


import yaml
from TopologicalMap import TopologicalMap
import math
# from math import random
import matplotlib.pyplot as plt
import random

class OccupancyMap(TopologicalMap):
    def __init__(self):
        self.occupancy_map = {'name': "", 
                              'node_occupancy': {}, 
                              'edge_occupancy': {},
                            #   'people': [],
                              'node_limits': [], 
                              'edge_limits': [], 
                              'edge_traverse_time': {}, 
                              'node_expected_occupancy': {}, 
                              'edge_expected_occupancy': {}
                             }
        super().__init__()

    def set_name(self, name):
        self.occupancy_map['name'] = name



    # def add_node_occupancy(self, node_id, n_people):
    #     # check if the node exists
    #     if node_id not in [node['id'] for node in self.topological_map['nodes']]:
    #         return False
    #     # add the node occupancy
    #     node_occupancy = {'id': node_id, 'number_of_people': n_people}
    #     self.occupancy_map['node_occupancy'].append(node_occupancy)
    #     return True

    # def add_edge_occupancy(self, edge_id, n_people):
    #     # check if the edge exists
    #     if edge_id not in [edge['id'] for edge in self.topological_map['edges']]:
    #         return False
    #     # add the edge occupancy
    #     edge_occupancy = {'id': edge_id, 'number_of_people': n_people}
    #     self.occupancy_map['edge_occupancy'].append(edge_occupancy)
    #     return True
    
    def add_edge_traverse_time(self, edge_id, occupancy_high_or_low, time):
        # check if the edge exists
        if edge_id not in [edge['id'] for edge in self.topological_map['edges']]:
            return False
        # add the edge traverse time
        if 'edge_traverse_time' not in self.occupancy_map.keys():
            self.occupancy_map['edge_traverse_time'] = {}
        if edge_id not in self.occupancy_map['edge_traverse_time'].keys():
            self.occupancy_map['edge_traverse_time'][edge_id] = {}
        self.occupancy_map['edge_traverse_time'][edge_id][occupancy_high_or_low] = time
        return True

    def add_node_limit(self, node_id, limit):
        # check if the node exists
        if node_id not in [node['id'] for node in self.topological_map['nodes']]:
            return False
        # add the node limit
        node_limit = {'id': node_id, 'limit': limit}
        self.occupancy_map['node_limits'].append(node_limit)
        return True

    def add_edge_limit(self, edge_id, limit):
        # check if the edge exists
        if edge_id not in [edge['id'] for edge in self.topological_map['edges']]:
            return False
        # add the edge limit
        edge_limit = {'id': edge_id, 'limit': limit}
        self.occupancy_map['edge_limits'].append(edge_limit)
        return True

    def find_node_occupancy(self, node_id):
        if node_id in [node['id'] for node in self.occupancy_map['node_occupancy']]:
            return self.occupancy_map['node_occupancy'][node_id]
        return None
    
    def find_edge_occupancy(self, edge_id):
        if edge_id in [edge['id'] for edge in self.occupancy_map['edge_occupancy']]:
            return self.occupancy_map['edge_occupancy'][edge_id]
        return None
    
    def find_node_limit(self, node_id):
        for node in self.occupancy_map['node_limits']:
            if node['id'] == node_id:
                return node['limit']
        return None
    
    def find_edge_limit(self, edge_id):
        for edge in self.occupancy_map['edge_limits']:
            if edge['id'] == edge_id:
                return edge['limit']
        return None
    
    def calculate_current_edges_occupancy(self):
        # put a random occupancy, high or low
        for edge in self.topological_map['edges']:
            if edge['id'] not in self.occupancy_map['edge_occupancy'].keys():
                # put a random occupancy, high or low
                if random.uniform(0,1) < 0.5:
                    self.occupancy_map['edge_occupancy'][edge['id']] = 'high'
                else:
                    self.occupancy_map['edge_occupancy'][edge['id']] = 'low'

    def calculate_current_nodes_occupancy(self):
        # put a random occupancy, high or low
        for node in self.topological_map['nodes']:
            if node['id'] not in self.occupancy_map['node_occupancy'].keys():
                # put a random occupancy, high or low
                if random.uniform(0,1) < 0.5:
                    self.occupancy_map['node_occupancy'][node['id']] = 'high'
                else:
                    self.occupancy_map['node_occupancy'][node['id']] = 'low'
        
    # def update_node_occupancy(self, node_id, n_people):
    #     # here I should have the position of the people instead of the number of people
    #     # and maybe I don't need this but only a way to compute cliff
    #     for node in self.occupancy_map['node_occupancy']:
    #         if node['id'] == node_id:
    #             node['number_of_people'] = n_people
    #             return True
    #     return False
    
    # def update_edge_occupancy(self, edge_id, n_people):
    #     # here I should have the position of the people instead of the number of people
    #     # and maybe I don't need this but only a way to compute cliff
    #     for edge in self.occupancy_map['edge_occupancy']:
    #         if edge['id'] == edge_id:
    #             # put a random occupancy, high or low
    #             if random.uniform(0,1) < 0.5:
    #                 edge['occupancy'] = 'high'
    #             else:
                    
    #             return True
    #     return False
    
    def predict_occupancies(self, time):
        # here I should call cliff
        ret = True
        for node in self.topological_map['nodes']:
            ret = ret and self.predict_occupancies_for_node(time, node['id'])
        for edge in self.topological_map['edges']:
            ret = ret and self.predict_occupancies_for_edge(time, edge['id'])
        return ret
        

    # def predict_occupancies_for_node(self, time, node_id):
    #     # here I should call cliff
    #     if time not in self.occupancy_map['node_expected_occupancy']:
    #         self.occupancy_map['node_expected_occupancy'][time] = {}
    #         # find the node in the nodes list
    #         for node in self.topological_map['node_occupancy']:
    #             if node['id'] == node_id:
    #                 if node['id'] not in self.occupancy_map['node_expected_occupancy'][time]:
    #                     self.occupancy_map['node_expected_occupancy'][time][node['id']] = max(0, node['number_of_people'] + math.floor(random.random() * 5) - 3)
    #     return self.occupancy_map['node_expected_occupancy'][time][node_id]
    
    # def predict_occupancies_for_edge(self, time, edge_id):
    #     # here I should call cliff
    #     if time not in self.occupancy_map['edge_expected_occupancy']:
    #         self.occupancy_map['edge_expected_occupancy'][time] = {}
    #         for edge in self.occupancy_map['edge_occupancy']:
    #             if edge['id'] == edge_id:
    #                 if edge['id'] not in self.occupancy_map['edge_expected_occupancy'][time]:
    #                     self.occupancy_map['edge_expected_occupancy'][time][edge['id']]['high'] = max(0, edge['number_of_people'] + math.floor(random.random() * 5) - 3)
    #                     self.occupancy_map['edge_expected_occupancy'][time][edge['id']]['low'] = max(0, edge['number_of_people'] + math.floor(random.random() * 5) - 3)

    #     return self.occupancy_map['edge_expected_occupancy'][time][edge_id]
    def predict_occupancies_for_edge(self, time, edge_id):
        # here I should call cliff
        if time not in self.occupancy_map['edge_expected_occupancy']:
            self.occupancy_map['edge_expected_occupancy'][time] = {}
        for edge in self.topological_map['edges']:
            if edge['id'] == edge_id:
                if edge_id not in self.occupancy_map['edge_expected_occupancy'][time].keys():
                    self.occupancy_map['edge_expected_occupancy'][time][edge_id] = {}
                    self.occupancy_map['edge_expected_occupancy'][time][edge_id]['high'] = random.uniform(0,1)
                    self.occupancy_map['edge_expected_occupancy'][time][edge_id]['low'] = 1-self.occupancy_map['edge_expected_occupancy'][time][edge_id]['high']
        if edge_id in self.occupancy_map['edge_expected_occupancy'][time]:
            return True
        return False

    def predict_occupancies_for_node(self, time, node_id):
        # here I should call cliff
        # print("predict_occupancies_for_node", time, node_id)
        if time not in self.occupancy_map['node_expected_occupancy']:
            self.occupancy_map['node_expected_occupancy'][time] = {}
        for node in self.topological_map['nodes']:
            if node['id'] == node_id:
                if node_id not in self.occupancy_map['node_expected_occupancy'][time].keys():
                    self.occupancy_map['node_expected_occupancy'][time][node_id] = {}
                    self.occupancy_map['node_expected_occupancy'][time][node_id]['high'] = random.uniform(0,1)
                    self.occupancy_map['node_expected_occupancy'][time][node_id]['low'] = 1-self.occupancy_map['node_expected_occupancy'][time][node_id]['high']
                    
        if node_id in self.occupancy_map['node_expected_occupancy'][time]:
            return True
        return False

    def get_edge_expected_occupancy(self, time, edge_id):
        if time in self.occupancy_map['edge_expected_occupancy']:
            if edge_id in self.occupancy_map['edge_expected_occupancy'][time]:
                return self.occupancy_map['edge_expected_occupancy'][time][edge_id]
        return None
    
    def get_node_expected_occupancy(self, time, node_id):
        if time in self.occupancy_map['node_expected_occupancy']:
            if node_id in self.occupancy_map['node_expected_occupancy'][time]:
                return self.occupancy_map['node_expected_occupancy'][time][node_id]
        return None
    
    def get_edge_traverse_time(self, edge_id):
        if edge_id in self.occupancy_map['edge_traverse_time']:
            return self.occupancy_map['edge_traverse_time'][edge_id]
        return None

    def remove_node_occupancy(self, node_id):
        self.occupancy_map['node_occupancy'] = [node for node in self.occupancy_map['node_occupancy'] if node['id'] != node_id]

    def remove_edge_occupancy(self, edge_id):
        self.occupancy_map['edge_occupancy'] = [edge for edge in self.occupancy_map['edge_occupancy'] if edge['id'] != edge_id]

    def save_occupancy_map(self, filename):
        with open(filename, 'w') as f:
            yaml.dump(self.occupancy_map, f)
    
    def load_occupancy_map(self, filename):
        with open(filename, 'r') as f:
            self.occupancy_map = yaml.load(f, Loader=yaml.FullLoader)

    def reset_occupancies(self):
        self.occupancy_map['node_occupancy'] = {}
        self.occupancy_map['edge_occupancy'] = {}
        self.occupancy_map['node_expected_occupancy'] = {}
        self.occupancy_map['edge_expected_occupancy'] = {}
