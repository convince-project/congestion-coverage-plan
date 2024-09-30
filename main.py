from OccupancyMap import OccupancyMap
from MDP import MDP
from LrtdpTvmaAlgorithm import LrtdpTvmaAlgorithm
import math
import random

        
def create(occupancy_map):
    occupancy_map.set_name('occupancy_map')
    # add a node to the topological map
    occupancy_map.add_node_with_id("node1", 0, 0)
    occupancy_map.add_node_with_id("node2", 2, 5)
    occupancy_map.add_node_with_id("node3", 5, 5)
    occupancy_map.add_node_with_id("node4", 6, 2)
    occupancy_map.add_node_with_id("node5", 9, 2)
    occupancy_map.add_node_with_id("node6", 5, 9)
    occupancy_map.add_node_with_id("node7", 7, 8)
    occupancy_map.add_node_with_id("node8", 9, 6)
    occupancy_map.add_node_with_id("node9", 11, 11)
    occupancy_map.add_node_with_id("node10", 11, 9)
    occupancy_map.add_terminal_node_with_id("node9")
    occupancy_map.add_terminal_node_with_id("node10")
    # for each node add the occupancy
    occupancy_map.add_edge_with_id("edge1", "node1", "node2")
    occupancy_map.add_edge_with_id("edge2", "node1", "node3")
    occupancy_map.add_edge_with_id("edge3", "node1", "node4")
    occupancy_map.add_edge_with_id("edge4", "node1", "node5")
    occupancy_map.add_edge_with_id("edge5", "node2", "node3")
    occupancy_map.add_edge_with_id("edge6", "node2", "node6")
    occupancy_map.add_edge_with_id("edge7", "node2", "node7")
    occupancy_map.add_edge_with_id("edge8", "node3", "node4")
    occupancy_map.add_edge_with_id("edge9", "node3", "node6")
    occupancy_map.add_edge_with_id("edge10", "node3", "node7")
    occupancy_map.add_edge_with_id("edge11", "node3", "node8")
    occupancy_map.add_edge_with_id("edge12", "node4", "node5")
    occupancy_map.add_edge_with_id("edge13", "node4", "node7")
    occupancy_map.add_edge_with_id("edge14", "node4", "node8")
    occupancy_map.add_edge_with_id("edge15", "node5", "node8")    
    occupancy_map.add_edge_with_id("edge15", "node5", "node10")    
    occupancy_map.add_edge_with_id("edge16", "node5", "node9")    
    occupancy_map.add_edge_with_id("edge17", "node6", "node7")    
    occupancy_map.add_edge_with_id("edge18", "node6", "node9")    
    occupancy_map.add_edge_with_id("edge19", "node7", "node8")    
    occupancy_map.add_edge_with_id("edge20", "node7", "node9")    
    occupancy_map.add_edge_with_id("edge20", "node7", "node10")    
    occupancy_map.add_edge_with_id("edge21", "node8", "node9")   
    occupancy_map.add_edge_with_id("edge21", "node8", "node10")   

    

    occupancy_map.calculate_current_nodes_occupancy()
    occupancy_map.calculate_current_edges_occupancy()

    for node in occupancy_map.topological_map['nodes']:
        occupancy_map.add_node_limit(node['id'], 3)
    for edge in occupancy_map.topological_map['edges']:
        occupancy_map.add_edge_limit(edge['id'], 3)
        occupancy_map.add_edge_traverse_time(edge['id'], 'high', 20 + math.floor(random.random() * 5))
        occupancy_map.add_edge_traverse_time(edge['id'], 'low', 10 + math.floor(random.random() * 5))

    for i in range(1,30):
        occupancy_map.predict_occupancies(i)


def test_mdp(occupancy_map):
    # print(occupancy_map.get_nodes_list())
    # print(occupancy_map.get_edges_list())   
    mdp = MDP(occupancy_map, 'node1')
    print(mdp.get_states())
    print(mdp.get_transitions())

    print(mdp.get_possible_actions_from_current_state())
    print(mdp.get_current_state())
    mdp.plot_as_graph()

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
    occupancy_map.plot_topological_map()
    # save the occupancy map

if __name__ == "__main__":
    occupancy_map = OccupancyMap()
    # test_occupancy_map(occupancy_map)
    occupancy_map.load_topological_map('data/topological_map.yaml')
    occupancy_map.load_occupancy_map('data/occupancy_map.yaml')
    test_mdp(occupancy_map)

    # lrtdp = LrtdpTvmaAlgorithm('occupancy_map', 'node1', 0.01, 300)
    # lrtdp.lrtdp_tvma()