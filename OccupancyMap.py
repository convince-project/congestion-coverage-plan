# based on the TopologicalMap class we add information about edge and vertices occupancy, as well as the limits of the edges and vertices in order to consider them as occupied or not.
# the occupancy map is a dictionary with the following structure:
# {
#   'name': 'map_name',
#   'vertex_limits' : [{'id': uuidvertex, 'limit': n_people}, ....],
#   'edge_limits' : [{'id': uuidedge, 'limit': n_people}, ....],
#   'edge_traverse_time': {'uuidedge': {'high': time, 'low': time}, ....}, 
#   'vertex_occupancy': {uuidvertex: high_or_low, ....},
#   'edge_occupancy': {uuidedge: high_or_low, ....},
#   'vertex_expected_occupancy': {time: {uuidvertex: {'high': n_people, 'low': n_people}, ....}, ....},
#   'edge_expected_occupancy': {time: {uuidedge: {'high': n_people, 'low': n_people}, ....}, ....}
# }
# The occupancy map can be saved and loaded to/from a yaml file.


import yaml
from TopologicalMap import TopologicalMap
import matplotlib.pyplot as plt
import random

class OccupancyMap(TopologicalMap):
    def __init__(self):
        self.name = ""
        self.vertex_occupancy = {}
        self.edge_occupancy = {}
        self.vertex_limits = []
        self.edge_limits = []
        self.edge_traverse_time = {}
        self.vertex_expected_occupancy = {}
        self.edge_expected_occupancy = {}
        super().__init__()

    def set_name(self, name):
        self.name = name
    


    # add the traverse time for an edge
    def add_edge_traverse_time(self, edge_id, occupancy_high_or_low, time):
        # check if the edge exists
        if self.find_edge_from_id(edge_id) is None:
            return False
        # add the edge traverse time
        if edge_id not in self.edge_traverse_time.keys():
            self.edge_traverse_time[edge_id] = {}
        if occupancy_high_or_low in self.edge_traverse_time[edge_id].keys():
            return False
        self.edge_traverse_time[edge_id][occupancy_high_or_low] = time
        return True
    


    # add the limits for vertices and edges
    def add_vertex_limit(self, vertex_id, limit):
        # check if the vertex exists
        if self.find_vertex_from_id(vertex_id) is None:
            return False
        # add the vertex limit
        found = False
        for vertex in self.vertex_limits:
            if vertex['id'] == vertex_id:
                found = True
                break
        if found:
            return False
        vertex_limit = {'id': vertex_id, 'limit': limit}
        self.vertex_limits.append(vertex_limit)
        return True

    def add_edge_limit(self, edge_id, limit):
        # check if the edge exists
        if self.find_edge_from_id(edge_id) is None:
            return False
        # add the edge limit
        found = False
        for edge in self.edge_limits:
            if edge['id'] == edge_id:
                found = True
                break
        if found:
            return False
        edge_limit = {'id': edge_id, 'limit': limit}
        self.edge_limits.append(edge_limit)
        return True
    

    # find the limits for vertices and edges
    def find_vertex_limit(self, vertex_id):
        for vertex in self.vertex_limits:
            if vertex['id'] == vertex_id:
                return vertex['limit']
        return None
    
    def find_edge_limit(self, edge_id):
        for edge in self.edge_limits:
            if edge['id'] == edge_id:
                return edge['limit']
        return None
    


    # find the occupancy for vertices and edges
    def find_vertex_occupancy(self, vertex_id):
        if vertex_id in [vertex['id'] for vertex in self.vertex_occupancy]:
            return self.vertex_occupancy[vertex_id]
        return None
    
    def find_edge_occupancy(self, edge_id):
        if edge_id in [edge['id'] for edge in self.edge_occupancy]:
            return self.edge_occupancy[edge_id]
        return None
    

    # add the occupancy for vertices and edges
    def add_vertex_occupancy(self, vertex_id, occupancy_high, occupancy_low, time):
        # check if the vertex exists
        if self.find_vertex_from_id(vertex_id) is None:
            return False
        if occupancy_high != (1 - occupancy_low):
            return False
        if time not in self.vertex_expected_occupancy:
            self.vertex_expected_occupancy[time] = {}
        elif vertex_id in self.vertex_expected_occupancy[time]:
            return False
        for vertex in self.vertices:
            if vertex.get_id() == vertex_id:
                if vertex_id not in self.vertex_expected_occupancy[time].keys():
                    self.vertex_expected_occupancy[time][vertex_id] = {}
                    self.vertex_expected_occupancy[time][vertex_id]['high'] = occupancy_high
                    self.vertex_expected_occupancy[time][vertex_id]['low'] = occupancy_low
        # add the vertex occupancy
        return True
    

    def add_edge_occupancy(self, edge_id, occupancy_high, occupancy_low, time):
        # check if the edge exists
        if self.find_edge_from_id(edge_id) is None:
            return False
        if occupancy_high != (1 - occupancy_low):
            return False
        if time not in self.edge_expected_occupancy:
            self.edge_expected_occupancy[time] = {}
        elif edge_id in self.edge_expected_occupancy[time]:
            return False
        for edge in self.edges:
            if edge.get_id() == edge_id:
                if edge_id not in self.edge_expected_occupancy[time].keys():
                    self.edge_expected_occupancy[time][edge_id] = {}
                    self.edge_expected_occupancy[time][edge_id]['high'] = occupancy_high
                    self.edge_expected_occupancy[time][edge_id]['low'] = occupancy_low
        # add the edge occupancy
        return True        
        


    # random occupancy calculator    
    def calculate_current_edges_occupancy(self):
        # put a random occupancy, high or low
        for edge in self.edges:
            if edge.get_id() not in self.edge_occupancy.keys():
                # put a random occupancy, high or low
                if random.uniform(0,1) < 0.5:
                    self.edge_occupancy[edge.get_id()] = 'high'
                else:
                    self.edge_occupancy[edge.get_id()] = 'low'

    def calculate_current_vertices_occupancy(self):
        # put a random occupancy, high or low
        for vertex in self.vertices:
            if vertex.get_id() not in self.vertex_occupancy.keys():
                # put a random occupancy, high or low
                if random.uniform(0,1) < 0.5:
                    self.vertex_occupancy[vertex.get_id()] = 'high'
                else:
                    self.vertex_occupancy[vertex.get_id()] = 'low'


    # predict the occupancy of the vertices and edges
    def predict_occupancies(self, time):
        # here I should call cliff
        ret = True
        for vertex in self.vertices:
            ret = ret and self.predict_occupancies_for_vertex(time, vertex.get_id())
        for edge in self.edges:
            ret = ret and self.predict_occupancies_for_edge(time, edge.get_id())
        return ret
    
    def predict_occupancies_for_edge(self, time, edge_id):
        # here I should call cliff
        if time not in self.edge_expected_occupancy:
            self.edge_expected_occupancy[time] = {}
        for edge in self.edges:
            if edge.get_id() == edge_id:
                if edge_id not in self.edge_expected_occupancy[time].keys():
                    self.edge_expected_occupancy[time][edge_id] = {}
                    self.edge_expected_occupancy[time][edge_id]['high'] = random.uniform(0,1)
                    self.edge_expected_occupancy[time][edge_id]['low'] = 1-self.edge_expected_occupancy[time][edge_id]['high']
        if edge_id in self.edge_expected_occupancy[time]:
            return True
        return False

    def predict_occupancies_for_vertex(self, time, vertex_id):
        # here I should call cliff
        if time not in self.vertex_expected_occupancy:
            self.vertex_expected_occupancy[time] = {}
        for vertex in self.vertices:
            if vertex.get_id() == vertex_id:
                if vertex_id not in self.vertex_expected_occupancy[time].keys():
                    self.vertex_expected_occupancy[time][vertex_id] = {}
                    self.vertex_expected_occupancy[time][vertex_id]['high'] = random.uniform(0,1)
                    self.vertex_expected_occupancy[time][vertex_id]['low'] = 1-self.vertex_expected_occupancy[time][vertex_id]['high']
                    
        if vertex_id in self.vertex_expected_occupancy[time]:
            return True
        return False


    # get the occupancy of the vertices and edges
    def get_edge_expected_occupancy(self, time, edge_id):
        if time in self.edge_expected_occupancy:
            if edge_id in self.edge_expected_occupancy[time]:
                return self.edge_expected_occupancy[time][edge_id]
        return None
    
    def get_vertex_expected_occupancy(self, time, vertex_id):
        if time in self.vertex_expected_occupancy:
            if vertex_id in self.vertex_expected_occupancy[time]:
                return self.vertex_expected_occupancy[time][vertex_id]
        return None
    

    # get the traverse time of an edge
    def get_edge_traverse_time(self, edge_id):
        if edge_id in self.edge_traverse_time:
            return self.edge_traverse_time[edge_id]
        return None



    # remove the occupancy of the vertices and edges
    def remove_vertex_occupancy(self, vertex_id):
        self.vertex_occupancy = [vertex for vertex in self.vertex_occupancy if vertex['id'] != vertex_id]

    def remove_edge_occupancy(self, edge_id):
        self.edge_occupancy = [edge for edge in self.edge_occupancy if edge['id'] != edge_id]


    # save and load the occupancy map
    def save_occupancy_map(self, filename):
        with open(filename, 'w') as f:
            yaml.dump({'name': self.name, 
                       'vertex_limits': [{'id': vertex['id'], 'limit': vertex['limit']} for vertex in self.vertex_limits], 
                       'edge_limits': [{'id': edge['id'], 'limit': edge['limit']} for edge in self.edge_limits], 
                       'edge_traverse_time': self.edge_traverse_time, 
                       'vertex_occupancy': self.vertex_occupancy, 
                       'edge_occupancy': self.edge_occupancy, 
                       'vertex_expected_occupancy': self.vertex_expected_occupancy, 
                       'edge_expected_occupancy': self.edge_expected_occupancy}, f)
            
    def load_occupancy_map(self, filename):
        with open(filename, 'r') as f:
            data = yaml.load(f, Loader=yaml.FullLoader)
            self.name = data['name']
            self.vertex_limits = data['vertex_limits']
            self.edge_limits = data['edge_limits']
            self.edge_traverse_time = data['edge_traverse_time']
            self.vertex_occupancy = data['vertex_occupancy']
            self.edge_occupancy = data['edge_occupancy']
            self.vertex_expected_occupancy = data['vertex_expected_occupancy']
            self.edge_expected_occupancy = data['edge_expected_occupancy']



    # remove the occupancy of the vertices and edges
    def reset_occupancies(self):
        self.vertex_occupancy = {}
        self.edge_occupancy = {}
        self.vertex_expected_occupancy = {}
        self.edge_expected_occupancy = {}
