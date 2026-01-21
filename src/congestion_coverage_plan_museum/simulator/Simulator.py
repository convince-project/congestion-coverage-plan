from matplotlib.pylab import matrix
from congestion_coverage_plan_museum.mdp.MDP import MDP, State, Transition
from congestion_coverage_plan_museum.solver.LrtdpTvmaAlgorithm import LrtdpTvmaAlgorithm
from congestion_coverage_plan_museum.map_utils.OccupancyMap import OccupancyMap
import congestion_coverage_plan_museum.utils.dataset_utils as dataset_utils
import warnings
from congestion_coverage_plan_museum.tsp.tsp import *
from tqdm import *
from datetime import datetime

class Simulator:

    def __init__(self, occupancy_map, time_for_occupancies, wait_time, time_bound_real, explain_time):
        self._time_for_occupancies = time_for_occupancies # time offset to calculate occupancies
        self._occupancy_map = occupancy_map
        self._robot_min_speed = 0.6
        self._robot_max_speed = 1.2
        self._wait_time = wait_time
        self._explain_time = explain_time
        self._time_bound_real = time_bound_real # maximum time for a single planning step in seconds


    def set_time_for_occupancies(self, time):
        self._time_for_occupancies = time


    def execute_step(self,state, action):
        if action == "wait":
            # state, collisions, traverse_time
            return State(state.get_vertex(), state.get_time() + self._wait_time, state.get_visited_vertices().copy(), state.get_pois_explained().copy()), 0, self._wait_time
        if action =="explain":
            current_vertex = self._occupancy_map.find_vertex_from_id(state.get_vertex())
            current_poi = current_vertex.get_poi_number()
            pois_explained = state.get_pois_explained().copy()
            pois_explained.add(current_poi)
            return State(vertex=state.get_vertex(), 
                         time=state.get_time() + self._explain_time, 
                         visited_vertices=state.get_visited_vertices().copy(), 
                         pois_explained=pois_explained), 0, self._explain_time
                         

        calculated_traverse_time, collisions = self.calculate_traverse_time(state, action)

        next_time = state.get_time() + calculated_traverse_time
        next_vertex = action
        next_position = (self._occupancy_map.find_vertex_from_id(next_vertex).get_posx(), self._occupancy_map.find_vertex_from_id(next_vertex).get_posy())
        visited_vertices = state.get_visited_vertices().copy()
        if next_vertex not in state.get_visited_vertices():
            visited_vertices.add(next_vertex)
        next_state = State(next_vertex, next_time, visited_vertices, state.get_pois_explained().copy())
        return next_state, collisions, calculated_traverse_time
        

    def calculate_traverse_time(self, state, action):
        occupancies = self.get_current_occupancies(state)
        edge_name = self._occupancy_map.find_edge_from_position(state.get_vertex(), action).get_id()
        edge_occupancy = 0
        if edge_name in occupancies.keys():
            edge_occupancy = occupancies[edge_name]
        edge_traverse_time = self._occupancy_map.get_edge_traverse_time(edge_name)
        traverse_time = edge_traverse_time['zero'] + edge_occupancy* self._occupancy_map.get_people_collision_cost()
        return traverse_time, edge_occupancy


    def simulate_lrtdp(self, start_time, initial_state, planner_time_bound, convergence_threshold, logger=None, simulate_planning_while_moving=False, heuristic_function=None):
        # print("start_time", start_time)
        self.set_time_for_occupancies(start_time)
        completed = False
        state = initial_state
        # self._occupancy_map.predict_occupancies(time, 50)

        executed_steps = []
        planning_time = []
        steps_time = []
        future_planning_time = self._time_bound_real
        while not completed:
            # print("state before", state)
            # print("#####################################################################################")
            # print("init", self.get_current_occupancies(state))
            if self._occupancy_map.find_vertex_from_id(state.get_vertex()).is_final_goal():
                completed = True
                break
            initial_planning_time = datetime.now()
            if not simulate_planning_while_moving:
                policy = self.plan(state, planner_time_bound, logger, self._time_bound_real, convergence_threshold, heuristic_function)
            else:
                policy = self.plan(state, planner_time_bound, logger, future_planning_time, convergence_threshold, heuristic_function)
            total_planning_time = datetime.now() - initial_planning_time
            planning_time.append(float(total_planning_time.total_seconds()))
            # print(policy)
            # print("policy[0]", policy[0])
            # print("policy[1]", policy[1])
            if state.get_time() > planner_time_bound:
                print("exit because state time exceeded planner time bound")
                print(state.get_visited_vertices())
                print(state.get_vertex())
                executed_steps.append(("FAILURE", 0))
                return (state.get_time(), executed_steps, planning_time, steps_time)
            if policy[1] is not None:
                # print(policy)
                # print("policy for current state", policy[1][str(state)])
                if str(state) in policy[1]:
                    action = policy[1][str(state)]

                    print("action", action[2])
                    state, collisions, traverse_time = self.execute_step(state, action[2])
                    # print(state.get_time(), state.get_vertex())
                    future_planning_time = float(traverse_time)

                    executed_steps.append((action[2], collisions))
                    steps_time.append(float(traverse_time))
                    # print(state.get_time(), state.get_vertex())
                    print("state after", state)
                else:
                    print("exit because state not in policy[1], increasing planning time")
                    future_planning_time = future_planning_time + 10
                    
            else:
                if future_planning_time >= 200:
                    print("exit because policy[1] is none and future planning time too high")
                    print(state.get_visited_vertices())
                    print(state.get_vertex())
                    executed_steps.append(("FAILURE", 0))
                    return (state.get_time(), executed_steps , planning_time, steps_time)
                else:
                    future_planning_time = future_planning_time + 10
                    print("exit because policy[1] is none")
                    print(state.get_visited_vertices())
                    print(state.get_vertex())

                
        # print (state.get_time(), executed_steps)

        return (state.get_time(), executed_steps, planning_time, steps_time)


    def get_current_occupancies(self, state):
        current_time = self._time_for_occupancies + state.get_time()
        self._occupancy_map.calculate_current_occupancies(current_time)
        return self._occupancy_map.get_current_occupancies(current_time)


    def plan(self, current_state, planner_time_bound, logger, time_bound_real, convergence_threshold, heuristic_function):
        # print("current_state", current_state)
        # print("start_time", self._start_time)
        # print("planning time", self._time_for_occupancies,  current_state.get_time())
        # print("planning")x 
        init_time = datetime.now()
        lrtdp = LrtdpTvmaAlgorithm(occupancy_map=self._occupancy_map, 
                                   initial_state_name=current_state.get_vertex(), 
                                   convergence_threshold=convergence_threshold, 
                                   time_bound_real=time_bound_real, 
                                   planner_time_bound=planner_time_bound, 
                                   time_for_occupancies=self._time_for_occupancies + current_state.get_time(),
                                   time_start=current_state.get_time(),
                                   wait_time=self._wait_time,
                                   initial_state=current_state, 
                                   logger=logger,
                                   heuristic_function=heuristic_function)
        # print("done creating")
        end_time = datetime.now()
        logger.log_time_elapsed("lrtdp_creation_time", (end_time - init_time).total_seconds())
        init_time = datetime.now()
        result = lrtdp.solve()
        end_time = datetime.now()
        logger.log_time_elapsed("lrtdp_planning_time", (end_time - init_time).total_seconds())
        # print("Result---------------------------------------------------")
        # print(result)
        # print("lrtdp.policy", lrtdp.policy)
        # print("current_state", current_state)
        # --current vertex:-- vertex1 --current time:-- 0 --already visited vertices:--  vertex1
        # --current vertex:-- vertex1 --current time:-- 0 --already visited vertices:--  vertex1
        # print("lrtdp.policy.keys()", lrtdp.policy.keys())
        # print("lrtdp.policy[current_state]", lrtdp.policy[str(current_state)])
        # if not result:
        #     return (False, None)
        # if lrtdp.policy == {}:
        #     return (True, None)
        # print("lrtdp.policy", lrtdp.policy)
        # print("lrtdp.policy")
        # for x in lrtdp.policy:
        #     print(x)
        return (result, lrtdp.policy)




def simulate_lrtdp(simulator, time, occupancy_map,  initial_state_name, writer, file, planner_time_bound, logger, convergence_threshold, heuristic_function):
    print("-------------------------------------lrtdp----------------------------------")
    initial_time = datetime.now()
    print("simulate_lrtdp: time", time)
    steps_lrtdp = simulator.simulate_lrtdp(time, 
                                           State(initial_state_name, 
                                                0, 
                                                set([initial_state_name]),
                                                set()),
                                            planner_time_bound, 
                                            convergence_threshold,
                                            logger, 
                                            simulate_planning_while_moving=False,
                                            heuristic_function=heuristic_function)
    print("=====================================end lrtdp==============================")
    time_used = datetime.now() - initial_time
    writer.writerow([time, "steps_lrtdp", steps_lrtdp[0], steps_lrtdp[1], time_used, steps_lrtdp[3], steps_lrtdp[2], len(occupancy_map.get_occupancy_levels())])
    file.flush()


def simulate_lrtdp_planning_while_moving(simulator, time, occupancy_map,  initial_state_name, writer, file, planner_time_bound, logger, convergence_threshold, heuristic_function):
    print("-------------------------------------lrtdp----------------------------------")
    initial_time = datetime.now()
    steps_lrtdp = simulator.simulate_lrtdp(time, 
                                           State(initial_state_name, 
                                                0, 
                                                set([initial_state_name])), 
                                            planner_time_bound, 
                                            convergence_threshold,
                                            logger,
                                            simulate_planning_while_moving=True,
                                            heuristic_function=heuristic_function)
    print("=====================================end lrtdp==============================")
    time_used = datetime.now() - initial_time
    writer.writerow([time, "steps_lrtdp_planning_while_moving", steps_lrtdp[0], steps_lrtdp[1], time_used, steps_lrtdp[3], steps_lrtdp[2], len(occupancy_map.get_occupancy_levels())])
    file.flush()