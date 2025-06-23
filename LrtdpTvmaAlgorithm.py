from MDP import MDP, State, Transition
import datetime
from scipy.sparse import csr_array
from scipy.sparse.csgraph import minimum_spanning_tree, shortest_path
import logging
import matplotlib.pyplot as plt

class LrtdpTvmaAlgorithm():

    def __init__(self, occupancy_map, initial_state_name, convergence_threshold, time_bound_real, planner_time_bound, time_for_occupancies, time_start ,  vinitState=None):
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


    def minimum_edge_entering_vertices(self):
        vertices = self.occupancy_map.get_vertices_list()
        minimum_edge_entering_vertices = {}
        for vertex in vertices:
            for edge in self.occupancy_map.get_edges_from_vertex(vertex.get_id()):
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
        # print("heuristic::state: ", state.to_string())
        value = 0
        for vertex in self.occupancy_map.get_vertices_list():
            if vertex.get_id() not in state.get_visited_vertices():
                value = value + self.minimum_edge_entering_vertices_dict[vertex.get_id()]
        return value

    def heuristic_max_path(self, state):
        # print("heuristic::state: ", state.to_string())
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
        sp =shortest_path(mst_matrix)
        return sp 


    def heuristic(self, state):
        # value = 0
        # for vertex in self.occupancy_map.get_vertices_list():
        #     if vertex.get_id() not in state.get_visited_vertices():
        #         value = value + self.minimum_edge_entering_vertices_dict[vertex.get_id()]
        # return value
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
                    edge_id = self.occupancy_map.find_edge_from_position(vertex.get_id(), vertex2.get_id())
                    mst_matrix_line.append(self.occupancy_map.get_edge_traverse_time(edge_id)['zero'])
                else:
                    mst_matrix_line.append(99999999)
            mst_matrix.append(mst_matrix_line)
        return csr_array(mst_matrix)

    ### Q VALUES
    def calculate_Q(self, state, action):

        if self.goal(state):
            return 0

        current_action_cost = 0
        future_actions_cost = 0
        possible_transitions = self.mdp.get_possible_transitions_from_action(state, action)

        for transition in possible_transitions:

            if transition.get_probability() == 0:
                continue

            local_current_action_cost = 0
            local_current_action_cost = transition.get_cost() * transition.get_probability()
            current_action_cost = current_action_cost + local_current_action_cost
            next_state = self.mdp.compute_next_state(state, transition)
            local_future_actions_cost = self.get_value(next_state) * transition.get_probability()
            future_actions_cost = future_actions_cost + local_future_actions_cost

        return current_action_cost + future_actions_cost 


    def calculate_current_action_cost(self, state, action):
        current_action_cost = 0
        possible_transitions = self.mdp.get_possible_transitions_from_action(state, action)
        for transition in possible_transitions:
            local_current_action_cost = 0
            local_current_action_cost = transition.get_cost() * transition.get_probability()
            current_action_cost = current_action_cost + local_current_action_cost
        return current_action_cost

    def calculate_argmin_Q(self, state):
        qvalues = []
        possible_actions = self.mdp.get_possible_actions(state)

        if not possible_actions:
            return (0, state, "")

        actions_sorted = list(possible_actions)
        actions_sorted.sort()

        for action in actions_sorted:
            qvalues.append((self.calculate_Q(state, action),state, action))

        min = None

        for qvalue in qvalues:
            if min is None:
                min = qvalue
            else:
                if qvalue[0] < min[0]:
                    min = qvalue

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
        # print("heuristic teleport", self.heuristic_teleport(state))
        # print("heuristic max path", self.heuristic_max_path(state))

        return self.heuristic_max_path(state)


    def goal(self, state):

        for vertex in self.occupancy_map.get_vertices_list():
            if vertex.get_id() not in state.get_visited_vertices():
                return False
        if state.get_time() < self.planner_time_bound:
            self.planner_time_bound = state.get_time()
        return True
    

    def check_solved(self, state, thetaparameter):
        solved_condition = True
        open = []
        closed = []
        open.append(state)
        while open != []:
            # print(str(len(open)) + "states in open")
            # print(str(len(closed)) + "states in closed")
            state = open.pop()
            closed.append(state)

            if self.residual(state) > thetaparameter:
                solved_condition = False
                continue

            action = self.greedy_action(state) # get the greedy action for the state

            for transition in self.mdp.get_possible_transitions_from_action(state, action):
                next_state = self.mdp.compute_next_state(state, transition)
                if not (next_state in open or next_state in closed) and not self.solved(next_state):
                    open.append(next_state)

        # print("--------------------------------------------------- check_solved::solved_condition: ", solved_condition)
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

        for transition in self.mdp.get_possible_transitions_from_action(state, action):
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
            print("start")
            time_init_trial = datetime.datetime.now()
            self.lrtdp_tvma_trial(self.vinitState, self.convergenceThresholdGlobal, self.planner_time_bound)
            time_final_trial = datetime.datetime.now()
            print("trial time: " + str((time_final_trial - time_init_trial).total_seconds()))

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
                # self.valueFunction[state_string] = self.calculate_Q(state, self.policy[state_string][2])
                # print("update time: ", (datetime.datetime.now() - time_update_start).total_seconds())
                # sample successor mdp state (random)
                # most_probable_transition = self.calculate_most_probable_transition(state, self.policy[state.to_string()][2])
                # sample successor mdp state 
                self.policy[state.to_string()] = self.calculate_argmin_Q(state)
                transitions = self.mdp.get_possible_transitions_from_action(state, self.policy[state.to_string()][2])
                if not transitions:
                    print("No transitions found for state: ", state.to_string())
                    
                
                transition_selected = np.random.choice(transitions, p=[t.get_probability() for t in transitions])
                state = self.mdp.compute_next_state(state, transition_selected)

            time_update_label = datetime.datetime.now()
            while visited:
                state = visited.pop()
                if not self.check_solved(state, thetaparameter):
                    break        
            print("update label time: ", (datetime.datetime.now() - time_update_label).total_seconds())


