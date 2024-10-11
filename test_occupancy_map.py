from OccupancyMap import OccupancyMap

def create_small_map(occupancy_map):
    occupancy_map.set_name('occupancy_map')
    
    # add the vertices
    assert occupancy_map.add_vertex_with_id("vertex1", 0, 0)
    assert occupancy_map.add_vertex_with_id("vertex2", 1, 6)
    assert occupancy_map.add_vertex_with_id("vertex3", 5, 5)
    assert occupancy_map.add_vertex_with_id("vertex4", 6, 1)
    assert occupancy_map.add_vertex_with_id("vertex5", 9, 9)
    assert not occupancy_map.add_vertex_with_id("vertex5", 7, 9)

    # add the edges
    assert occupancy_map.add_edge_with_id("edge1", "vertex1", "vertex2")
    assert occupancy_map.add_edge_with_id("edge2", "vertex1", "vertex3")
    assert occupancy_map.add_edge_with_id("edge3", "vertex1", "vertex4")
    assert occupancy_map.add_edge_with_id("edge5", "vertex2", "vertex3")
    assert occupancy_map.add_edge_with_id("edge4", "vertex2", "vertex5")
    assert occupancy_map.add_edge_with_id("edge6", "vertex3", "vertex4")
    assert occupancy_map.add_edge_with_id("edge7", "vertex3", "vertex5")
    assert occupancy_map.add_edge_with_id("edge8", "vertex4", "vertex5")
    assert not occupancy_map.add_edge_with_id("edge8", "vertex4", "vertex2")
    assert not occupancy_map.add_edge_with_id("edge9", "vertex4", "vertex10")
    assert not occupancy_map.add_edge_with_id("edge10", "vertex10", "vertex5")
    
    # add limits and edge traverse time
    for vertex in occupancy_map.get_vertices_list():
        assert occupancy_map.add_vertex_limit(vertex.get_id(), 3)
        assert not occupancy_map.add_vertex_limit(vertex.get_id(), 3)
    
    for edge in occupancy_map.get_edges_list():
        assert occupancy_map.add_edge_limit(edge.get_id(), 3)
        assert not occupancy_map.add_edge_limit(edge.get_id(), 3)
  
    

    for i in range(1,60):
        assert occupancy_map.add_vertex_occupancy("vertex1", 0.6, 0.4, i)
        assert not occupancy_map.add_vertex_occupancy("vertex1", 0.6, 0.4, i)
        assert occupancy_map.add_vertex_occupancy("vertex2", 0.6, 0.4, i)
        assert occupancy_map.add_vertex_occupancy("vertex3", 0.6, 0.4, i)
        assert occupancy_map.add_vertex_occupancy("vertex4", 0.6, 0.4, i)
        assert occupancy_map.add_vertex_occupancy("vertex5", 0.6, 0.4, i)

        assert occupancy_map.add_edge_occupancy("edge1", 0.6, 0.4, i)
        assert occupancy_map.add_edge_occupancy("edge2", 0.6, 0.4, i)
        assert occupancy_map.add_edge_occupancy("edge3", 0.6, 0.4, i)
        assert occupancy_map.add_edge_occupancy("edge4", 0.6, 0.4, i)
        assert occupancy_map.add_edge_occupancy("edge5", 0.6, 0.4, i)
        assert occupancy_map.add_edge_occupancy("edge6", 0.6, 0.4, i)
        assert occupancy_map.add_edge_occupancy("edge7", 0.6, 0.4, i)

    assert occupancy_map.add_edge_traverse_time("edge1", 'high', 20 )
    assert not occupancy_map.add_edge_traverse_time("edge1", 'high', 20 )
    assert occupancy_map.add_edge_traverse_time("edge1", 'low', 10 )
    assert occupancy_map.add_edge_traverse_time("edge2", 'high', 20 )
    assert occupancy_map.add_edge_traverse_time("edge2", 'low', 10 )
    assert occupancy_map.add_edge_traverse_time("edge3", 'high', 20 )
    assert occupancy_map.add_edge_traverse_time("edge3", 'low', 10 )
    assert occupancy_map.add_edge_traverse_time("edge4", 'high', 20 )
    assert occupancy_map.add_edge_traverse_time("edge4", 'low', 10 )
    assert occupancy_map.add_edge_traverse_time("edge5", 'high', 20 )
    assert occupancy_map.add_edge_traverse_time("edge5", 'low', 10 )
    assert occupancy_map.add_edge_traverse_time("edge6", 'high', 20 )
    assert occupancy_map.add_edge_traverse_time("edge6", 'low', 10 )
    assert occupancy_map.add_edge_traverse_time("edge7", 'high', 20 )
    assert occupancy_map.add_edge_traverse_time("edge7", 'low', 10 )


def test_occupancy_map(occupancy_map):
    create_small_map(occupancy_map)
    # save the occupancy map
    occupancy_map.save_occupancy_map('data/occupancy_map_small.yaml')
    #save the topological map
    occupancy_map.save_topological_map('data/topological_map_small.yaml')
    occupancy_map.load_topological_map('data/topological_map_small.yaml')
    occupancy_map.load_occupancy_map('data/occupancy_map_small.yaml')
    # occupancy_map.plot_topological_map()

if __name__ == "__main__":
    occupancy_map = OccupancyMap()
    test_occupancy_map(occupancy_map)