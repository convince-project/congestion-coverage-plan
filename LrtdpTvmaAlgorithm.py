from MDP import MDP, State
import datetime
from scipy.sparse import csr_array
from scipy.sparse.csgraph import shortest_path
import numpy as np
import Logger

class LrtdpTvmaAlgorithm():

    def __init__(self, occupancy_map, initial_state_name, convergence_threshold, time_bound_real, planner_time_bound, time_for_occupancies, time_start , vinitState=None, logger=None):
        self.occupancy_map = occupancy_map
        self.mdp = MDP(self.occupancy_map, time_for_occupancies, time_start)
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
        if logger is not None:
            self.logger = logger
        else:
            self.logger = Logger.Logger(print_time_elapsed=False)

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

    def get_policy(self):
        return self.policy

    def calculate_shortest_path(self, vertex1, vertex2):
        vertex1_number = int(vertex1[6:]) - 1
        vertex2_number = int(vertex2[6:]) - 1
        return self.shortest_paths_matrix[vertex1_number][vertex2_number]

    def calculate_shortest_path_matrix(self):
        mst_matrix = self.create_map_matrix()
        sp =shortest_path(mst_matrix)
        return sp 

    
    ### HEURISTIC FUNCTIONS
    def heuristic_teleport(self, state):
        value = 0
        initial_time = datetime.datetime.now()
        for vertex_id in (self.occupancy_map.get_vertices().keys() - state.get_visited_vertices()):
            value = value + self.minimum_edge_entering_vertices_dict[vertex_id]
        end_time = datetime.datetime.now()
        self.logger.log_time_elapsed("heuristic_teleport::time for calculating heuristic teleport", (end_time - initial_time).total_seconds())
        return value

    def heuristic_max_path(self, state):
        value = 0
        for vertex_id in (self.occupancy_map.get_vertices().keys() - state.get_visited_vertices()):
            value = max(value, self.calculate_shortest_path(state.get_vertex(), vertex_id))
        return value

    def get_policy(self):
        return self.policy

    def calculate_shortest_path(self, vertex1, vertex2):
        vertex1_number = int(vertex1[6:]) - 1
        vertex2_number = int(vertex2[6:]) - 1
        return self.shortest_paths_matrix[vertex1_number][vertex2_number]

    def calculate_shortest_path_matrix(self):
        mst_matrix = self.create_map_matrix()
        sp = shortest_path(mst_matrix)
        return sp 


    def heuristic(self, state):
        value = 0
        for vertex_id in (self.occupancy_map.get_vertices().keys() - state.get_visited_vertices()):
            value = value + self.calculate_shortest_path(state.get_vertex(), vertex_id)
        return value

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





    ### Q VALUES
    def calculate_Q(self, state, action):
        if self.goal(state):
            return 0
        time_initial = datetime.datetime.now()
        current_action_cost = 0
        future_actions_cost = 0
        # print("action:", action, "state", state.to_string())
        possible_transitions = self.mdp.get_possible_transitions_from_action(state, action, self.planner_time_bound)

        time_final = datetime.datetime.now()
        self.logger.log_time_elapsed("calculate_Q::time for getting possible transitions", (time_final - time_initial).total_seconds())
        # if len(possible_transitions) > 3:
        #     print("calculate_Q::possible transitions: ", len(possible_transitions))
        # print("calculate_Q::possible transitions:", [transition.to_string() for transition in possible_transitions])
        for transition in possible_transitions:
            time_initial = datetime.datetime.now()
            if transition.get_probability() == 0:
                continue

            local_current_action_cost = 0
            local_current_action_cost = transition.get_cost() * transition.get_probability()
            current_action_cost = current_action_cost + local_current_action_cost
            time_compute_next_state = datetime.datetime.now()
            next_state = self.mdp.compute_next_state(state, transition)
            time_final_compute_next_state = datetime.datetime.now()
            self.logger.log_time_elapsed("calculate_Q::time for computing next state", (time_final_compute_next_state - time_compute_next_state).total_seconds())
            time_compute_future_actions = datetime.datetime.now()
            local_future_actions_cost = self.get_value(next_state) * transition.get_probability()
            time_final_compute_future_actions = datetime.datetime.now()
            self.logger.log_time_elapsed("calculate_Q::time for computing future actions", (time_final_compute_future_actions - time_compute_future_actions).total_seconds())
            
            future_actions_cost = future_actions_cost + local_future_actions_cost
            time_final = datetime.datetime.now()
            self.logger.log_time_elapsed("calculate_Q::time for processing transition" + transition.to_string(), (time_final - time_initial).total_seconds())
        # self.qvalues[state.to_string() + action] = current_action_cost + future_actions_cost
        cost = current_action_cost + future_actions_cost
        # if cost  <= 0:
            # print("errorrrrr", cost, state.to_string(), action, current_action_cost, future_actions_cost)
            # print(len(possible_transitions))
            # for transition in possible_transitions:
            #     print(transition.get_cost(), transition.get_probability())

        return cost






    def calculate_current_action_cost(self, state, action):
        id = state.to_string() + action
        if id in self.action_costs:
            return self.action_costs[id]
        current_action_cost = 0
        possible_transitions = self.mdp.get_possible_transitions_from_action(State(state.get_vertex(), state.get_time(), state.get_visited_vertices().copy()), action.copy(), self.planner_time_bound)
        for transition in possible_transitions:
            local_current_action_cost = 0
            local_current_action_cost = transition.get_cost() * transition.get_probability()
            current_action_cost = current_action_cost + local_current_action_cost
        self.action_costs[id] = current_action_cost
        return current_action_cost




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
        return self.heuristic_teleport(state)
        # return self.heuristic_max_path(state)





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
        print("LRTDP TVMA started at: ", initial_current_time)
        average_trial_time = 0
        old_policy = None
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
            number_of_trials += 1
            average_trial_time = (average_trial_time * (number_of_trials - 1) + (time_final_trial - time_init_trial).total_seconds()) / number_of_trials
            if number_of_trials % 10000 == 0:
                print("Average trial time after " + str(number_of_trials) + " trials: ", average_trial_time)
            if old_policy == self.policy:
                print("Policy has not changed.")
            old_policy = self.policy.copy()
        print(str(number_of_trials) + " trials")
        return self.solved(self.vinitState)



    def lrtdp_tvma_trial(self, vinitStateParameter, thetaparameter, planner_time_bound):
            # print("trial started")
            visited = [] # this is a stack
            state = vinitStateParameter
            while not self.solved(state):
                visited.append(state)
                self.update(state)
                if self.goal(state) or (state.get_time() > planner_time_bound):
                    ######## should there be here a bellamn backup?
                    break
                # perform bellman backup and update policy
                time_initial = datetime.datetime.now()
                self.policy[state.to_string()] = self.calculate_argmin_Q(state)
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
                    break
            time_final = datetime.datetime.now()
            self.logger.log_time_elapsed("lrtdp_tvma_trial::time for backward check", (time_final - time_initial).total_seconds())
