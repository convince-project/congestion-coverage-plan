from ortools.init.python import init
from ortools.linear_solver import pywraplp
from OccupancyMap import OccupancyMap
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
import math
import numpy as np
from PredictorCreator import create_madama_cliff_predictor

def hamilton(graph, start_v):
  size = len(graph)
  # if None we are -unvisiting- comming back and pop v
  to_visit = [None, start_v]
  path = []
  visited = set([])
  while(to_visit):
    v = to_visit.pop()
    if v : 
      path.append(v)
      if len(path) == size:
        break
      visited.add(v)
      for x in graph[v]-visited:
        to_visit.append(None) # out
        to_visit.append(x) # in
    else: # if None we are comming back and pop v
      visited.remove(path.pop())
  return path


def compute_solution_cost(path, occupancy_map):
    cost = 0
    for i in range(len(path) - 1):
        cost += occupancy_map.find_edge_from_position(path[i], path[i + 1]).get_length()
    return cost

def create_graph(occupancy_map):
    graph = {}
    for vertex in occupancy_map.get_vertices():
        graph[vertex] = set()
    edges = occupancy_map.get_edges()
    for edge_id in edges.keys():
        graph[edges[edge_id].get_start()].add(edges[edge_id].get_end())
    return graph





def create_data_model(occupancy_map, time, initial_vertex_id, distance_matrix_function):
    """Stores the data for the problem."""
    data = {}
    data["distance_matrix"] = distance_matrix_function(occupancy_map, time, initial_vertex_id)
    data["num_vehicles"] = 1
    data["depot"] = 0
    return data


def create_data_model_from_matrix(matrix):
    """Stores the data for the problem."""
    data = {}
    data["distance_matrix"] = matrix
    data["num_vehicles"] = 1
    data["depot"] = 0
    return data


def print_solution(manager, routing, solution):
    """Prints solution on console."""
    print(f"Objective: {solution.ObjectiveValue()} miles")
    index = routing.Start(0)
    plan_output = "Route for vehicle 0:\n"
    route_distance = 0
    while not routing.IsEnd(index):
        plan_output += f" {manager.IndexToNode(index)} ->"
        previous_index = index
        index = solution.Value(routing.NextVar(index))
        route_distance += routing.GetArcCostForVehicle(previous_index, index, 0)
    plan_output += f" {manager.IndexToNode(index)}\n"
    plan_output += f"Route distance: {route_distance}miles\n"
    print(plan_output)


def get_solution(manager, routing, solution):
    """Returns the solution as a list of routes."""
    index = routing.Start(0)
    route = []
    while not routing.IsEnd(index):
        route.append("vertex" + str(manager.IndexToNode(index)))
        index = solution.Value(routing.NextVar(index))
    return route[1:]


def solve_with_google_with_data(data):
    """Entry point of the program."""
    # Instantiate the data problem.
    # data = create_data_model(occupancy_map, time, initial_vertex_id, distance_matrix_function)
    # print(data)

    # Create the routing index manager.
    manager = pywrapcp.RoutingIndexManager(
        len(data["distance_matrix"]), data["num_vehicles"], data["depot"]
    )

    # Create Routing Model.
    routing = pywrapcp.RoutingModel(manager)


    def distance_callback(from_index, to_index):
        """Returns the distance between the two nodes."""
        # Convert from routing variable Index to distance matrix NodeIndex.
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return data["distance_matrix"][from_node][to_node]

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)
    dimension_name = 'Distance'
    routing.AddDimension(
        transit_callback_index, # you can reuse the same callback use in SetArcCost
        0,  # no slack
        42000000, # vehicle maximum travel distance
        True,  # start cumul to zero
        dimension_name)

    # Define cost of each arc.
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
    )
    search_parameters.time_limit.seconds = 1

    solution = routing.SolveWithParameters(search_parameters)

    # Print solution on console.
    if solution:
        
        # print_solution(manager, routing, solution)
        # print(routing)
        # print(manager)
        # print(solution)
        # print(get_solution(manager, routing, solution))
        # return get_solution(manager, routing, solution)
        index = routing.Start(0)
        plan_output = "Route for vehicle 0:\n"
        route_distance = 0
        while not routing.IsEnd(index):
            plan_output += f" {manager.IndexToNode(index)} ->"
            previous_index = index
            index = solution.Value(routing.NextVar(index))
            route_distance += routing.GetArcCostForVehicle(previous_index, index, 0)
        return route_distance / 100.0
    else:
        # print("No solution found")
        return None

def solve_with_google(occupancy_map, time, initial_vertex_id, distance_matrix_function):
    """Entry point of the program."""
    # Instantiate the data problem.
    data = create_data_model(occupancy_map, time, initial_vertex_id, distance_matrix_function)
    # print(data)

    # Create the routing index manager.
    manager = pywrapcp.RoutingIndexManager(
        len(data["distance_matrix"]), data["num_vehicles"], data["depot"]
    )

    # Create Routing Model.
    routing = pywrapcp.RoutingModel(manager)


    def distance_callback(from_index, to_index):
        """Returns the distance between the two nodes."""
        # Convert from routing variable Index to distance matrix NodeIndex.
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return data["distance_matrix"][from_node][to_node]

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)
    dimension_name = 'Distance'
    routing.AddDimension(
        transit_callback_index, # you can reuse the same callback use in SetArcCost
        0,  # no slack
        42000000, # vehicle maximum travel distance
        True,  # start cumul to zero
        dimension_name)

    # Define cost of each arc.
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    # search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    # search_parameters.time_limit.seconds = 10
    # search_parameters.first_solution_strategy = (
    #     routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
    # )
    # solution = routing.SolveWithParameters(search_parameters)

    # if solution:
        
    #     print_solution(manager, routing, solution)
        # print(routing)
        # print(manager)
        # print(solution)
        # print(get_solution(manager, routing, solution))

    # Setting first solution heuristic.
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.local_search_metaheuristic = (
        routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH)
    search_parameters.time_limit.seconds = 100
    search_parameters.log_search = False



    # Solve the problem.
    solution = routing.SolveWithParameters(search_parameters)

    # Print solution on console.
    if solution:
        
        print_solution(manager, routing, solution)
        # print(routing)
        # print(manager)
        # print(solution)
        # print(get_solution(manager, routing, solution))
        return get_solution(manager, routing, solution)
    else:
        print("No solution found")
        return None

def get_current_occupancies(occupancy_map, idVertex1, idVertex2, occupancies):
    edge = occupancy_map.find_edge_from_position(idVertex1, idVertex2)
    if edge is None:
        edge = occupancy_map.find_edge_from_position(idVertex2, idVertex1)
    if edge is None:
        return 9999999999999999
    else:
        edge_id = edge.get_id()
        # here should be a function
        traverse_time =occupancy_map.get_edge_traverse_time(edge_id)
        if edge_id in occupancies.keys():
            for level in occupancy_map.get_occupancy_levels():
                if occupancies[edge_id] in range(occupancy_map.find_edge_limit(edge_id)[level][0], occupancy_map.find_edge_limit(edge_id)[level][1]):
                    return math.floor(traverse_time[level] * 100)
        else:
            return math.floor(traverse_time["zero"] * 100)
        

def get_length(occupancy_map, idVertex1, idVertex2, occupancies):
    edge = occupancy_map.find_edge_from_position(idVertex1, idVertex2)
    if edge is None:
        edge = occupancy_map.find_edge_from_position(idVertex2, idVertex1)
    if edge is None:
        return 9999999999999999
    return math.floor(edge.get_length() * 100)

def get_medium_occupancy(occupancy_map, idVertex1, idVertex2, occupancies):
    edge = occupancy_map.find_edge_from_position(idVertex1, idVertex2)
    if edge is None:
        edge = occupancy_map.find_edge_from_position(idVertex2, idVertex1)
    if edge is None:
        return 9999999999999999
    else:
        edge_id = edge.get_id()
        # here should be a function
        traverse_time =occupancy_map.get_edge_traverse_time(edge_id)
        if edge_id in occupancies.keys():
            for level in occupancy_map.get_occupancy_levels():
                if occupancies[edge_id] in range(occupancy_map.find_edge_limit(edge_id)[level][0], occupancy_map.find_edge_limit(edge_id)[level][1]):
                    return math.floor(traverse_time[level] * 100)
        else:
            return math.floor(traverse_time["zero"] * 100)

def get_high_occupancy(occupancy_map, idVertex1, idVertex2, occupancies):
    edge = occupancy_map.find_edge_from_position(idVertex1, idVertex2)
    if edge is None:
        edge = occupancy_map.find_edge_from_position(idVertex2, idVertex1)
    if edge is None:
        return 9999999999999999
    else:
        edge_id = edge.get_id()
        # here should be a function
        traverse_time =occupancy_map.get_edge_traverse_time(edge_id)
        if edge_id in occupancies.keys():
            return math.floor(traverse_time[occupancy_map.get_occupancy_levels()[-1]] * 100)
        else:
            return math.floor(traverse_time["zero"] * 100)

def create_matrix_from_occupancy_map_length(occupancy_map,time, initial_vertex_id):
    return create_matrix_from_occupancy_map_generic(occupancy_map, time, initial_vertex_id, get_length)

def create_matrix_from_occupancy_map_current_occupancy(occupancy_map, time, initial_vertex_id):
    return create_matrix_from_occupancy_map_generic(occupancy_map, time, initial_vertex_id, get_current_occupancies)

def create_matrix_from_occupancy_map_medium_occupancy(occupancy_map, time, initial_vertex_id):
    return create_matrix_from_occupancy_map_generic(occupancy_map, time, initial_vertex_id, get_medium_occupancy)

def create_matrix_from_occupancy_map_high_occupancy(occupancy_map, time, initial_vertex_id):
    return create_matrix_from_occupancy_map_generic(occupancy_map, time, initial_vertex_id, get_high_occupancy)

def create_matrix_from_occupancy_map_generic(occupancy_map, time, initial_vertex_id, length_function):
    matrix = []
    occupancies = occupancy_map.get_current_occupancies(time)

    vertices = occupancy_map.get_vertices()
    for row_id in range(0, len(vertices.keys()) + 1):
        row = []
        for column_id in range(0, len(vertices.keys()) + 1):
            idVertex1 = "vertex" + str(row_id)
            idVertex2 = "vertex" + str(column_id)
            # print(row_id, column_id)
            if row_id == column_id:
                row.append(0)
            elif row_id == 0:
                if column_id == 1:
                    row.append(0)
                elif column_id != 1:
                    row.append(9999999999999999)
            elif column_id == 0:
                if row_id == 1:
                    row.append(9999999999999999)
                elif row_id != 1:
                    row.append(0)
            else:
                row.append(length_function(occupancy_map, idVertex1, idVertex2, occupancies))
        matrix.append(row)
    return matrix

def create_matrix_from_vertices_list(vertices_ids, occupancy_map, initial_vertex_id):
    matrix = []
    initial_vertex_index = vertices_ids.index(initial_vertex_id) + 1

    for row_id in range(0, len(vertices_ids) + 1):
        row = []
        vertex_row_id = ""
        if row_id != 0:
            vertex_row_id = vertices_ids[row_id - 1]
        for column_id in range(0, len(vertices_ids) + 1):
            vertex_column_id = ""
            if column_id != 0:
                vertex_column_id = vertices_ids[column_id - 1]
            # print(row_id, column_id)
            if row_id == column_id:
                row.append(0)
            elif row_id == 0:
                if column_id == initial_vertex_index:
                    row.append(0)
                elif column_id != initial_vertex_index:
                    row.append(9999999999999999)
            elif column_id == 0:
                if row_id == initial_vertex_index:
                    row.append(9999999999999999)
                elif row_id != initial_vertex_index:
                    row.append(0)
            else:
                if vertex_column_id == "" or vertex_row_id == "":
                    row.append(9999999999999999)
                else:
                    # print("finding edge from", vertex_row_id, vertex_column_id)
                    edge_length = occupancy_map.find_edge_from_position(vertex_row_id, vertex_column_id)
                    if edge_length is None:
                        row.append(9999999999999999)
                    else:
                        row.append(math.floor(edge_length.get_length() * 100))
        matrix.append(row)
    return matrix



def test_create_matrix_from_vertices_list():
    predictor = create_madama_cliff_predictor()
    occupancy_map = OccupancyMap(predictor)
    occupancy_map.load_occupancy_map("data/occupancy_maps_madama_sequential_21/occupancy_map_madama_sequential_21_2_levels.yaml")
    vertices = occupancy_map.get_vertices()
    print("vertices", occupancy_map.get_vertices_list())
    unvisited_vertices_ids = []
    for v in vertices.keys():
        if v != "vertex1" and v != "vertex3" and v != "vertex16":
            unvisited_vertices_ids.append(v)
    # unvisited_vertices_ids.sort(key=lambda x: int(x.replace("vertex", "")))
    print("unvisited_vertices_ids", unvisited_vertices_ids)
    initial_vertex_id = "vertex2"
    matrix = create_matrix_from_vertices_list(unvisited_vertices_ids, occupancy_map, initial_vertex_id)
    with open("matrix.txt", "w") as f:
        for row in matrix:
            f.write(str(row) + "\n")

    matrix2 = create_matrix_from_occupancy_map_length(occupancy_map, 0, initial_vertex_id)
    with open("matrix2.txt", "w") as f:
        for row in matrix2:
            f.write(str(row) + "\n")
    print("matrix created")
    # now solve with google
    data = create_data_model_from_matrix(matrix)
    print("data created")
    solution = solve_with_google_with_data(data)
    print("solution from google", solution)


    



if __name__ == "__main__":
    test_create_matrix_from_vertices_list()