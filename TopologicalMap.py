# topological map representation of a location.
# The topological map is a dictionary with the following format:
# { 
#   'name': 'map_name',
#   'nodes': [{'id': uuidnode1, 'posx': x1, 'posy': y1}, {'id': uuidnode2, 'posx': x2, 'posy': y2},, ...],
#   'edges': [{'id': uuidedge1, 'start': uuidnode1, 'end': uuidnode2}, {'id': uuidedge2, 'start': uuidnode2, 'end': uuidnode3}, ...],
#   'terminal_nodes': [uuidnode1, uuidnode2, ...]
# }
# The topological map can be saved and loaded to/from a yaml file.
# The topological map can be visualized using the function plot_topological_map.

import yaml
import uuid
import matplotlib.pyplot as plt

class TopologicalMap:
    def __init__(self):
        self.topological_map = {'name': "", 'nodes': [], 'edges': [], 'terminal_nodes': []}
    
    def set_name(self, name):
        self.topological_map['name'] = name

    def add_node(self, posx, posy):
        # check if a node already exists at the same position
        for node in self.topological_map['nodes']:
            if node['posx'] == posx and node['posy'] == posy:
                return False
        # add the node
        node = {'id': str(uuid.uuid4()), 'posx': posx, 'posy': posy}
        self.topological_map['nodes'].append(node)
        return True
    
    def get_nodes_list(self):
        return self.topological_map['nodes']
    
    def get_edges_list(self):   
        return self.topological_map['edges']
    
    def get_terminal_nodes_list(self):
        return self.topological_map['terminal_nodes']

    def add_node_with_id(self, node_id, posx, posy):
        # check if a node already exists at the same position
        # print (self.topological_map)
        for node in self.topological_map['nodes']:
            if node['posx'] == posx and node['posy'] == posy:
                return False
        # add the node
        node = {'id': node_id, 'posx': posx, 'posy': posy}
        self.topological_map['nodes'].append(node)
        return True
    
    def add_edge_from_positions(self, start_posx, start_posy, end_posx, end_posy):
        start = self.find_node(start_posx, start_posy)
        end = self.find_node(end_posx, end_posy)
        if start is not None and end is not None:
            return self.add_edge(start, end)
        return False
    
    def is_terminal_node(self, node_id):
        return node_id in self.topological_map['terminal_nodes']

    def add_terminal_node(self, posx, posy):
        # check if the node exists
        node_id = self.find_node(posx, posy)
        if node_id is not None:
            self.topological_map['terminal_nodes'].append(node_id)
            return True
        return False
    
    def add_terminal_node_with_id(self, node_id):
        # check if the node exists
        if node_id in [node['id'] for node in self.topological_map['nodes']]:
            self.topological_map['terminal_nodes'].append(node_id)
            return True
        return False

    def add_edge(self, start, end):
        # check if the nodes exist
        if start not in [node['id'] for node in self.topological_map['nodes']] and end not in [node['id'] for node in self.topological_map['nodes']]:
            return False
        edge = {'id': str(uuid.uuid4()), 'start': start, 'end': end}
        self.topological_map['edges'].append(edge)
        return True
    
    def add_edge_with_id(self, edge_id, start, end):
        # check if the nodes exist
        if start not in [node['id'] for node in self.topological_map['nodes']] and end not in [node['id'] for node in self.topological_map['nodes']]:
            return False
        edge = {'id': edge_id, 'start': start, 'end': end}
        self.topological_map['edges'].append(edge)
        return True
    
    def add_edge_with_id_and_positions(self, edge_id, start_posx, start_posy, end_posx, end_posy):
        start = self.find_node(start_posx, start_posy)
        end = self.find_node(end_posx, end_posy)
        if start is not None and end is not None:
            return self.add_edge_with_id(edge_id, start, end)
        return False
    
    def find_node(self, posx, posy):
        for node in self.topological_map['nodes']:
            if node['posx'] == posx and node['posy'] == posy:
                return node['id']
        return None
    
    def find_edge(self, start, end):
        for edge in self.topological_map['edges']:
            if edge['start'] == start and edge['end'] == end:
                return edge['id']
        return None

    def remove_node(self, node_id):
        # remove the node
        self.topological_map['nodes'] = [node for node in self.topological_map['nodes'] if node['id'] != node_id]
        # remove the edges
        self.topological_map['edges'] = [edge for edge in self.topological_map['edges'] if edge['start'] != node_id and edge['end'] != node_id]

    def remove_edge(self, edge_id):
        self.topological_map['edges'] = [edge for edge in self.topological_map['edges'] if edge['id'] != edge_id]
    
    def save_topological_map(self, filename):
        with open(filename, 'w') as f:
            yaml.dump(self.topological_map, f)
    
    def load_topological_map(self, filename):
        with open(filename, 'r') as f:
            self.topological_map = yaml.load(f, Loader=yaml.FullLoader)
    
    def plot_topological_map(self):
        fig, ax = plt.subplots()
        for edge in self.topological_map['edges']:
            start = None
            end = None
            for node in self.topological_map['nodes']:
                if node['id'] == edge['start']:
                    start = node
                if node['id'] == edge['end']:
                    end = node
            if start is not None and end is not None:
                ax.plot([start['posx'], end['posx']], [start['posy'], end['posy']], 'k-')
                # plot also the id of the edge
                ax.text((start['posx'] + end['posx']) / 2, (start['posy'] + end['posy']) / 2, edge['id'])
        for node in self.topological_map['nodes']:
            if node['id'] in self.topological_map['terminal_nodes']:
                ax.plot(node['posx'], node['posy'], 'bo')
            else:
                ax.plot(node['posx'], node['posy'], 'ro')
            ax.text(node['posx'], node['posy'], node['id'])
        plt.show()


# def test_topological_map():
#     topological_map = TopologicalMap()
#     map_name = 'test_map'
#     topological_map.set_name(map_name)
#     topological_map.add_node(0, 0)
#     topological_map.add_node(1, 0)
#     topological_map.add_node(0, 1)
#     topological_map.add_node(1, 1)
#     topological_map.add_node(4, 1)
#     topological_map.add_node(1, 4)
#     topological_map.add_node(3, 2)
#     topological_map.add_node(1, 2)
#     topological_map.add_node(4, 2)

#     topological_map.add_edge(topological_map.find_node(0, 0), topological_map.find_node(1, 0))
#     topological_map.add_edge(topological_map.find_node(1, 0), topological_map.find_node(0, 1))
#     topological_map.add_edge(topological_map.find_node(0, 0), topological_map.find_node(1, 1))
#     topological_map.add_edge(topological_map.find_node(1, 1), topological_map.find_node(2, 2))
#     topological_map.add_edge(topological_map.find_node(1, 1), topological_map.find_node(1, 4))
#     topological_map.add_edge(topological_map.find_node(1, 4), topological_map.find_node(4, 1))
#     topological_map.add_edge(topological_map.find_node(4, 1), topological_map.find_node(4, 2))
#     topological_map.add_edge(topological_map.find_node(4, 2), topological_map.find_node(3, 2))
#     topological_map.add_edge(topological_map.find_node(3, 2), topological_map.find_node(1, 2))
#     topological_map.add_edge(topological_map.find_node(1, 2), topological_map.find_node(1, 0))
    
    

#     topological_map.plot_topological_map()

# if __name__ == '__main__':
#     test_topological_map()
