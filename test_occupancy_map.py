from OccupancyMap import OccupancyMap
import utils
import matplotlib.pyplot as plt

from cliff_predictor import CliffPredictor
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


def test_medium_occupancy_map(occupancy_map):
    time_to_predict = 1717314218.0
    time_now = 1717314208.0
    create_medium_occupancy_map(occupancy_map)
    tracks = occupancy_map.get_tracks_by_time(time_now)
    # for track in tracks:
    #     for pos in tracks[track]:
    #         print(pos[0])
        # print(tracks[track])
    predicted_positions = occupancy_map.predict_people_positions(time_now, time_to_predict)
    # print(predicted_positions[0][0])
    for person in predicted_positions:
        print("person" + "------------------------")
        for trajectory in person:
            for position in trajectory:
                print("time" + str(position[0]) + " x: " + str(position[1]) + " y: " + str(position[2]))
    occupancy_map.plot_predicted_positions(time_to_predict)
    # print(predicted_positions[0])
    # for pos in predicted_positions:
    #     for i in pos:
    #         print(len(i))
    #         print("------------------------")
    # occupancy_map.predict_occupancies(time_to_predict)
    # occupancy_map.predict_occupancies(time_to_predict,time_to_predict+ 10)
    # for edge in occupancy_map.get_edges_list():
    #     print(edge.get_id())
    #     if occupancy_map.get_edge_expected_occupancy(time_to_predict, edge.get_id()):
    #         print(edge.get_id(), occupancy_map.get_edge_expected_occupancy(time_to_predict, edge.get_id())['high'] , occupancy_map.get_edge_expected_occupancy(time_to_predict, edge.get_id())['low'])
    # for vertex in occupancy_map.get_vertices_list():
    #     print(vertex.get_id())
    #     if occupancy_map.get_vertex_expected_occupancy(time_to_predict, vertex.get_id()):
    #         print(vertex.get_id(), occupancy_map.get_vertex_expected_occupancy(time_to_predict, vertex.get_id())['high'] , occupancy_map.get_vertex_expected_occupancy(time_to_predict, vertex.get_id())['low'])
    # occupancy_map.print_people_in_areas(time_to_predict)
    # occupancy_map.calculate_poisson_binomial(time_to_predict)
    # occupancy_map.print_poisson_binomial(time_to_predict)
    # occupancy_map.plot_predicted_positions(time_to_predict)
    # print(occupancy_map.get_tracks_by_time(1717314208.0))
    # predicted_positions = occupancy_map.predict_people_positions(1717314218.0)

    # # save the occupancy map
    # occupancy_map.track_current_people()
    # # occupancy_map.plot_tracked_people()
    # occupancy_map.predict_people_positions()
    # occupancy_map.get_people_predicted_positions(time_to_predict)
    # occupancy_map.assign_people_to_areas(time_to_predict)
    # occupancy_map.print_people_in_areas(time_to_predict)

    # occupancy_map.calculate_poisson_binomial(time_to_predict)
    # occupancy_map.print_poisson_binomial(time_to_predict)
    # occupancy_map.plot_predicted_positions(time_to_predict)
    # occupancy_map.plot_topological_map()

    # plt.show()

def create_small_occupancy_map(occupancy_map):
    occupancy_map.set_name('occupancy_map')
    
    # add the vertices
    assert occupancy_map.add_vertex_with_id("vertex1", 0, 0)
    assert occupancy_map.add_vertex_with_id("vertex2", 1, 6)
    assert occupancy_map.add_vertex_with_id("vertex3", 5, 5)
    assert occupancy_map.add_vertex_with_id("vertex4", 7, 0)
    # assert occupancy_map.add_vertex_with_id("vertex5", 9, 9)
    # assert not occupancy_map.add_vertex_with_id("vertex5", 7, 9)

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
    # assert occupancy_map.add_edge_with_id("edge6", "vertex2", "vertex5")
    # assert occupancy_map.add_edge_with_id("edge14", "vertex5", "vertex2")
    # assert occupancy_map.add_edge_with_id("edge7", "vertex3", "vertex5")
    # assert occupancy_map.add_edge_with_id("edge15", "vertex5", "vertex3")
    # assert occupancy_map.add_edge_with_id("edge8", "vertex4", "vertex5")
    # assert occupancy_map.add_edge_with_id("edge16", "vertex5", "vertex4")

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
  
    

    i = 0
    for vertex in occupancy_map.get_vertices_list():
        assert occupancy_map.add_vertex_occupancy(vertex.get_id(), 0.6, 0.4, i)
        assert not occupancy_map.add_vertex_occupancy(vertex.get_id(), 0.6, 0.4, i)
    for edge in occupancy_map.get_edges_list():
        assert occupancy_map.add_edge_occupancy(edge.get_id(), 0.6, 0.4, i)
        assert not occupancy_map.add_edge_occupancy(edge.get_id(), 0.6, 0.4, i)
    for edge in occupancy_map.get_edges_list():
        assert occupancy_map.get_edge_expected_occupancy(i, edge.get_id()) == {'high': 0.6, 'low': 0.4}

    for edge in occupancy_map.get_edges_list():
        # print(occupancy_map.get_edge_traverse_time(edge.get_id()))
        assert occupancy_map.get_edge_traverse_time(edge.get_id()) == None
        assert occupancy_map.add_edge_traverse_time(edge.get_id(), 'high', 2 * occupancy_map.get_vertex_distance(edge.get_start(), edge.get_end()))
        assert occupancy_map.add_edge_traverse_time(edge.get_id(), 'low',  occupancy_map.get_vertex_distance(edge.get_start(), edge.get_end()))
        assert occupancy_map.get_edge_traverse_time(edge.get_id()) == {'high': 2 * occupancy_map.get_vertex_distance(edge.get_start(), edge.get_end()), 'low': occupancy_map.get_vertex_distance(edge.get_start(), edge.get_end())}
    assert not occupancy_map.add_edge_traverse_time("edge1", 'high', 20 )
    # for edge in occupancy_map.get_edges_list():
        
    #     print(edge.get_id(), occupancy_map.get_edge_traverse_time(edge.get_id())['high'] * occupancy_map.get_edge_expected_occupancy(i, edge.get_id())['high'] + occupancy_map.get_edge_traverse_time(edge.get_id())['low'] * occupancy_map.get_edge_expected_occupancy(i, edge.get_id())['low'])


def test_small_occupancy_map(occupancy_map):
    create_small_occupancy_map(occupancy_map)
    # save the occupancy map
    occupancy_map.save_occupancy_map('data/occupancy_map_small.yaml')
    #save the topological map
    occupancy_map.save_topological_map('data/topological_map_small.yaml')
    occupancy_map.load_topological_map('data/topological_map_small.yaml')
    occupancy_map.load_occupancy_map('data/occupancy_map_small.yaml')
    # occupancy_map.plot_topological_map()


def create_minimal_occupancy_map(occupancy_map):
    occupancy_map.set_name('minimal_occupancy_map')
    
    # add the vertices
    assert occupancy_map.add_vertex_with_id("vertex1", 0, 0)
    assert occupancy_map.add_vertex_with_id("vertex2", 1, 6)
    assert occupancy_map.add_vertex_with_id("vertex3", 5, 5)
    # assert occupancy_map.add_vertex_with_id("vertex5", 9, 9)
    # assert not occupancy_map.add_vertex_with_id("vertex5", 7, 9)

    # add the edges
    assert occupancy_map.add_edge_with_id("edge1", "vertex1", "vertex2")
    assert occupancy_map.add_edge_with_id("edge9", "vertex2", "vertex1")
    assert occupancy_map.add_edge_with_id("edge2", "vertex1", "vertex3")
    assert occupancy_map.add_edge_with_id("edge10", "vertex3", "vertex1")
    assert occupancy_map.add_edge_with_id("edge4", "vertex2", "vertex3")
    assert occupancy_map.add_edge_with_id("edge12", "vertex3", "vertex2")
    
    # add limits and edge traverse time
    for vertex in occupancy_map.get_vertices_list():
        assert occupancy_map.add_vertex_limit(vertex.get_id(), 3)
        assert not occupancy_map.add_vertex_limit(vertex.get_id(), 3)
    
    for edge in occupancy_map.get_edges_list():
        assert occupancy_map.add_edge_limit(edge.get_id(), 3)
        assert not occupancy_map.add_edge_limit(edge.get_id(), 3)
        # print(edge.get_start())
  
    

    i = 0
    for vertex in occupancy_map.get_vertices_list():
        assert occupancy_map.add_vertex_occupancy(vertex.get_id(), 0.6, 0.4, i)
        assert not occupancy_map.add_vertex_occupancy(vertex.get_id(), 0.6, 0.4, i)
    for edge in occupancy_map.get_edges_list():
        assert occupancy_map.add_edge_occupancy(edge.get_id(), 0.6, 0.4, i)
        assert not occupancy_map.add_edge_occupancy(edge.get_id(), 0.6, 0.4, i)
    for edge in occupancy_map.get_edges_list():
        assert occupancy_map.get_edge_expected_occupancy(i, edge.get_id()) == {'high': 0.6, 'low': 0.4}

    for edge in occupancy_map.get_edges_list():
        # print(occupancy_map.get_edge_traverse_time(edge.get_id()))
        assert occupancy_map.get_edge_traverse_time(edge.get_id()) == None
        assert occupancy_map.add_edge_traverse_time(edge.get_id(), 'high', 2 * occupancy_map.get_vertex_distance(edge.get_start(), edge.get_end()))
        assert occupancy_map.add_edge_traverse_time(edge.get_id(), 'low',  occupancy_map.get_vertex_distance(edge.get_start(), edge.get_end()))
        assert occupancy_map.get_edge_traverse_time(edge.get_id()) == {'high': 2 * occupancy_map.get_vertex_distance(edge.get_start(), edge.get_end()), 'low': occupancy_map.get_vertex_distance(edge.get_start(), edge.get_end())}
    assert not occupancy_map.add_edge_traverse_time("edge1", 'high', 20 )
    # for edge in occupancy_map.get_edges_list():
        
    #     print(edge.get_id(), occupancy_map.get_edge_traverse_time(edge.get_id())['high'] * occupancy_map.get_edge_expected_occupancy(i, edge.get_id())['high'] + occupancy_map.get_edge_traverse_time(edge.get_id())['low'] * occupancy_map.get_edge_expected_occupancy(i, edge.get_id())['low'])


def test_minimal_occupancy_map(occupancy_map):
    create_minimal_occupancy_map(occupancy_map)
    # save the occupancy map
    occupancy_map.save_occupancy_map('data/minimal_occupancy_map.yaml')
    #save the topological map
    occupancy_map.save_topological_map('data/minimal_topological_map.yaml')
    occupancy_map.load_topological_map('data/minimal_topological_map.yaml')
    occupancy_map.load_occupancy_map('data/minimal_occupancy_map.yaml')
    # occupancy_map.plot_topological_map()


if __name__ == "__main__":
    # occupancy_map = OccupancyMap()
    # test_minimal_occupancy_map(occupancy_map)
    # occupancy_map = OccupancyMap()
    # test_small_occupancy_map(occupancy_map)
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
    test_medium_occupancy_map(occupancy_map)
    
    # test_occupancy_map(occupancy_map)