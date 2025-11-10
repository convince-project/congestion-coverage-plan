from congestion_coverage_plan.mdp.MDP import MDP, State
import datetime
from scipy.sparse import csr_array
from scipy.sparse.csgraph import shortest_path, minimum_spanning_tree
import numpy as np
from congestion_coverage_plan.utils import Logger
from congestion_coverage_plan.hamiltonian_path.hamiltonian_path import create_matrix_from_vertices_list_for_mst,  create_matrix_from_vertices_list, solve_with_google_with_data, create_data_model_from_matrix, create_matrix_from_vertices_list_from_shortest_path_matrix_tsp, create_matrix_from_vertices_list_for_mst
import sys
class LrtdpTvmaAlgorithm():

    def __init__(self, 
                 occupancy_map, 
                 initial_state_name,
                 convergence_threshold, 
                 time_bound_real, 
                 planner_time_bound, 
                 time_for_occupancies, 
                 time_start , 
                 wait_time, 
                 heuristic_function, 
                 vinitState=None, 
                 logger=None):
        self.occupancy_map = occupancy_map

        self.mdp = MDP(occupancy_map=occupancy_map, 
                       time_for_occupancies=time_for_occupancies, 
                       time_start=time_start, 
                       wait_time=wait_time)
        self._wait_time = wait_time
        self.initial_time = time_for_occupancies
        self.time_for_occupancies = time_for_occupancies
        if vinitState is not None:
            self.vinitState = vinitState
            self.initial_time = time_for_occupancies
        else:
            self.vinitState = State(initial_state_name, 
                                   0,
                                    set([initial_state_name]))
        self.vinitStateName = initial_state_name
        self.time_bound_real = time_bound_real
        self.planner_time_bound = planner_time_bound
        self.convergenceThresholdGlobal = convergence_threshold
        self.policy = {}
        self.valueFunction = {}
        self.action_costs = {}
        self.solved_set = set()
        self.shortest_paths_matrix = self.calculate_shortest_path_matrix()
        self.minimum_edge_entering_vertices_dict = self.minimum_edge_entering_vertices()
        if heuristic_function == "teleport":
            self.heuristic_function = self.heuristic_teleport
        elif heuristic_function == "mst_shortest_path":
            self.heuristic_function = self.heuristic_mst_shortest_path
        elif heuristic_function == "mst":
            self.heuristic_function = self.heuristic_mst
        elif heuristic_function == "hamiltonian_path":
            self.heuristic_function = self.heuristic_hamiltonian_path
        elif heuristic_function == "hamiltonian_path_with_shortest_path":
            self.heuristic_function = self.heuristic_hamiltonian_path_with_shortest_path
        else:
            print("Heuristic function not recognized")
            sys.exit(1)

        if logger is not None:
            self.logger = logger
        else:
            self.logger = Logger.Logger(print_time_elapsed=False)
        self.heuristic_backup = {}

    ### HEURISTIC HELPERS
    def minimum_edge_entering_vertices(self):
        vertices = self.occupancy_map.get_vertices()
        minimum_edge_entering_vertices = {}
        for vertex_id in vertices.keys():
            for edge in self.occupancy_map.get_edges_from_vertex_with_edge_class(vertex_id):
                if edge.get_length() is not None:
                    if vertex_id not in minimum_edge_entering_vertices:
                        minimum_edge_entering_vertices[vertex_id] = edge.get_length()
                    else:
                        if edge.get_length() < minimum_edge_entering_vertices[vertex_id]:
                            minimum_edge_entering_vertices[vertex_id] = edge.get_length()
        return minimum_edge_entering_vertices


    def create_current_shortest_path_matrix(self, state):
        # create a matrix without the visited vertices
        matrix = create_matrix_from_vertices_list(list(set(self.occupancy_map.get_vertices_list()) - state.get_visited_vertices()) + [state.get_vertex()], self.occupancy_map, state.get_vertex())
        # compute MST
        sp = shortest_path(csr_array(matrix))
        # def calculate_current_shortest_path_matrix(self, state):
        return sp


    def create_current_shortest_path_matrix_for_tsp(self, state):
        # print(self.shortest_paths_matrix)
        matrix = create_matrix_from_vertices_list_from_shortest_path_matrix_tsp(vertices_ids=list(
                                                                                set(self.occupancy_map.get_vertices_list()) -
                                                                                state.get_visited_vertices()) + 
                                                                                [state.get_vertex()], 
                                                                            occupancy_map=self.occupancy_map, 
                                                                            shortest_path_matrix=self.shortest_paths_matrix, 
                                                                            initial_vertex_id=state.get_vertex(), 
                                                                            value_for_not_existent_edge=99999999)
        return matrix


    def create_current_mst_matrix_from_shortest_path(self, state):
        # create a matrix without the visited vertices
        matrix = create_matrix_from_vertices_list_for_mst(vertices_ids=list(set(self.occupancy_map.get_vertices_list()) - state.get_visited_vertices()) + [state.get_vertex()], 
                                                          occupancy_map=self.occupancy_map, 
                                                          initial_vertex_id=state.get_vertex(), 
                                                          shortest_path_matrix=self.shortest_paths_matrix, 
                                                          value_for_not_existent_edge=np.inf)
        mst = minimum_spanning_tree(csr_array(matrix))
        return mst.toarray().astype(float)


    def create_current_mst_matrix(self, state):
        # create a matrix without the visited vertices
        matrix = create_matrix_from_vertices_list_for_mst(vertices_ids=list(set(self.occupancy_map.get_vertices_list()) - state.get_visited_vertices()) + [state.get_vertex()], 
                                                          occupancy_map=self.occupancy_map, 
                                                          initial_vertex_id=state.get_vertex(), 
                                                          value_for_not_existent_edge=99999999)
        # compute MST
        mst = minimum_spanning_tree(csr_array(matrix))
        return mst.toarray().astype(float)


    def calculate_shortest_path(self, vertex1, vertex2):
        vertex1_number = int(vertex1[6:]) - 1
        vertex2_number = int(vertex2[6:]) - 1
        return self.shortest_paths_matrix[vertex1_number][vertex2_number]


    def calculate_shortest_path_matrix(self):
        mst_matrix = self.create_map_matrix()
        sp = shortest_path(mst_matrix)
        return sp 


    def create_map_matrix(self):
        vertices = self.occupancy_map.get_vertices()
        mst_matrix = []
        for vertex in vertices.keys():
            mst_matrix_line = []
            for vertex2 in vertices.keys():
                if vertex == vertex2:
                    mst_matrix_line.append(0)
                elif self.occupancy_map.find_edge_from_position(vertex, vertex2) is not None:
                    edge_id = self.occupancy_map.find_edge_from_position(vertex, vertex2).get_id()
                    mst_matrix_line.append(self.occupancy_map.get_edge_traverse_time(edge_id)['zero'])
                else:
                    mst_matrix_line.append(99999999)
            mst_matrix.append(mst_matrix_line)
        return csr_array(mst_matrix)


    ### HEURISTIC FUNCTIONS
    def heuristic_hamiltonian_path_with_shortest_path(self, state):
        if self.goal(state):
            return 0
        matrix = self.create_current_shortest_path_matrix_for_tsp(state)
        # print("matrix for hamiltonian path heuristic:", matrix)
        data = create_data_model_from_matrix(matrix)
        cost = solve_with_google_with_data(data)
        if cost is not None:
            return cost
        else:
            print("ERRORRRRR: cost is none, this should not happen")
            return None


    def heuristic_mst(self, state):
        if self.goal(state):
            return 0
        mst_matrix = self.create_current_mst_matrix(state)
        # check if all the states are connected
        
        # print("matrix for mst heuristic:", mst_matrix)
        cost = np.sum(mst_matrix[mst_matrix != 0])
        if cost is not None:
            return cost
        else:
            print("ERRORRRRR: cost is none, this should not happen")
            return None
        # return cost if cost is not None else 9999999


    def heuristic_mst_shortest_path(self, state):
        if self.goal(state):
            return 0
        mst_matrix = self.create_current_mst_matrix_from_shortest_path(state)
        # check if all the states are connected
        
        # print("matrix for mst heuristic:", mst_matrix)
        cost = np.sum(mst_matrix[mst_matrix != 0])
        if cost is not None:
            return cost
        else:
            print("ERRORRRRR: cost is none, this should not happen")
            return None
        # return cost if cost is not None else 9999999


    def heuristic_hamiltonian_path(self, state):
        if self.goal(state):
            return 0
        matrix = create_matrix_from_vertices_list(vertices_ids=list(set(self.occupancy_map.get_vertices_list()) - state.get_visited_vertices()) + [state.get_vertex()], 
                                                  occupancy_map=self.occupancy_map, 
                                                  initial_vertex_id=state.get_vertex(),
                                                  value_for_not_existent_edge=99999999)
                                                #   value_for_not_existent_edge=np.array([np.inf]).astype(int)[0])
        # print("matrix for hamiltonian path heuristic:", matrix)
        data = create_data_model_from_matrix(matrix)
        cost = solve_with_google_with_data(data)
        return cost if cost is not None else 9999999


    def heuristic_teleport(self, state):
        value = 0
        initial_time = datetime.datetime.now()
        # if self.goal(state):
        #     return 0
        for vertex_id in (self.occupancy_map.get_vertices().keys() - state.get_visited_vertices()):
            value = value + self.minimum_edge_entering_vertices_dict[vertex_id]
        end_time = datetime.datetime.now()
        self.logger.log_time_elapsed("heuristic_teleport::time for calculating heuristic teleport", (end_time - initial_time).total_seconds())
        return value



    ### HELPERS
    def get_policy(self):
        return self.policy


    ### Q VALUES
    def calculate_Q(self, state, action):
        if self.goal(state):
            return 0
        
        current_action_cost = 0
        future_actions_cost = 0

        possible_transitions = self.mdp.get_possible_transitions_from_action(state, action, self.planner_time_bound)

        for transition in possible_transitions:

            if transition.get_probability() == 0:
                continue
            # if transition.get_occupancy_level() != "none" and transition.get_occupancy_level() != "zero":
            #     print("calculate_Q::transition with occupancy level:", transition.to_string())
            # print("calculate_Q::transition with occupancy level:", transition.to_string())
            local_current_action_cost = 0
            local_current_action_cost = transition.get_cost() * transition.get_probability()
            current_action_cost = current_action_cost + local_current_action_cost

            next_state = self.mdp.compute_next_state(state, transition)
            local_future_actions_cost = self.get_value(next_state) * transition.get_probability()
            
            future_actions_cost = future_actions_cost + local_future_actions_cost
        # self.qvalues[state.to_string() + action] = current_action_cost + future_actions_cost
        cost = current_action_cost + future_actions_cost
        # if cost  <= 0:
            # print("errorrrrr", cost, state.to_string(), action, current_action_cost, future_actions_cost)
            # print(len(possible_transitions))
            # for transition in possible_transitions:
            #     print(transition.get_cost(), transition.get_probability())
        # if state.get_time() == 0:
        #     print("Q value for state:", state.to_string(), "action:", action, "current action cost:", current_action_cost, "future actions cost:", future_actions_cost, "is:", cost)

        return cost


    def calculate_argmin_Q(self, state):
        qvalues = []
        state_internal = State(state.get_vertex(), state.get_time(), state.get_visited_vertices().copy())
        time_initial = datetime.datetime.now()
        possible_actions = self.mdp.get_possible_actions(state_internal)
        if not possible_actions:
            print("NO POSSIBLE ACTIONS???")
            return (0, state_internal, "")
        time_final = datetime.datetime.now()
        self.logger.log_time_elapsed("calculate_argmin_Q::time for getting possible actions", (time_final - time_initial).total_seconds())

        # actions_sorted = list(possible_actions)
        # actions_sorted.sort()
        time_initial = datetime.datetime.now()
        for action in possible_actions:
            qvalues.append((self.calculate_Q(state_internal, action), state_internal, action))
            # if state.get_time() == 0:
                # print("Q value for state:", state_internal.to_string(), "action:", action, "is:", qvalues[-1][0])
        self.logger.log_time_elapsed("calculate_argmin_Q::time for calculating Q values", (time_final - time_initial).total_seconds())

        time_initial = datetime.datetime.now()
        min = None
        # min = np.min(qvalues, key=lambda x: x[0])  # Find the minimum Q value
        for qvalue in qvalues:
            if min is None:
                min = qvalue
            else:
                if qvalue[0] < min[0]:
                    min = qvalue
        time_final = datetime.datetime.now()
        self.logger.log_time_elapsed("calculate_argmin_Q::time for finding minimum Q value", (time_final - time_initial).total_seconds())
        # if min[0] <= 0:
        #     print("goal")
        return (min[0], min[1], min[2]) # this contains the value, state and action with the minimum Q value


    ### STATE FUNCTIONS
    def update(self, state):
        action = self.greedy_action(state)
        self.valueFunction[state.to_string()] = action[0]  # this is the value of the state
        return True


    def greedy_action(self, state):
        return self.calculate_argmin_Q(state)


    def residual(self, state):
        # print("Residual for state:", state.to_string())

        action = self.greedy_action(state)
        residual = abs(self.get_value(state) - action[0])
        # if residual > 0.01:
        #     print("Residual for state:", state.to_string(), "======", residual, "GOAL?  ", self.goal(state))
        # if residual < 0.0001:
        #     print("**************************", action[0], action[1].to_string(), action[2])
        #     print(state.to_string())
        #     print()
        return residual


    def solved(self, state):
        return state.to_string() in self.solved_set


    def get_value(self, state):
        if state.to_string() in self.valueFunction:
            return self.valueFunction[state.to_string()]
        if state.to_string() in self.heuristic_backup:
            return self.heuristic_backup[state.to_string()]
        heuristic_value = self.heuristic_function(state)
        self.heuristic_backup[state.to_string()] = heuristic_value
        return heuristic_value


    def goal(self, state):
        is_goal = self.mdp.solved(state)
        return is_goal


    def check_solved(self, state, thetaparameter):
        # print("Checking if state is solved: ", state.to_string())
        solved_condition = True
        open = []
        closed = []
        open.append(state)
        while open != []:
            state = open.pop()
            closed.append(state)
            if self.residual(state) > thetaparameter: # or state.get_time() > self.planner_time_bound:
                solved_condition = False
                continue

            action = self.greedy_action(state)[2] # get the greedy action for the state            
            for transition in self.mdp.get_possible_transitions_from_action(state, action, self.planner_time_bound):
                next_state = self.mdp.compute_next_state(state, transition)
                if not (next_state in open or next_state in closed) and not self.solved(next_state): # and not self.goal(state): # and next_state.get_time() <= self.planner_time_bound: # and not self.goal(next_state):
                    open.append(next_state)
        if solved_condition:
            for state in closed:
                self.solved_set.add(state.to_string())
        else:
            while closed:
                state = closed.pop()
                self.update(state)
        return solved_condition


    def calculate_most_probable_transition(self, state, action):
        most_probable_transitions = []

        for transition in self.mdp.get_possible_transitions_from_action(state, action, self.planner_time_bound):
            if transition.get_probability() > 0:
                if most_probable_transitions == []:
                    most_probable_transitions.append(transition)
                else:
                    if transition.get_probability() < most_probable_transitions[0].get_probability():
                        most_probable_transitions = []
                        most_probable_transitions.append(transition)
                    elif transition.get_probability() == most_probable_transitions[0].get_probability():
                        most_probable_transitions.append(transition)
        most_probable_transition_to_return = None

        if len(most_probable_transitions) > 1:
            # get the one with the lowest cost
            min_cost = None
            for transition in most_probable_transitions:
                if min_cost is None:
                    min_cost = transition.get_cost()
                    most_probable_transition_to_return = transition
                else:
                    if transition.get_cost() < min_cost:
                        min_cost = transition.get_cost()
                        most_probable_transition_to_return = transition
        else:
            most_probable_transition_to_return = most_probable_transitions[0]
        return most_probable_transition_to_return


    def lrtdp_tvma(self):
        number_of_trials = 0
        self.occupancy_map.predict_occupancies(self.time_for_occupancies, self.time_for_occupancies + self.planner_time_bound)
        self.occupancy_map.calculate_current_occupancies(self.time_for_occupancies)
        initial_current_time = datetime.datetime.now()
        # for edge_id in self.occupancy_map.get_edges().keys():
        #     # print the current occupancies for each edge
        # occ = self.occupancy_map.get_current_occupancies(edge_id)
        # if occ is not None:
        #     print("Edge: ", edge_id, "occupancy levels: ", occ)
            # print("Edge: ", edge_id, "occupancy levels: ", occ)
        print("LRTDP TVMA started at: ", initial_current_time, "convergence threshold:", self.convergenceThresholdGlobal, "wait_time:", self._wait_time, "planner time bound:", self.planner_time_bound, "real time bound:", self.time_bound_real, "initial time for occupancies:", self.time_for_occupancies)
        average_trial_time = 0
        old_policy = None
        old_time = None
        while (not self.solved(self.vinitState)) and ((datetime.datetime.now() - initial_current_time)) < datetime.timedelta(seconds = self.time_bound_real):
            time_init_trial = datetime.datetime.now()
            # print("Trial number: ", number_of_trials)
            self.lrtdp_tvma_trial(self.vinitState, self.convergenceThresholdGlobal, self.planner_time_bound)
            # print(self.valueFunction)
            # print(self.policy)
            # for item in self.policy.keys():
            #     print("***state***", item, "***qvalue***", self.policy[item][0], "***action***", self.policy[item][2])
            time_final_trial = datetime.datetime.now()
            self.logger.log_time_elapsed("trial time", (time_final_trial - time_init_trial).total_seconds())
            # print("Trial ", number_of_trials, " time: ", (time_final_trial - time_init_trial).total_seconds())
            number_of_trials += 1
            average_trial_time = (average_trial_time * (number_of_trials - 1) + (time_final_trial - time_init_trial).total_seconds()) / number_of_trials
            if number_of_trials % 50 == 0:
                print("Average trial time after " + str(number_of_trials) + " trials: ", average_trial_time)
                print(len(self.policy), "states in policy")
                # print("Current policy: ", self.policy)
                print(len(self.valueFunction), "states in value function")
            # if old_policy == self.policy[self.vinitState.to_string()][2] and old_time == self.policy[self.vinitState.to_string()][0]:
            #     print("Policy has not changed.", old_policy, "**", old_time)
            # else:
            #     print("Policy has changed.", old_policy, "**", old_time, "->", self.policy[self.vinitState.to_string()][2], "**", self.policy[self.vinitState.to_string()][0])
            old_policy = self.policy[self.vinitState.to_string()][2] if self.vinitState.to_string() in self.policy else None
            old_time = self.policy[self.vinitState.to_string()][0] if self.vinitState.to_string() in self.policy else None
        print(str(number_of_trials) + " trials")
        print(len(self.policy), "states in policy")
        print(len(self.valueFunction), "states in value function")
        return self.solved(self.vinitState)


    def lrtdp_tvma_trial(self, vinitStateParameter, thetaparameter, planner_time_bound):
            # print("trial started")
            visited = [] # this is a stack
            state = vinitStateParameter
            while not self.solved(state):
                # print("checking state:", state.to_string())

                visited.append(state)
                self.update(state)
                self.policy[state.to_string()] = self.calculate_argmin_Q(state)
                if self.goal(state) or (state.get_time() > planner_time_bound):
                    ######## should there be here a bellamn backup?
                    break
                # perform bellman backup and update policy
                time_initial = datetime.datetime.now()
                time_final = datetime.datetime.now()
                self.logger.log_time_elapsed("lrtdp_tvma_trial::time for argmin", (time_final - time_initial).total_seconds())
                # print("state: ", state.to_string())
                # print("action: ", self.policy[state.to_string()][2])
                time_initial = datetime.datetime.now()
                action = self.policy[state.to_string()][2]
                transitions = self.mdp.get_possible_transitions_from_action(state, action, self.planner_time_bound)
                if not transitions:
                    print("lrtdp_tvma_trial::No transitions found for state: ", state.to_string())
                    break
                time_final = datetime.datetime.now()
                self.logger.log_time_elapsed("lrtdp_tvma_trial::time for transitions", (time_final - time_initial).total_seconds())
                # for t in transitions:
                #     print("transition: ", t.to_string())
                time_initial = datetime.datetime.now()
                transition_selected = np.random.choice(transitions, p=[t.get_probability() for t in transitions])

                time_final = datetime.datetime.now()
                self.logger.log_time_elapsed("lrtdp_tvma_trial::time for transition selection", (time_final - time_initial).total_seconds())
                time_initial = datetime.datetime.now()
                state = self.mdp.compute_next_state(state, transition_selected)
                time_final = datetime.datetime.now()
                self.logger.log_time_elapsed("lrtdp_tvma_trial::time for next state computation", (time_final - time_initial).total_seconds())
                # print("next state: ", state.to_string())
            time_initial = datetime.datetime.now()
            while visited:
                state = visited.pop()
                # print("in while 2")
                if not self.check_solved(state, thetaparameter):
                    # print("State not solved: ", state.to_string(), "======", self.residual(state), "GOAL?  ", self.goal(state))
                    # print(len(visited), "states in visited stack")
                    break
            time_final = datetime.datetime.now()
            self.logger.log_time_elapsed("lrtdp_tvma_trial::time for backward check", (time_final - time_initial).total_seconds())
