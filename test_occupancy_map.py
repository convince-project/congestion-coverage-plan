from OccupancyMap import OccupancyMap

def create_medium_occupancy_map(occupancy_map):
    occupancy_map.set_name('medium_occupancy_map')
    
    # add the vertices
    assert occupancy_map.add_vertex_with_id("vertex1", 0, 0)
    assert occupancy_map.add_vertex_with_id("vertex2", 1, 6)
    assert occupancy_map.add_vertex_with_id("vertex3", 5, 5)
    assert occupancy_map.add_vertex_with_id("vertex4", 7, 0)
    assert occupancy_map.add_vertex_with_id("vertex5", 9, 9)
    assert not occupancy_map.add_vertex_with_id("vertex5", 7, 9)

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


def test_medium_occupancy_map(occupancy_map):
    create_medium_occupancy_map(occupancy_map)
    # save the occupancy map
    occupancy_map.save_occupancy_map('data/occupancy_map_medium.yaml')
    #save the topological map
    occupancy_map.save_topological_map('data/topological_map_medium.yaml')
    occupancy_map.load_topological_map('data/topological_map_medium.yaml')
    occupancy_map.load_occupancy_map('data/occupancy_map_medium.yaml')
    # occupancy_map.plot_topological_map()

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
    occupancy_map = OccupancyMap()
    test_minimal_occupancy_map(occupancy_map)
    occupancy_map = OccupancyMap()
    test_small_occupancy_map(occupancy_map)
    occupancy_map = OccupancyMap()
    test_medium_occupancy_map(occupancy_map)
    
    # test_occupancy_map(occupancy_map)