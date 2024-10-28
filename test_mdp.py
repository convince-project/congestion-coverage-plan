from OccupancyMap import OccupancyMap
from MDP import MDP, State, Transition
from test_occupancy_map import create_small_map, test_occupancy_map


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
    assert mdp.get_possible_actions(initial_state) == set(["vertex2", "vertex3", "vertex4", "wait"])
    assert not mdp.solved(initial_state)
    transitions = mdp.get_possible_transitions(initial_state)
    assert len(transitions) == 7


    # for state in mdp.get_possible_next_states(initial_state):
    #     print(state.get_vertex(), state.get_time(), state.get_position(), state.get_visited_vertices())
    next_states = set([State("vertex1", 5, (occupancy_map.find_vertex_from_id("vertex1").get_posx(), occupancy_map.find_vertex_from_id("vertex1").   
                                                           get_posy()), [initial_state_name]),
                                                           State("vertex2", 10, (occupancy_map.find_vertex_from_id("vertex2").get_posx(), occupancy_map.find_vertex_from_id("vertex2").
                                                           get_posy()), [initial_state_name, "vertex2"]), 
                                                           State("vertex2", 20, (occupancy_map.find_vertex_from_id("vertex2").get_posx(), occupancy_map.find_vertex_from_id("vertex2").
                                                           get_posy()), [initial_state_name, "vertex2"]), 
                                                           State("vertex3", 10, (occupancy_map.find_vertex_from_id("vertex3").get_posx(), occupancy_map.find_vertex_from_id("vertex3").get_posy()), [initial_state_name, "vertex3"]), 
                                                           State("vertex3", 20, (occupancy_map.find_vertex_from_id("vertex3").get_posx(), occupancy_map.find_vertex_from_id("vertex3").get_posy()), [initial_state_name, "vertex3"]), 
                                                           State("vertex4", 10, (occupancy_map.find_vertex_from_id("vertex4").get_posx(), occupancy_map.find_vertex_from_id("vertex4").get_posy()), [initial_state_name, "vertex4"]),
                                                           State("vertex4", 20, (occupancy_map.find_vertex_from_id("vertex4").get_posx(), occupancy_map.find_vertex_from_id("vertex4").get_posy()), [initial_state_name, "vertex4"])])
    # print("============================ possible next states ============================")

    # assert mdp.get_possible_next_states(initial_state) == next_states
    transitions_vertex2 = mdp.get_possible_transitions_from_action(initial_state, "vertex2")
    
    # for transition in transitions_vertex2:
        # assert transition.get_action() == "vertex2"
        # assert transition.get_start() == "vertex1"
        # assert transition.get_end() == "vertex2"
        # assert transition.get_occupancy_level() in ["high", "low"]
        # assert transition.get_cost() in [10, 20]
        
    # print("============================ possible transitions from action ============================")
        









    # print("============================ possible transitions ============================")
    # for transition in mdp.calculate_transitions(initial_state):
    #     print(transition.get_action(), transition.get_start(), transition.get_end(), transition.get_occupancy_level(), transition.get_cost(), transition.get_probability())

    # print("============================ transition from action ============================")
    # for transition in mdp.calculate_transitions_from_action(initial_state, "vertex4"):
    #     print(transition.get_action(), transition.get_start(), transition.get_end(), transition.get_occupancy_level(), transition.get_cost(), transition.get_probability())
    # print("============================ compute transition ============================")
    # transition_high = mdp.compute_transition(initial_state, occupancy_map.find_edge_from_id("edge1"), "high")
    # transition_low = mdp.compute_transition(initial_state, occupancy_map.find_edge_from_id("edge1"), "low")
    # print(transition_high.get_action(), transition_high.get_start(), transition_high.get_end(), transition_high.get_occupancy_level(), transition_high.get_cost(), transition_high.get_probability())
    # print(transition_low.get_action(), transition_low.get_start(), transition_low.get_end(), transition_low.get_occupancy_level(), transition_low.get_cost(), transition_low.get_probability())
    # possible_next_states = mdp.get_possible_next_states(initial_state)
    # print("============================ possible next states ============================")
    # for state in possible_next_states:
    #     print(state.get_vertex(), state.get_time(), state.get_position(), state.get_visited_vertices())
    # vertrices_names = [vertex.get_id() for vertex in occupancy_map.get_vertices_list()]
    # print("============================ goal ============================")
    # goal_state = State("vertex9",
    #                       0,
    #                       (occupancy_map.find_vertex_from_id("vertex9").get_posx(),
    #                        occupancy_map.find_vertex_from_id("vertex9").get_posy()),
    #                       vertrices_names)
    # print(mdp.solved(initial_state))
    # print(mdp.solved(goal_state))



if __name__ == "__main__":
    occupancy_map = OccupancyMap()
    test_occupancy_map(occupancy_map)
    test_mdp(occupancy_map)