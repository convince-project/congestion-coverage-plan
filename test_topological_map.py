from TopologicalMap import TopologicalMap


def create_small_map(topological_map):
    topological_map.set_name('topological_map')
    
    # add the vertices
    assert topological_map.add_vertex_with_id("vertex1", 0, 0)
    assert topological_map.add_vertex_with_id("vertex2", 1, 6)
    assert topological_map.add_vertex_with_id("vertex3", 5, 5)
    assert topological_map.add_vertex_with_id("vertex4", 6, 1)
    assert topological_map.add_vertex_with_id("vertex5", 9, 9)
    assert not topological_map.add_vertex_with_id("vertex5", 7, 9)

    # add the edges
    assert topological_map.add_edge_with_id("edge1", "vertex1", "vertex2")
    assert topological_map.add_edge_with_id("edge2", "vertex1", "vertex3")
    assert topological_map.add_edge_with_id("edge3", "vertex1", "vertex4")
    assert topological_map.add_edge_with_id("edge5", "vertex2", "vertex3")
    assert topological_map.add_edge_with_id("edge4", "vertex2", "vertex5")
    assert topological_map.add_edge_with_id("edge6", "vertex3", "vertex4")
    assert topological_map.add_edge_with_id("edge7", "vertex3", "vertex5")
    assert topological_map.add_edge_with_id("edge8", "vertex4", "vertex5")
    assert not topological_map.add_edge_with_id("edge8", "vertex4", "vertex2")
    assert not topological_map.add_edge_with_id("edge9", "vertex4", "vertex10")
    assert not topological_map.add_edge_with_id("edge10", "vertex10", "vertex5")
    
    for vertex in topological_map.get_vertices_list():
        assert type(vertex.get_posx()) == int
        assert type(vertex.get_posy()) == int




def test_topological_map(topological_map):

    create_small_map(topological_map)
    # save the topological map
    topological_map.save_topological_map('data/topological_map_small.yaml')
    # load the topological map
    topological_map.load_topological_map('data/topological_map_small.yaml')
    # plot the topological map
    topological_map.plot_topological_map()

if __name__ == "__main__":
    topological_map = TopologicalMap()
    test_topological_map(topological_map)
