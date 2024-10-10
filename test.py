from OccupancyMap import OccupancyMap
from MDP import MDP, State, Transition
from LrtdpTvmaAlgorithm import LrtdpTvmaAlgorithm
import math
import random

        
def create(occupancy_map):
    occupancy_map.set_name('occupancy_map')
    # add a vertex to the topological map
    occupancy_map.add_vertex_with_id("vertex1", 0, 0)
    occupancy_map.add_vertex_with_id("vertex2", 2, 5)
    occupancy_map.add_vertex_with_id("vertex3", 5, 5)
    occupancy_map.add_vertex_with_id("vertex4", 6, 2)
    occupancy_map.add_vertex_with_id("vertex5", 9, 2)
    occupancy_map.add_vertex_with_id("vertex6", 5, 9)
    occupancy_map.add_vertex_with_id("vertex7", 7, 8)
    occupancy_map.add_vertex_with_id("vertex8", 9, 6)
    occupancy_map.add_vertex_with_id("vertex9", 11, 11)
    occupancy_map.add_vertex_with_id("vertex10", 11, 9)
    occupancy_map.set_vertex_as_goal_from_id("vertex9")
    occupancy_map.set_vertex_as_goal_from_id("vertex10")
    # for each vertex add the occupancy
    occupancy_map.add_edge_with_id("edge1", "vertex1", "vertex2")
    occupancy_map.add_edge_with_id("edge2", "vertex1", "vertex3")
    occupancy_map.add_edge_with_id("edge3", "vertex1", "vertex4")
    occupancy_map.add_edge_with_id("edge4", "vertex1", "vertex5")
    occupancy_map.add_edge_with_id("edge5", "vertex2", "vertex3")
    occupancy_map.add_edge_with_id("edge6", "vertex2", "vertex6")
    occupancy_map.add_edge_with_id("edge7", "vertex2", "vertex7")
    occupancy_map.add_edge_with_id("edge8", "vertex3", "vertex4")
    occupancy_map.add_edge_with_id("edge9", "vertex3", "vertex6")
    occupancy_map.add_edge_with_id("edge10", "vertex3", "vertex7")
    occupancy_map.add_edge_with_id("edge11", "vertex3", "vertex8")
    occupancy_map.add_edge_with_id("edge12", "vertex4", "vertex5")
    occupancy_map.add_edge_with_id("edge13", "vertex4", "vertex7")
    occupancy_map.add_edge_with_id("edge14", "vertex4", "vertex8")
    occupancy_map.add_edge_with_id("edge15", "vertex5", "vertex8")    
    occupancy_map.add_edge_with_id("edge15", "vertex5", "vertex10")    
    occupancy_map.add_edge_with_id("edge16", "vertex5", "vertex9")    
    occupancy_map.add_edge_with_id("edge17", "vertex6", "vertex7")    
    occupancy_map.add_edge_with_id("edge18", "vertex6", "vertex9")    
    occupancy_map.add_edge_with_id("edge19", "vertex7", "vertex8")    
    occupancy_map.add_edge_with_id("edge20", "vertex7", "vertex9")    
    occupancy_map.add_edge_with_id("edge20", "vertex7", "vertex10")    
    occupancy_map.add_edge_with_id("edge21", "vertex8", "vertex9")   
    occupancy_map.add_edge_with_id("edge21", "vertex8", "vertex10")   

    

    occupancy_map.calculate_current_vertices_occupancy()
    occupancy_map.calculate_current_edges_occupancy()

    for vertex in occupancy_map.get_vertices_list():
        occupancy_map.add_vertex_limit(vertex.get_id(), 3)
    for edge in occupancy_map.get_edges_list():
        occupancy_map.add_edge_limit(edge.get_id(), 3)
        occupancy_map.add_edge_traverse_time(edge.get_id(), 'high', 20 + math.floor(random.random() * 5))
        occupancy_map.add_edge_traverse_time(edge.get_id(), 'low', 10 + math.floor(random.random() * 5))

    for i in range(1,30):
        occupancy_map.predict_occupancies(i)


def test_mdp(occupancy_map):
    # print(occupancy_map.get_vertices_list())
    # print(occupancy_map.get_edges_list())   
    mdp = MDP(occupancy_map)
    initial_state_name = "vertex1"
    initial_state = State(initial_state_name, 
                          0, 
                          (occupancy_map.find_vertex_from_id(initial_state_name).get_posx(), 
                           occupancy_map.find_vertex_from_id(initial_state_name).get_posy()), 
                           [initial_state_name])
    print("============================ possible actions ============================")
    print(mdp.get_possible_actions(initial_state))
    print("============================ possible transitions ============================")
    for transition in mdp.calculate_transitions(initial_state):
        print(transition.get_action(), transition.get_start(), transition.get_end(), transition.get_occupancy_level(), transition.get_cost(), transition.get_probability())

    print("============================ transition from action ============================")
    for transition in mdp.calculate_transitions_from_action(initial_state, "vertex4"):
        print(transition.get_action(), transition.get_start(), transition.get_end(), transition.get_occupancy_level(), transition.get_cost(), transition.get_probability())
    print("============================ compute transition ============================")
    transition_high = mdp.compute_transition(initial_state, occupancy_map.find_edge_from_id("edge1"), "high")
    transition_low = mdp.compute_transition(initial_state, occupancy_map.find_edge_from_id("edge1"), "low")
    print(transition_high.get_action(), transition_high.get_start(), transition_high.get_end(), transition_high.get_occupancy_level(), transition_high.get_cost(), transition_high.get_probability())
    print(transition_low.get_action(), transition_low.get_start(), transition_low.get_end(), transition_low.get_occupancy_level(), transition_low.get_cost(), transition_low.get_probability())
    possible_next_states = mdp.get_possible_next_states(initial_state)
    print("============================ possible next states ============================")
    for state in possible_next_states:
        print(state.get_vertex(), state.get_time(), state.get_position(), state.get_visited_vertices())
    vertrices_names = [vertex.get_id() for vertex in occupancy_map.get_vertices_list()]
    print("============================ goal ============================")
    goal_state = State("vertex9",
                          0,
                          (occupancy_map.find_vertex_from_id("vertex9").get_posx(),
                           occupancy_map.find_vertex_from_id("vertex9").get_posy()),
                          vertrices_names)
    print(mdp.solved(initial_state))
    print(mdp.solved(goal_state))




def test_occupancy_map(occupancy_map):
    # create a topological map
    # topological_map = TopologicalMap()
    # create an occupancy map
    # occupancy_map = OccupancyMap(topological_map)\
    # occupancy_map = OccupancyMap()
    create(occupancy_map)
    # save the occupancy map
    occupancy_map.save_occupancy_map('data/occupancy_map.yaml')
    #save the topological map
    occupancy_map.save_topological_map('data/topological_map.yaml')
    # set the name of the occupancy map
    occupancy_map.load_topological_map('data/topological_map.yaml')
    occupancy_map.load_occupancy_map('data/occupancy_map.yaml')
    # occupancy_map.plot_topological_map()
    # save the occupancy map

if __name__ == "__main__":
    occupancy_map = OccupancyMap()
    test_occupancy_map(occupancy_map)
    occupancy_map.load_topological_map('data/topological_map.yaml')
    occupancy_map.load_occupancy_map('data/occupancy_map.yaml')
    test_mdp(occupancy_map)

    # lrtdp = LrtdpTvmaAlgorithm('occupancy_map', 'vertex1', 0.01, 30000)
    # lrtdp.lrtdp_tvma()