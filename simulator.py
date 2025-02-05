from MDP import MDP, State, Transition
from LrtdpTvmaAlgorithm import LrtdpTvmaAlgorithm
from OccupancyMap import OccupancyMap
import utils
import matplotlib.pyplot as plt

from cliff_predictor import CliffPredictor

class Simulator:

    def __init__(self, occupancy_map):
        self._occupancy_map = occupancy_map
        self._robot_min_speed = 0.6
        self._robot_max_speed = 1.2
        self._mdp = MDP(occupancy_map)


    def execute_step(self,state, action):
        # return self._mdp.compute_next_state(state, action)
        pass
        

    def simulate(self, start_time, initial_state, robot_min_speed = None, robot_max_speed = None ):
        completed = False
        time = start_time
        state = initial_state
        self._occupancy_map.predict_occupancies(time, 50)
        if robot_max_speed is not None:
            self._robot_max_speed = robot_max_speed
        if robot_min_speed is not None:
            self._robot_min_speed = robot_min_speed

        while not completed:
            # occupancies = self.get_current_occupancies(state)
            action = self.plan(state)
            if action is None:
                return False
            state = self.execute_step(state, action)
            if len(state.get_visited_vertices()) == len(self._occupancy_map.get_vertices_list()):
                completed = True
        return True

    def get_current_occupancies(self, state):
        current_time = state.get_time()
        occupancies = self._occupancy_map.get_occupancies(current_time)
        return occupancies
        

    def plan(self, current_state):
        lrtdp = LrtdpTvmaAlgorithm(occupancy_map=self._occupancy_map, 
                                   initial_state_name=current_state, 
                                   convergence_threshold=0.5, 
                                   time_bound_real=10000, 
                                   planner_time_bound=500, 
                                   vinitState=current_state)
        result = lrtdp.lrtdp_tvma()
        print("Result---------------------------------------------------")
        print(result)
        print(lrtdp.policy)
        print(current_state)
        # --current vertex:-- vertex1 --current time:-- 0 --already visited vertices:--  vertex1
        # --current vertex:-- vertex1 --current time:-- 0 --already visited vertices:--  vertex1
        print(lrtdp.policy.keys())
        print("lrtdp.policy[current_state]", lrtdp.policy[str(current_state)])
        if result and lrtdp.policy[str(current_state)] is None:
            return (True, None)
        elif not result:
            return (False, None)
        return (True, lrtdp.policy)


def create_medium_occupancy_map(occupancy_map):
    occupancy_map.set_name('medium_occupancy_map')
    
    # add the vertices
    assert occupancy_map.add_vertex_with_id("vertex1", 0, -11)
    assert occupancy_map.add_vertex_with_id("vertex2", 1, -4)
    assert occupancy_map.add_vertex_with_id("vertex3", 3, -6)
    assert occupancy_map.add_vertex_with_id("vertex4", 8, -11)
    assert occupancy_map.add_vertex_with_id("vertex5", 6, -2)
    assert not occupancy_map.add_vertex_with_id("vertex5", 5, -2)

    # add the edges
    assert occupancy_map.add_edge_with_id("edge1", "vertex1", "vertex2")
    assert occupancy_map.add_edge_with_id("edge9", "vertex2", "vertex1")
    assert occupancy_map.add_edge_with_id("edge2", "vertex1", "vertex3")
    assert occupancy_map.add_edge_with_id("edge10", "vertex3", "vertex1")
    assert occupancy_map.add_edge_with_id("edge3", "vertex1", "vertex4")
    assert occupancy_map.add_edge_with_id("edge11", "vertex4", "vertex1")
    assert occupancy_map.add_edge_with_id("edge4", "vertex2", "vertex3")
    assert occupancy_map.add_edge_with_id("edge12", "vertex3", "vertex2")
    assert occupancy_map.add_edge_with_id("edge5", "vertex3", "vertex4")
    assert occupancy_map.add_edge_with_id("edge13", "vertex4", "vertex3")
    assert occupancy_map.add_edge_with_id("edge6", "vertex2", "vertex5")
    assert occupancy_map.add_edge_with_id("edge14", "vertex5", "vertex2")
    assert occupancy_map.add_edge_with_id("edge7", "vertex3", "vertex5")
    assert occupancy_map.add_edge_with_id("edge15", "vertex5", "vertex3")
    assert occupancy_map.add_edge_with_id("edge8", "vertex4", "vertex5")
    assert occupancy_map.add_edge_with_id("edge16", "vertex5", "vertex4")

    # assert not occupancy_map.add_edge_with_id("edge8", "vertex4", "vertex2")
    # assert not occupancy_map.add_edge_with_id("edge9", "vertex4", "vertex10")
    # assert not occupancy_map.add_edge_with_id("edge10", "vertex10", "vertex5")
    
    # add limits and edge traverse time
    for vertex in occupancy_map.get_vertices_list():
        assert occupancy_map.add_vertex_limit(vertex.get_id(), 3)
        assert not occupancy_map.add_vertex_limit(vertex.get_id(), 3)
    
    for edge in occupancy_map.get_edges_list():
        assert occupancy_map.add_edge_limit(edge.get_id(), 3)
        assert not occupancy_map.add_edge_limit(edge.get_id(), 3)
        # print(edge.get_start())
  
    

    # i = 0
    # for vertex in occupancy_map.get_vertices_list():
    #     assert occupancy_map.add_vertex_occupancy(vertex.get_id(), 0.6, 0.4, i)
    #     assert not occupancy_map.add_vertex_occupancy(vertex.get_id(), 0.6, 0.4, i)
    # for edge in occupancy_map.get_edges_list():
    #     assert occupancy_map.add_edge_occupancy(edge.get_id(), 0.6, 0.4, i)
    #     assert not occupancy_map.add_edge_occupancy(edge.get_id(), 0.6, 0.4, i)
    # for edge in occupancy_map.get_edges_list():
    #     assert occupancy_map.get_edge_expected_occupancy(i, edge.get_id()) == {'high': 0.6, 'low': 0.4}

    for edge in occupancy_map.get_edges_list():
        # print(occupancy_map.get_edge_traverse_time(edge.get_id()))
        assert occupancy_map.get_edge_traverse_time(edge.get_id()) == None
        assert occupancy_map.add_edge_traverse_time(edge.get_id(), 'high', 2 * occupancy_map.get_vertex_distance(edge.get_start(), edge.get_end()))
        assert occupancy_map.add_edge_traverse_time(edge.get_id(), 'low',  occupancy_map.get_vertex_distance(edge.get_start(), edge.get_end()))
        assert occupancy_map.get_edge_traverse_time(edge.get_id()) == {'high': 2 * occupancy_map.get_vertex_distance(edge.get_start(), edge.get_end()), 'low': occupancy_map.get_vertex_distance(edge.get_start(), edge.get_end())}
    assert not occupancy_map.add_edge_traverse_time("edge1", 'high', 20 )
    # for edge in occupancy_map.get_edges_list():
        
    #     print(edge.get_id(), occupancy_map.get_edge_traverse_time(edge.get_id())['high'] * occupancy_map.get_edge_expected_occupancy(i, edge.get_id())['high'] + occupancy_map.get_edge_traverse_time(edge.get_id())['low'] * occupancy_map.get_edge_expected_occupancy(i, edge.get_id())['low'])




if __name__ == "__main__":
    map_file = "CLiFF_LHMP/maps/iit.png"
    mod_file = "CLiFF_LHMP/MoDs/iit/iit_cliff.csv"
    # ground_truth_data_file = "dataset/iit/iit.csv"
    # result_file = "iit_results.csv"
    observed_tracklet_length = 4
    start_length = 0
    planning_horizon = 50
    beta = 1
    sample_radius = 0.5
    delta_t = 1
    method = utils.Method.MoD
    # method = utils.Method.CVM
    dataset = utils.Dataset.IIT
    fig_size = [-12.83, 12.83, -12.825, 12.825]
    predictor = CliffPredictor(dataset, map_file, mod_file, observed_tracklet_length, start_length, planning_horizon, beta, sample_radius, delta_t, method, fig_size)
    occupancy_map = OccupancyMap(predictor)
    create_medium_occupancy_map(occupancy_map)
    simulator = Simulator(occupancy_map)
    initial_state_name = "vertex1"
    initial_state = State(initial_state_name, 
                          0, 
                          (occupancy_map.find_vertex_from_id(initial_state_name).get_posx(), 
                           occupancy_map.find_vertex_from_id(initial_state_name).get_posy()), 
                           set([initial_state_name]))
    simulator.simulate(0, initial_state)