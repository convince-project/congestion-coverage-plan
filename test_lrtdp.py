from OccupancyMap import OccupancyMap
from MDP import MDP, State, Transition
from test_occupancy_map import test_minimal_occupancy_map,  test_small_occupancy_map, test_medium_occupancy_map
from test_mdp import test_mdp
from LrtdpTvmaAlgorithm import LrtdpTvmaAlgorithm


def test_lrtdp(occupancy_map):
    
    initial_state_name = "vertex1"
    visited_set = set()
    visited_set.add(initial_state_name)
    # print(visited_set)
    initial_state = State(initial_state_name, 
                          0, 
                          (occupancy_map.find_vertex_from_id(initial_state_name).get_posx(), 
                           occupancy_map.find_vertex_from_id(initial_state_name).get_posy()), 
                           set([initial_state_name]))
    lrtdp = LrtdpTvmaAlgorithm(occupancy_map=occupancy_map, initial_state_name=initial_state_name, convergence_threshold=0.5, time_bound_real=10000, planner_time_bound=50)
    assert lrtdp.occupancy_map == occupancy_map
    # assert lrtdp.mdp == mdp
    assert lrtdp.vinitState == initial_state
    assert lrtdp.vinitStateName == initial_state_name
    # assert lrtdp.timeBoundGlobal == 500
    assert lrtdp.policy == {}
    assert lrtdp.valueFunction == {}
    assert lrtdp.solved_set == set()
    # assert lrtdp.value == {}
    assert not lrtdp.solved(initial_state)
    assert lrtdp.get_value(initial_state) == 0
    # print(lrtdp.calculate_Q(initial_state, "vertex2"))
    # assert lrtdp.residual(initial_state) == 0
    # for action in lrtdp.mdp.get_possible_actions(initial_state):
    #     print(action)
    #     print(lrtdp.calculate_Q(initial_state, action))
    # argmin_q = lrtdp.calculate_argmin_Q(initial_state)
    # print(argmin_q)
    # print(argmin_q[1])
    # assert argmin_q == (5.0, State(initial_state.get_vertex(), initial_state.get_time(), initial_state.get_position(), initial_state.get_visited_vertices()), "wait")
    lrtdp.update(initial_state)
    # assert lrtdp.get_value(initial_state) == 5.0
    # print(lrtdp.get_value(initial_state))
    # print(lrtdp.residual(initial_state))
    # lrtdp.lrtdp_tvma_trial(initial_state, 0.1, 400)
    # lrtdp.lrtdp_tvma_trial(initial_state, 0.1, 400)
    # lrtdp.lrtdp_tvma_trial(initial_state, 0.1, 400)
    # lrtdp.lrtdp_tvma_trial(initial_state, 0.1, 400)
    # lrtdp.lrtdp_tvma_trial(initial_state, 0.1, 400)
    # lrtdp.lrtdp_tvma_trial(initial_state, 0.1, 400)
    # lrtdp.lrtdp_tvma_trial(initial_state, 0.1, 400)


    lrtdp.lrtdp_tvma()

    
    print("FINAL POLICY:")
    for state in lrtdp.policy:
        # print("State: ", state)
        print(lrtdp.policy[state][1], "action", lrtdp.policy[state][2])
    # print ("FINAL VALUE FUNCTION", lrtdp.valueFunction)
    


if __name__ == "__main__":
    occupancy_map = OccupancyMap()
    # test_minimal_occupancy_map(occupancy_map)
    # test_small_occupancy_map(occupancy_map)
    test_medium_occupancy_map(occupancy_map)

    occupancy_map.plot_topological_map()    
    # test_mdp(occupancy_map)
    test_lrtdp(occupancy_map)