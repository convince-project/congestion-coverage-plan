from OccupancyMap import OccupancyMap
from MDP import MDP, State, Transition
from test_occupancy_map import test_minimal_occupancy_map,  test_small_occupancy_map, create_medium_occupancy_map
from test_mdp import test_mdp
from LrtdpTvmaAlgorithm import LrtdpTvmaAlgorithm
import utils
from cliff_predictor import CliffPredictor


def test_lrtdp(occupancy_map):
    
    initial_state_name = "vertex1"
    visited_set = set()
    visited_set.add(initial_state_name)
    # print(visited_set)
    final_state_name = "vertex3"
    final_state = State(final_state_name, 
                          26, 
                          (occupancy_map.find_vertex_from_id(final_state_name).get_posx(), 
                           occupancy_map.find_vertex_from_id(final_state_name).get_posy()), 
                           set(["vertex1", "vertex2", "vertex3", "vertex4", "vertex5"]))
    second_state_name = "vertex2"
    second_state = State(second_state_name,
                         6,
                            (occupancy_map.find_vertex_from_id(second_state_name).get_posx(),
                            occupancy_map.find_vertex_from_id(second_state_name).get_posy()),
                            set([initial_state_name, second_state_name]))
    initial_state = State(initial_state_name, 
                          0, 
                          (occupancy_map.find_vertex_from_id(initial_state_name).get_posx(), 
                           occupancy_map.find_vertex_from_id(initial_state_name).get_posy()), 
                           set([initial_state_name]))
    # lrtdp = LrtdpTvmaAlgorithm(occupancy_map=occupancy_map, initial_state_name=second_state_name, convergence_threshold=0.5, time_bound_real=10000, planner_time_bound=500, vinitState=second_state, )
    lrtdp = LrtdpTvmaAlgorithm(occupancy_map=occupancy_map, initial_state_name=initial_state_name, convergence_threshold=0.5, time_bound_real=10000, planner_time_bound=500, vinitState=initial_state, )
    # lrtdp = LrtdpTvmaAlgorithm(occupancy_map=occupancy_map, initial_state_name=final_state_name, convergence_threshold=0.5, time_bound_real=10000, planner_time_bound=500, vinitState=final_state )
    assert lrtdp.occupancy_map == occupancy_map
    # assert lrtdp.mdp == mdp
    # assert lrtdp.vinitState == second_state
    # assert lrtdp.vinitStateName == second_state_name
    # assert lrtdp.timeBoundGlobal == 500
    assert lrtdp.policy == {}
    assert lrtdp.valueFunction == {}
    assert lrtdp.solved_set == set()
    # assert lrtdp.value == {}
    assert not lrtdp.solved(initial_state)
    # assert lrtdp.check_solved(final_state, 0.5)
    # assert lrtdp.get_value(initial_state) == 0
    # print(lrtdp.calculate_Q(initial_state, "vertex2"))
    # assert lrtdp.residual(initial_state) == 0
    # for action in lrtdp.mdp.get_possible_actions(initial_state):
    #     print(action)
    #     print(lrtdp.calculate_Q(initial_state, action))
    # argmin_q = lrtdp.calculate_argmin_Q(initial_state)
    # print(argmin_q)
    # print(argmin_q[1])
    # assert argmin_q == (5.0, State(initial_state.get_vertex(), initial_state.get_time(), initial_state.get_position(), initial_state.get_visited_vertices()), "wait")
    # lrtdp.update(initial_state)
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

    # for line in lrtdp.create_mst_matrix():
    #     print(line)
    # print(lrtdp.calculate_mst())
    # print(lrtdp.calculate_shortest_path_in_mst("vertex1", "vertex2"))
    # print(lrtdp.calculate_shortest_path_in_mst("vertex1", "vertex3"))
    # print(lrtdp.calculate_shortest_path_in_mst("vertex1", "vertex4"))
    # print(lrtdp.calculate_shortest_path_in_mst("vertex1", "vertex5"))
    # print(lrtdp.create_mst_matrix())
    lrtdp.lrtdp_tvma()
    # assert lrtdp.solved(final_state)


    print("FINAL POLICY:")
    for state in lrtdp.policy:
        # print("State: ", lrtdp.policy[state])
        # print("state **", lrtdp.policy[state][1])
        # print("action **", lrtdp.policy[state][2])
        print("lrtdp_tvma_trial::Policy: ", "qvalue", lrtdp.policy[state][0], "current state", str(lrtdp.policy[state][1]), "action", lrtdp.policy[state][2])

        # print("next state **", lrtdp.policy[state][3])
    # print ("FINAL VALUE FUNCTION", lrtdp.valueFunction)
    


if __name__ == "__main__":
        # occupancy_map = OccupancyMap()
    # test_minimal_occupancy_map(occupancy_map)
    # occupancy_map = OccupancyMap()
    # test_small_occupancy_map(occupancy_map)
    map_file = "CLiFF_LHMP/maps/iit.png"
    mod_file = "CLiFF_LHMP/MoDs/iit/iit_cliff.csv"
    # ground_truth_data_file = "dataset/iit/iit.csv"
    # result_file = "iit_results.csv"
    observed_tracklet_length = 5
    start_length = 0
    planning_horizon = 50
    beta = 1
    sample_radius = 0.5
    delta_t = 0.4
    method = utils.Method.MoD
    # method = utils.Method.CVM
    dataset = utils.Dataset.IIT
    fig_size = [-12.83, 12.83, -12.825, 12.825]
    predictor = CliffPredictor(dataset, map_file, mod_file, observed_tracklet_length, start_length, planning_horizon, beta, sample_radius, delta_t, method, fig_size)

    occupancy_map = OccupancyMap(predictor)
    # test_minimal_occupancy_map(occupancy_map)
    # test_small_occupancy_map(occupancy_map)
    create_medium_occupancy_map(occupancy_map)

    # occupancy_map.plot_topological_map()    
    # test_mdp(occupancy_map)
    test_lrtdp(occupancy_map)