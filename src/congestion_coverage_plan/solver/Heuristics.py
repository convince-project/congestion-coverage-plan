from scipy.sparse import csr_array
from scipy.sparse.csgraph import shortest_path
from congestion_coverage_plan.utils import Logger
class Heuristics():

    def __init__(self, 
                 occupancy_map, 
                 mdp,
                 heuristic_function="mst_shortest_path",
                 logger = None):
        self.occupancy_map = occupancy_map
        self._mdp = mdp
        self.logger = logger if logger is not None else Logger()
        self.shortest_paths_matrix = self.calculate_shortest_path_matrix()
        if heuristic_function == "madama_experiments":
            self.heuristic_function = self.heuristic_experiments
        else:
            # self.logger.log("Heuristic function not recognized, using default madama_experiments", Logger.WARNING)
            self.heuristic_function = self.heuristic_experiments
    ### HEURISTIC HELPERS

    def calculate_shortest_path(self, vertex1, vertex2):
        vertex1_position = sorted(self.occupancy_map.get_vertices().keys()).index(vertex1)
        vertex2_position = sorted(self.occupancy_map.get_vertices().keys()).index(vertex2)
        return self.shortest_paths_matrix[vertex1_position][vertex2_position]


    def calculate_shortest_path_matrix(self):
        mst_matrix = self.create_map_matrix()
        sp = shortest_path(mst_matrix)
        return sp 


    def create_map_matrix(self):
        vertices = sorted(self.occupancy_map.get_vertices().keys())
        mst_matrix = []
        for vertex in vertices:
            mst_matrix_line = []
            for vertex2 in vertices:
                if vertex == vertex2:
                    mst_matrix_line.append(0)
                elif self.occupancy_map.find_edge_from_position(vertex, vertex2) is not None:
                    edge_id = self.occupancy_map.find_edge_from_position(vertex, vertex2).get_id()
                    mst_matrix_line.append(self.occupancy_map.get_edge_traverse_time(edge_id)['zero'])
                else:
                    mst_matrix_line.append(99999999)
            mst_matrix.append(mst_matrix_line)
        return csr_array(mst_matrix)


    ### HEURISTIC FUNCTIONS

    def heuristic_experiments(self, state):
        if self._mdp.solved(state):
            return 0
        goal_vertex = self.occupancy_map.find_vertex_from_id(sorted(self.occupancy_map.get_final_goal_vertices())[0])
        current_vertex = self.occupancy_map.find_vertex_from_id(state.get_vertex())
        shortest_path = self.calculate_shortest_path(state.get_vertex(), goal_vertex.get_id())
        remaining_pois_to_explain = len(self.occupancy_map.get_pois_set()) - len(state.get_pois_explained())
        # get current vertex poi
        penalty = 0
        current_vertex_poi = current_vertex.get_poi_number() 
        if current_vertex_poi is not None:
            for poi_number in range(1, current_vertex_poi):
                if poi_number not in state.get_pois_explained():
                    penalty = penalty + 99999
        # increase cost if the pois before are not explained
        
        # check if all the states are connected
        cost = shortest_path + (remaining_pois_to_explain * 20) + penalty
        return cost if cost is not None else 9999999
