# topological map representation of a location.
# The topological map is a dictionary with the following format:
# { 
#   'name': 'map_name',
#   'vertices': [{'id': uuidvertex1, 'posx': x1, 'posy': y1}, {'id': uuidvertex2, 'posx': x2, 'posy': y2},, ...],
#   'edges': [{'id': uuidedge1, 'start': uuidvertex1, 'end': uuidvertex2}, {'id': uuidedge2, 'start': uuidvertex2, 'end': uuidvertex3}, ...],
#   'goal_vertices': [uuidvertex1, uuidvertex2, ...]
# }
# The topological map can be saved and loaded to/from a yaml file.
# The topological map can be visualized using the function plot_topological_map.

import yaml
import uuid
import matplotlib.pyplot as plt


class Vertex:
    def __init__(self, id, posx, posy):
        self._id = id
        self._posx = posx
        self._posy = posy

    def __eq__(self, other):
        return self._id == other.get_id() and self._posx == other.get_posx() and self._posy == other.get_posy()

    # create getters for the class
    def get_id(self):
        return self._id
    
    def get_posx(self):
        return self._posx
    
    def get_posy(self):
        return self._posy


class Edge:
    def __init__(self, id, start, end):
        self._id = id
        self._start = start
        self._end = end

    def __eq__(self, other):
        return self._id == other.get_id() and self._start == other.get_start() and self._end == other.get_end()
    
    # create getters for the class
    def get_id(self):
        return self._id
    
    def get_start(self):
        return self._start
    
    def get_end(self):
        return self._end


class TopologicalMap:
    def __init__(self):
        self.name = ""
        self.vertices = []
        self.edges = []
        self.goal_vertices = []
    

    ## GETTERS

    def get_vertices_list(self):
        return self.vertices
    
    def get_edges_list(self):   
        return self.edges
    
    def get_goal_vertices_list(self):
        return self.goal_vertices

    def get_name(self):
        return self.name
    
    ## Functions for setting the topological map

    ### Vertices functions
    def add_vertex(self, posx, posy):
        # check if a vertex already exists at the same position
        id = str(uuid.uuid4())
        return self.add_vertex_with_id(id, posx, posy)

    def add_vertex_with_id(self, vertex_id, posx, posy):
        # check if a vertex already exists at the same position
        for vertex in self.vertices:
            if vertex.get_id() == vertex_id or (vertex.get_posx() == posx and vertex.get_posy() == posy):
                return False
        # add the vertex
        self.vertices.append(Vertex(vertex_id, posx, posy))
        return True

    ### Edges functions
    def add_edge(self, start_id, end_id):
        # check if the vertices exist
        id = str(uuid.uuid4())
        return self.add_edge_with_id(id, start_id, end_id)
    
    def add_edge_with_id(self, edge_id, start_id, end_id):
        # check if the vertices exist
        if self.find_vertex_from_id(start_id) is None and self.find_vertex_from_id(end_id) is None:
            return False
        # check if the edge already exists
        for edge in self.edges:
            if edge.get_id() == edge_id or (edge.get_start() == start_id and edge.get_end() == end_id):
                return False
        self.edges.append(Edge(edge_id, start_id, end_id))
        return True
    
    def add_edge_with_id_and_positions(self, edge_id, start_posx, start_posy, end_posx, end_posy):
        start = self.find_vertex_from_position(start_posx, start_posy)
        end = self.find_vertex_from_position(end_posx, end_posy)
        if start is not None and end is not None:
            return self.add_edge_with_id(edge_id, start.get_id(), end.get_id())
        return False

    def add_edge_from_positions(self, start_posx, start_posy, end_posx, end_posy):
        id = str(uuid.uuid4())
        return self.add_edge_with_id_and_positions(id, start_posx, start_posy, end_posx, end_posy)

    ### Goal vertices functions
    def set_vertex_as_goal_from_position(self, posx, posy):
        # check if the vertex exists
        vertex = self.find_vertex_from_position(posx, posy)
        if vertex is not None:
            self.goal_vertices.append(vertex)
            return True
        return False

    def is_goal_vertex(self, vertex_id):
        return vertex_id in self.goal_vertices

    def set_vertex_as_goal_from_id(self, vertex_id):
        # check if the vertex exists
        for vertex in self.vertices:
            if vertex.get_id() == vertex_id:
                self.goal_vertices.append(vertex)
                return True
        return False


    ## Functions for finding elements in the topological map
    def find_vertex_from_position(self, posx, posy):
        for vertex in self.vertices:
            if vertex.get_posx() == posx and vertex.get_posy() == posy:
                return vertex
        return None
    
    def find_vertex_from_id(self, vertex_id):
        for vertex in self.vertices:
            if vertex.get_id() == vertex_id:
                return vertex
        return None
    
    def find_edge_from_position(self, start, end):
        for edge in self.edges:
            if edge.get_start() == start and edge.get_end() == end:
                return edge.get_id()
        return None
    
    def find_edge_from_id(self, edge_id):
        for edge in self.edges:
            if edge.get_id() == edge_id:
                return edge
        return None
    

    ### Functions for saving and loading the topological map
    def save_topological_map(self, filename):
        with open(filename, 'w') as f:
            yaml.dump({'name': self.name, 
                       'vertices': [{'id': vertex.get_id(), 
                                     'posx': vertex.get_posx(), 
                                     'posy': vertex.get_posy()} for vertex in self.vertices], 
                        'edges': [{'id': edge.get_id(), 
                                   'start': edge.get_start(), 
                                   'end': edge.get_end()} for edge in self.edges], 
                        'goal_vertices': [{'id': vertex.get_id(), 
                                           'posx': vertex.get_posx(), 
                                           'posy': vertex.get_posy()} for vertex in self.goal_vertices]}, f)
    
    def load_topological_map(self, filename):
        with open(filename, 'r') as f:
            data = yaml.load(f, Loader=yaml.FullLoader)
            self.name = data['name']
            self.vertices = [Vertex(vertex['id'], vertex['posx'], vertex['posy']) for vertex in data['vertices']]
            self.edges = [Edge(edge['id'], edge['start'], edge['end']) for edge in data['edges']]
            self.goal_vertices = [Vertex(vertex['id'], vertex['posx'], vertex['posy']) for vertex in data['goal_vertices']]
    
    def plot_topological_map(self):
        fig, ax = plt.subplots()
        for edge in self.edges:
            start = None
            end = None
            for vertex in self.vertices:
                if vertex.get_id() == edge.get_start():
                    start = vertex
                elif vertex.get_id() == edge.get_end():
                    end = vertex
            if start is not None and end is not None:
                ax.plot([start.get_posx(), end.get_posx()], [start.get_posy(), end.get_posy()], 'pink')
                # plot also the id of the edge
                ax.text(x = (start.get_posx() + end.get_posx()) / 2, y = (start.get_posy() + end.get_posy()) / 2,  s = edge.get_id(), color = "blue")
        for vertex in self.vertices:
            if vertex in self.goal_vertices:
                ax.plot(vertex.get_posx(), vertex.get_posy(), 'bo')
            else:
                ax.plot(vertex.get_posx(), vertex.get_posy(), 'ro')
            ax.text(x = vertex.get_posx(), y = vertex.get_posy(), s = vertex.get_id(), color = "black")
        plt.show()



# Example of usage
def test():
    topological_map = TopologicalMap()
    topological_map.add_vertex(0, 0)
    topological_map.add_vertex(1, 1)
    topological_map.add_vertex(2, 2)
    topological_map.add_edge_from_positions(0, 0, 1, 1)
    topological_map.add_edge_from_positions(1, 1, 2, 2)
    topological_map.set_vertex_as_goal_from_position(2, 2)
    topological_map.save_topological_map('prova.yaml')
    topological_map.load_topological_map('prova.yaml')
    topological_map.plot_topological_map()


if __name__ == '__main__':
    test()