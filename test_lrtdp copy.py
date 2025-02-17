from OccupancyMap import OccupancyMap
from MDP import MDP, State, Transition
from test_mdp import test_mdp
from LrtdpTvmaAlgorithm import LrtdpTvmaAlgorithm
import utils
from cliff_predictor import CliffPredictor
from test_occupancy_map import *


def test_lrtdp(occupancy_map, time_init):
    
    initial_state_name = "vertex1"
    visited_set = set()
    visited_set.add(initial_state_name)
    initial_state = State(initial_state_name, 
                          0, 
                          (occupancy_map.find_vertex_from_id(initial_state_name).get_posx(), 
                           occupancy_map.find_vertex_from_id(initial_state_name).get_posy()), 
                           set([initial_state_name]))
    lrtdp = LrtdpTvmaAlgorithm(occupancy_map=occupancy_map, initial_state_name=initial_state_name, convergence_threshold=0.5, time_bound_real=10000, planner_time_bound=50, time_for_occupancies=time_init ,vinitState=initial_state, )
    assert lrtdp.occupancy_map == occupancy_map
    assert lrtdp.policy == {}
    assert lrtdp.valueFunction == {}
    assert lrtdp.solved_set == set()
    assert not lrtdp.solved(initial_state)
    lrtdp.lrtdp_tvma()


    print("FINAL POLICY:")
    for state in lrtdp.policy:
        print("lrtdp_tvma_trial::Policy: ", "qvalue", lrtdp.policy[state][0], "current state", str(lrtdp.policy[state][1]), "action", lrtdp.policy[state][2])

    


def test_iit():
    predictor = create_iit_cliff_predictor()
    occupancy_map = OccupancyMap(predictor)
    occupancy_map.load_occupancy_map("data/occupancy_map_iit_medium_latest.yaml")
    time_init = 1717314208.0
    test_lrtdp(occupancy_map, time_init)




if __name__ == "__main__":
    
    test_iit()
    # occupancy_map = OccupancyMap(predictor)
    # # test_minimal_occupancy_map(occupancy_map)
    # # test_small_occupancy_map(occupancy_map)
    # create_medium_occupancy_map(occupancy_map)

    # # occupancy_map.plot_topological_map()    
    # # test_mdp(occupancy_map)
    # test_lrtdp(occupancy_map)