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