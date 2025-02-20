from MDP import MDP, State, Transition
from OccupancyMap import OccupancyMap
import datetime
from inspect import currentframe, getframeinfo
# from scipy.sparse import csr_matrix
from scipy.sparse import csr_array
from scipy.sparse.csgraph import minimum_spanning_tree, shortest_path
import logging
import networkx as nx
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
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        self.shortest_paths_matrix = self.calculate_shortest_path_matrix()
        # self._map_matrix = self.create_map_matrix()


    def get_policy(self):
        return self.policy

    def calculate_shortest_path(self, vertex1, vertex2):
        vertex1_number = int(vertex1[6:]) - 1
        vertex2_number = int(vertex2[6:]) - 1
        return self.shortest_paths_matrix[vertex1_number][vertex2_number]

    def calculate_shortest_path_matrix(self):
        mst_matrix = self.create_map_matrix()
        print("mst")
        sp =shortest_path(mst_matrix)
        return sp 


    def create_map_matrix(self):
        # g = nx.Graph()
        vertices = self.occupancy_map.get_vertices_list()
        mst_matrix = []
        for vertex in vertices:
            mst_matrix_line = []
            # mst_matrix[vertex.get_id()] = {}
            for vertex2 in vertices:
                if vertex.get_id() == vertex2.get_id():
                    mst_matrix_line.append(0)
                elif self.occupancy_map.find_edge_from_position(vertex.get_id(), vertex2.get_id()) is not None:
                    edge_id = self.occupancy_map.find_edge_from_position(vertex.get_id(), vertex2.get_id())
                    mst_matrix_line.append(self.occupancy_map.get_edge_traverse_time(edge_id)['low'])
                else:
                    mst_matrix_line.append(99999999)
            mst_matrix.append(mst_matrix_line)
        print(mst_matrix)
        return csr_array(mst_matrix)

    ### Q VALUES
    def calculate_Q(self, state, action):
        if self.goal(state):
            return 0
        # need to calculate Q(v, a, t)
        # get the cost of the action 
        current_action_cost = 0
        future_actions_cost = 0
        possible_transitions = self.mdp.get_possible_transitions_from_action(state, action)
        for transition in possible_transitions:
            local_current_action_cost = 0
            local_current_action_cost = transition.get_cost() * transition.get_probability()
            self.logger.debug("local_current_action_cost: ", local_current_action_cost)
            current_action_cost = current_action_cost + local_current_action_cost
            next_state = self.mdp.compute_next_state(state, transition)
            # self.logger.debug("next_state: ", next_state)
            local_future_actions_cost = self.get_value(next_state) * transition.get_probability()
            self.logger.debug("local_future_actions_cost: ", local_future_actions_cost)
            future_actions_cost = future_actions_cost + local_future_actions_cost
            print("value = ", self.get_value(next_state), "probability", transition.get_probability())
            string_to_print = "GOALLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLL"
            for vertex in self.occupancy_map.get_vertices_list():
                if vertex.get_id() not in next_state.get_visited_vertices():
                    string_to_print = ""
        print(string_to_print, "total_cost_state_time", current_action_cost + future_actions_cost+state.get_time(),"action", action, "total_cost", current_action_cost + future_actions_cost,"visited_vertices", next_state.get_ordered_visited_vertex(),  "state_time", state.get_time() , "current_action_cost: ", current_action_cost, "future_actions_cost: ", future_actions_cost)
        return current_action_cost + future_actions_cost 

    def calculate_current_action_cost(self, state, action):
        current_action_cost = 0
        possible_transitions = self.mdp.get_possible_transitions_from_action(state, action)
        for transition in possible_transitions:
            local_current_action_cost = 0
            local_current_action_cost = transition.get_cost() * transition.get_probability()
            self.logger.debug("local_current_action_cost: ", local_current_action_cost)
            current_action_cost = current_action_cost + local_current_action_cost
        return current_action_cost


    def calculate_argmin_Q(self, state):
        # take the actions of the MDP and calculate their Q values, then takes the argmin of the Q values
        qvalues = []
        self.logger.debug("calculate_argmin_Q::state: ", state)
        self.logger.debug("calculate_argmin_Q::possible actions: ", self.mdp.get_possible_actions(state))
        if not self.mdp.get_possible_actions(state):
            self.logger.debug("calculate_argmin_Q::No possible actions")
            return (0, state, "")
        actions_sorted = list(self.mdp.get_possible_actions(state))
        actions_sorted.sort()
        for action in actions_sorted:
            qvalues.append((self.calculate_Q(state, action),state, action))
        ## need to check if this is correct
        min = None
        self.logger.debug ("calculate_argmin_Q::LEN QVALUES", len(qvalues))
        for qvalue in qvalues:
            print("calculate_argmin_Q::qvalue: ", qvalue[0], "***", str(qvalue[1]),"***", qvalue[2])
            if min is None:
                min = qvalue
            else:
                if qvalue[0] < min[0]:
                    min = qvalue
                # elif qvalue[0] == min[0]:
                #     if self.calculate_current_action_cost(qvalue[1], qvalue[2]) < self.calculate_current_action_cost(min[1], min[2]):
                #         min = qvalue

        self.logger.debug("calculate_argmin_Q::min: ", min[0], "***", str(min[1]),"***", min[2])
        # min is a tuple with the Q value, the state and the action
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
        # print("RESIDUAL::STATE: ", str(state))
        # print("RESIDUAL::ACTION: ", action)
        # print("RESIDUAL::Q: ", self.calculate_Q(state, action))
        # print("RESIDUAL::VALUE: ", self.get_value(state))

        return abs(self.get_value(state) - self.calculate_Q(state, action))

    def solved(self, state):
        return state in self.solved_set    

    def get_value(self, state):
        print(str(state))
        if state.to_string() in self.valueFunction:
            return self.valueFunction[state.to_string()]
        value = 0
        for vertex in self.occupancy_map.get_vertices_list():
            if vertex.get_id() not in state.get_visited_vertices():
                value = max(value, self.calculate_shortest_path(state.get_vertex(), vertex.get_id()))
        return value

    def goal(self, state):
        # print(state.get_visited_vertices())

        for vertex in self.occupancy_map.get_vertices_list():
            if vertex.get_id() not in state.get_visited_vertices():
                return False
        return True
        # return len(state.get_visited_vertices()) == len(self.occupancy_map.get_vertices_list())
    


    

    def check_solved(self, state, thetaparameter):
        solved_condition = True
        open = []
        closed = []
        self.logger.debug("check_solved::State: ", state, "Visited vertices: ", state.get_visited_vertices(), "Time: ", state.get_time(), "solved: ", self.solved(state))
        self.logger.debug("check_solved::State: ", state, "Visited vertices: ", state.get_visited_vertices(), "Time: ", state.get_time(), "solved: ", self.solved(state))
        # if not self.solved(state):
        open.append(state)
        while open != []:
            state = open.pop()
            closed.append(state)

            self.logger.debug("****************check_solved::State: ", str(state))
            self.logger.debug("@@@@@@@@@@@@check_solved::residual", self.residual(state))
            self.logger.debug("============check_solved::Theta: ", thetaparameter)
            # self.logger.debug("len(open)", len(open))
            if self.residual(state) > thetaparameter:
                solved_condition = False
                continue
            action = self.greedy_action(state)
            self.logger.debug("check_solved::Action: ", action)
            self.logger.debug("check_solved::possible transitions:")
            for transition in self.mdp.get_possible_transitions_from_action(state, action):
                self.logger.debug("check_solved::Transition: ", str(transition))
                next_state = self.mdp.compute_next_state(state, transition)
                # self.logger.debug("Next state: ", next_state.to_string())
                # self.logger.debug("solved: ", self.solved(next_state))
                self.logger.debug("check_solved::solved: ", self.solved(next_state))
                self.logger.debug("check_solved::open: ", open)
                self.logger.debug("check_solved::closed: ", closed)
                self.logger.debug("check_solved::next_State: ", next_state.to_string())    
                for state in open:
                    self.logger.debug("check_solved::open: ", state.to_string())
                for state in closed:
                    self.logger.debug("check_solved::closed: ", state.to_string())
                if not self.solved(next_state) and not (next_state in open or next_state in closed) and (next_state.get_time() <= self.planner_time_bound):
                    open.append(next_state)
        self.logger.debug("--------------------------------------------------- check_solved::solved_condition: ", solved_condition)

        if solved_condition:
            for state in closed:
                self.solved_set.add(state)
        else:
            while closed:
                state = closed.pop()
                self.update(state)
        
    def calculate_most_probable_transition(self, state):
        most_probable_transitions = []
        for transition in self.mdp.get_possible_transitions(state):
            self.logger.debug("Transition: ", str(transition))
            if most_probable_transitions == []:
                most_probable_transitions.append(transition)
            else:
                if transition.get_probability() < most_probable_transitions[0].get_probability():
                    most_probable_transitions = []
                    most_probable_transitions.append(transition)
                elif transition.get_probability() == most_probable_transitions[0].get_probability():
                    most_probable_transitions.append(transition)
                
        # self.logger.debug("lrtdp_tvma_trial::Most probable transition: ", str(most_probable_transition))
        # state = self.mdp.compute_next_state(state, most_probable_transition)
        most_probable_transition = None
        if len(most_probable_transitions) > 1:
            # get the one with the lowest cost
            min_cost = None
            for transition in most_probable_transitions:
                if min_cost is None:
                    min_cost = transition.get_cost()
                    most_probable_transition = transition
                else:
                    if transition.get_cost() < min_cost:
                        min_cost = transition.get_cost()
                        most_probable_transition = transition
        else:
            most_probable_transition = most_probable_transitions[0]
        return most_probable_transition


    def lrtdp_tvma(self):
        # need to check where to fit this (time_elapsed)
        # self.occupancy_map.track_current_people()
        # self.occupancy_map.predict_people_positions(100)
        self.occupancy_map.predict_occupancies(self.time_for_occupancies, self.time_for_occupancies + self.planner_time_bound)
        initial_current_time = datetime.datetime.now()
        # self.logger.debug ("Time elapsed: ", (datetime.datetime.now() - initial_current_time).total_seconds())
        self.logger.debug("initial state vinit:", self.vinitState)
        self.logger.debug("initial state visited vertices", self.vinitState.get_visited_vertices())
        while (not self.solved(self.vinitState)) and ((datetime.datetime.now() - initial_current_time)) < datetime.timedelta(seconds = self.time_bound_real):
            # self.logger.debug("Time elapsed: ", (datetime.datetime.now() - initial_current_time).total_seconds())
            # self.logger.debug("valueFunction", self.valueFunction)
            # self.logger.debug("policy", self.policy)
            self.lrtdp_tvma_trial(self.vinitState, self.convergenceThresholdGlobal, self.planner_time_bound)
            # print("trial")
            # print("policy", self.policy)
            # print("Time elapsed: ", (datetime.datetime.now() - initial_current_time).total_seconds())
        print("exit reason: ", "solved initial state", self.solved(self.vinitState), "reached time bound",  (datetime.datetime.now() - initial_current_time))
        return self.solved(self.vinitState)

    def lrtdp_tvma_trial(self, vinitStateParameter, thetaparameter, maxtimeparameter):
            visited = [] # this is a stack
            state = vinitStateParameter
            # check for termination
            while not self.solved(state):
                print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
                visited.append(state)
                # print("lrtdp_tvma_trial::State: ", state.to_string())
                # print("lrtdp_tvma_trial::vertex", state.get_vertex())
                # print("lrtdp_tvma_trial::Visited vertices: ", state.get_visited_vertices())   
                # print("lrtdp_tvma_trial::Time: ", state.get_time())
                # print("lrtdp_tvma_trial::goal: ", self.goal(state))
                if self.goal(state) or (state.get_time() > maxtimeparameter):
                    break
                # perform bellman backup and update policy
                # self.logger.debug("State: ", state.to_string())
                state_string = state.to_string()
                # self.logger.debug(state.get_visited_vertices())
                # self.logger.debug(state.get_visited_vertices())
                self.policy[state_string] = self.calculate_argmin_Q(state)
                print("lrtdp_tvma_trial::Policy: ", "qvalue", self.policy[state_string][0], "current state", str(self.policy[state_string][1]), "action", self.policy[state_string][2])
                self.valueFunction[state_string] = self.calculate_Q(state, self.policy[state_string][2])
                # sample successor mdp state (random)

                # most_probable_transition = self.calculate_most_probable_transition(state)
                # sample according to policy
                most_probable_transition = None
                for transition in self.mdp.get_possible_transitions_from_action(self.policy[state_string][1], self.policy[state_string][2]):
                    if most_probable_transition is None:
                        most_probable_transition = transition
                    elif transition.get_cost() < most_probable_transition.get_cost():
                        most_probable_transition = transition
                state = self.mdp.compute_next_state(state, most_probable_transition)
                    
                # self.logger.debug("State: ", state.to_string())
            self.logger.debug("lrtdp_tvma_trial::after while, until here it seems correct")
            
            # update solved label for visited states
            while visited:
                state = visited.pop()
                # self.logger.debug("State: ", state.to_string())
                if not self.check_solved(state, thetaparameter):
                    break        
