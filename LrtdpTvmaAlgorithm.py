from MDP import MDP, State
import datetime
from scipy.sparse import csr_array
from scipy.sparse.csgraph import shortest_path
import numpy as np

class LrtdpTvmaAlgorithm():

    def __init__(self, occupancy_map, initial_state_name, convergence_threshold, time_bound_real, planner_time_bound, time_for_occupancies, time_start , vinitState=None, print_times=False):
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
                                   (self.occupancy_map.find_vertex_from_id(initial_state_name).get_posx(), 
                                    self.occupancy_map.find_vertex_from_id(initial_state_name).get_posy()),
                                    set([initial_state_name]))
        self.vinitStateName = initial_state_name
        self.time_bound_real = time_bound_real
        self.planner_time_bound = planner_time_bound
        self.convergenceThresholdGlobal = convergence_threshold
        self.policy = {}
        self.valueFunction = {}
        self.solved_set = set()
        self.shortest_paths_matrix = self.calculate_shortest_path_matrix()
        self.minimum_edge_entering_vertices_dict = self.minimum_edge_entering_vertices()
        self.print_times = print_times # set to True to print times for debugging purposes

    def minimum_edge_entering_vertices(self):
        vertices = self.occupancy_map.get_vertices_list()
        minimum_edge_entering_vertices = {}
        for vertex in vertices:
            for edge in self.occupancy_map.get_edges_from_vertex_with_edge_class(vertex.get_id()):
                if edge.get_length() is not None:
                    if vertex.get_id() not in minimum_edge_entering_vertices:
                        minimum_edge_entering_vertices[vertex.get_id()] = edge.get_length()
                    else:
                        if edge.get_length() < minimum_edge_entering_vertices[vertex.get_id()]:
                            minimum_edge_entering_vertices[vertex.get_id()] = edge.get_length()
            
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
        for vertex in self.occupancy_map.get_vertices_list():
            if vertex.get_id() not in state.get_visited_vertices():
                value = value + self.minimum_edge_entering_vertices_dict[vertex.get_id()]
        return value

    def heuristic_max_path(self, state):
        value = 0
        for vertex in self.occupancy_map.get_vertices_list():
            if vertex.get_id() not in state.get_visited_vertices():
                value = max(value, self.calculate_shortest_path(state.get_vertex(), vertex.get_id()))
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
        for vertex in self.occupancy_map.get_vertices_list():
            if vertex.get_id() not in state.get_visited_vertices():
                value = value + self.calculate_shortest_path(state.get_vertex(), vertex.get_id())
        return value

    def create_map_matrix(self):
        vertices = self.occupancy_map.get_vertices_list()
        mst_matrix = []
        for vertex in vertices:
            mst_matrix_line = []
            for vertex2 in vertices:
                if vertex.get_id() == vertex2.get_id():
                    mst_matrix_line.append(0)
                elif self.occupancy_map.find_edge_from_position(vertex.get_id(), vertex2.get_id()) is not None:
                    edge_id = self.occupancy_map.find_edge_from_position(vertex.get_id(), vertex2.get_id()).get_id()
                    mst_matrix_line.append(self.occupancy_map.get_edge_traverse_time(edge_id)['zero'])
                else:
                    mst_matrix_line.append(99999999)
            mst_matrix.append(mst_matrix_line)
        return csr_array(mst_matrix)





    ### Q VALUES
    def calculate_Q(self, state, action):
        if self.goal(state):
            return 0
        if self.print_times:
            time_initial = datetime.datetime.now()
        current_action_cost = 0
        future_actions_cost = 0
        possible_transitions = self.mdp.get_possible_transitions_from_action(state, action, self.planner_time_bound)
        if self.print_times:
            time_final = datetime.datetime.now()
            print("calculate_Q::time for getting possible transitions: " + str((time_final - time_initial).total_seconds()))

        for transition in possible_transitions:
            if self.print_times:
                time_initial = datetime.datetime.now()
            if transition.get_probability() == 0:
                continue

            local_current_action_cost = 0
            local_current_action_cost = transition.get_cost() * transition.get_probability()
            current_action_cost = current_action_cost + local_current_action_cost
            next_state = self.mdp.compute_next_state(state, transition)
            local_future_actions_cost = self.get_value(next_state) * transition.get_probability()
            future_actions_cost = future_actions_cost + local_future_actions_cost
            if self.print_times:
                time_final = datetime.datetime.now()
                print("calculate_Q::time for processing transition: " + str((time_final - time_initial).total_seconds()))
        # self.qvalues[state.to_string() + action] = current_action_cost + future_actions_cost
        return current_action_cost + future_actions_cost 






    def calculate_current_action_cost(self, state, action):
        current_action_cost = 0
        possible_transitions = self.mdp.get_possible_transitions_from_action(state, action, self.planner_time_bound)
        for transition in possible_transitions:
            local_current_action_cost = 0
            local_current_action_cost = transition.get_cost() * transition.get_probability()
            current_action_cost = current_action_cost + local_current_action_cost
        return current_action_cost




    def calculate_argmin_Q(self, state):
        qvalues = []
        if self.print_times:
            time_initial = datetime.datetime.now()
        possible_actions = self.mdp.get_possible_actions(state)
        if not possible_actions:
            return (0, state, "")
        if self.print_times:
            time_final = datetime.datetime.now()
            print("calculate_argmin_Q::time for getting possible actions: " + str((time_final - time_initial).total_seconds()))

        # actions_sorted = list(possible_actions)
        # actions_sorted.sort()
        if self.print_times:
            time_initial = datetime.datetime.now()
        for action in possible_actions:
            qvalues.append((self.calculate_Q(state, action),state, action))
        if self.print_times:
            time_final = datetime.datetime.now()
            print("calculate_argmin_Q::time for calculating Q values: " + str((time_final - time_initial).total_seconds()))

        if self.print_times:
            time_initial = datetime.datetime.now()
        min = None
        for qvalue in qvalues:
            if min is None:
                min = qvalue
            else:
                if qvalue[0] < min[0]:
                    min = qvalue
        if self.print_times:
            time_final = datetime.datetime.now()
            print("calculate_argmin_Q::time for finding minimum Q value: " + str((time_final - time_initial).total_seconds()))
        return (min[0], min[1], min[2]) # in this case I copy the value




    ### STATE FUNCTIONS
    def update(self, state):
        action = self.greedy_action(state)
        self.valueFunction[state.to_string()] = self.calculate_Q(state, action)
        return True




    def greedy_action(self, state):
        return self.calculate_argmin_Q(state)[2]




    def residual(self, state):
        action = self.greedy_action(state)
        return abs(self.get_value(state) - self.calculate_Q(state, action))




    def solved(self, state):
        return state.to_string() in self.solved_set    


    def get_value(self, state):
        if state.to_string() in self.valueFunction:
            return self.valueFunction[state.to_string()]
        return self.heuristic_teleport(state)
        # return self.heuristic_max_path(state)





    def goal(self, state):
        return len(state.get_visited_vertices()) == len(self.occupancy_map.get_vertices_list())




    def check_solved(self, state, thetaparameter):
        solved_condition = True
        open = []
        closed = []
        open.append(state)
        while open != []:
            state = open.pop()
            closed.append(state)
            if self.print_times:
                time_initial = datetime.datetime.now()
            if self.residual(state) > thetaparameter:
                solved_condition = False
                continue
            if self.print_times:
                time_final = datetime.datetime.now()
                print("check_solved::time for residual: " + str((time_final - time_initial).total_seconds()))

            if self.print_times:
                time_initial = datetime.datetime.now()
            action = self.greedy_action(state) # get the greedy action for the state
            if self.print_times:
                time_final = datetime.datetime.now()
                print("check_solved::time for greedy action: " + str((time_final - time_initial).total_seconds()))
            if self.print_times:
                time_initial = datetime.datetime.now()
            for transition in self.mdp.get_possible_transitions_from_action(state, action, self.planner_time_bound):
                next_state = self.mdp.compute_next_state(state, transition)
                if not (next_state in open or next_state in closed) and not self.solved(next_state): # and next_state.get_time() <= self.planner_time_bound:
                    open.append(next_state)
            if self.print_times:
                time_final = datetime.datetime.now()
                print("check_solved::time for transitions: " + str((time_final - time_initial).total_seconds()))
        if solved_condition:
            if self.print_times:
                time_initial = datetime.datetime.now()
            for state in closed:
                self.solved_set.add(state.to_string())
            if self.print_times:
                time_final = datetime.datetime.now()
                print("check_solved::time for adding to solved set: " + str((time_final - time_initial).total_seconds()))
        else:
            if self.print_times:
                time_initial = datetime.datetime.now()
            while closed:
                state = closed.pop()
                self.update(state)
            if self.print_times:
                time_final = datetime.datetime.now()
                print("check_solved::time for backward update in check solved: " + str((time_final - time_initial).total_seconds()))
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

        while (not self.solved(self.vinitState)) and ((datetime.datetime.now() - initial_current_time)) < datetime.timedelta(seconds = self.time_bound_real):
            if self.print_times:
                time_init_trial = datetime.datetime.now()
            self.lrtdp_tvma_trial(self.vinitState, self.convergenceThresholdGlobal, self.planner_time_bound)
            if self.print_times:
                time_final_trial = datetime.datetime.now()
                print("trial time: " + str((time_final_trial - time_init_trial).total_seconds()))
            number_of_trials += 1
        if self.print_times:
            print(str(number_of_trials) + " trials")
        return self.solved(self.vinitState)



    def lrtdp_tvma_trial(self, vinitStateParameter, thetaparameter, planner_time_bound):
            visited = [] # this is a stack
            state = vinitStateParameter
            while not self.solved(state):
                visited.append(state)
                self.update(state)
                if self.goal(state) or (state.get_time() > planner_time_bound):
                    ######## should there be here a bellamn backup?
                    break
                # perform bellman backup and update policy
                if self.print_times:
                    time_initial = datetime.datetime.now()
                self.policy[state.to_string()] = self.calculate_argmin_Q(state)
                if self.print_times:
                    time_final = datetime.datetime.now()
                    print("lrtdp_tvma_trial::time for argmin: " + str((time_final - time_initial).total_seconds()))
                # print("state: ", state.to_string())
                # print("action: ", self.policy[state.to_string()][2])
                if self.print_times:
                    time_initial = datetime.datetime.now()
                transitions = self.mdp.get_possible_transitions_from_action(state, self.policy[state.to_string()][2], self.planner_time_bound)
                if not transitions:
                    print("lrtdp_tvma_trial::No transitions found for state: ", state.to_string())
                if self.print_times:
                    time_final = datetime.datetime.now()
                    print("lrtdp_tvma_trial::time for transitions: " + str((time_final - time_initial).total_seconds()))
                # for t in transitions:
                #     print("transition: ", t.to_string())
                if self.print_times:
                    time_initial = datetime.datetime.now()
                transition_selected = np.random.choice(transitions, p=[t.get_probability() for t in transitions])

                if self.print_times:
                    time_final = datetime.datetime.now()
                    print("lrtdp_tvma_trial::time for transition selection: " + str((time_final - time_initial).total_seconds()))
                    time_initial = datetime.datetime.now()
                state = self.mdp.compute_next_state(state, transition_selected)
                if self.print_times:
                    time_final = datetime.datetime.now()
                    print("lrtdp_tvma_trial::time for next state computation: " + str((time_final - time_initial).total_seconds()))
                # print("next state: ", state.to_string())
            if self.print_times:
                time_initial = datetime.datetime.now()
            while visited:
                state = visited.pop()
                # print("in while 2")
                if not self.check_solved(state, thetaparameter):
                    break
            if self.print_times:
                time_final = datetime.datetime.now()
                print("time for backward check: " + str((time_final - time_initial).total_seconds()))
