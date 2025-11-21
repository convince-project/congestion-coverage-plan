Tutorials
=========

To be able to plan, you will need:

- A map of the environment in which the robot will operate. A map created using ros2 slam_toolbox is recommended.
- A topological graph of the environment. See below for instructions on how to create an occupancy map.
- A CLiFF map learned from human motion data collected in the environment. See `<https://github.com/tkucner/CLiFF-map-matlab>` for instructions on how to create a CLiFF map.
- A dataset of human motion data collected in the environment.

Creating an Occupancy Map
------------------------

To create an occupancy map, once you have a map of the environment you will need:

- To instantiate a predictor object with the map file and CLiFF map file as inputs. (see CliffPredictor class in `src/congestion_coverage_plan/cliff_predictor/CliffPredictor.py`)
- To instantiate an OccupancyMap object with the predictor object as input. (see OccupancyMap class in `src/congestion_coverage_plan/occupancy_map/OccupancyMap.py`)

Once instantiated, you can use the various functions of the OccupancyMap to add vertices and edges to the topological graph.
An example of adding vertices and edges is shown below:

.. code-block:: python

    occupancy_map.add_vertex(vertex_id, posx, posy)
    occupancy_map.add_edge_with_id(edge_id, start_vertex_id, end_vertex_id)

After adding all vertices and edges, you can set edge limits using the function `add_edge_limit(edge_id, level)` where `level` is a dictionary of congestion levels to be used as limits for the edge with id `edge_id`.
An example of setting edge limits is shown below:

.. code-block:: python

    edges = occupancy_map.get_edges()
    level = {
        'low': [0,1],
        'medium': [1,3],
        'high': [3,500]
    }
    for edge_key in edges:
        occupancy_map.add_edge_limit(edges[edge_key].get_id(), level)


After the creation of the topological map, you can compute the average edge traverse time using the function `compute_average_edge_traverse_times()`.

Finally, you can save the occupancy map to a file using the function `save_occupancy_map(file_path)`.



Running the algorithm
---------------------

Once you have created and saved the occupancy map, you can run the congestion-aware planning algorithm using the occupancy map file, CLiFF map file, and human motion dataset as inputs.

To instantiate the planner, you will need to instantiate a solver (in this case the LRTDP solver) with the occupancy map (which takes also the cliff predictor as input) and the initial state defined as an MDP state.