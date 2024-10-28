from MDP import MDP, State, Transition
from OccupancyMap import OccupancyMap
import datetime
from inspect import currentframe, getframeinfo

class LrtdpTvmaAlgorithm():

    def __init__(self, occupancy_map, initial_state_name, convergence_threshold, time_bound_real, planner_time_bound):
        self.occupancy_map = occupancy_map
        self.mdp = MDP(self.occupancy_map)
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


    ### Q VALUES
    def calculate_Q(self, state, action):
        # need to calculate Q(v, a, t)
        # get the cost of the action 
        current_action_cost = 0
        future_actions_cost = 0
        possible_transitions = self.mdp.get_possible_transitions_from_action(state, action)
        for transition in possible_transitions:
            local_current_action_cost = 0
            local_current_action_cost = transition.get_cost() * transition.get_probability()
            # print("local_current_action_cost: ", local_current_action_cost)
            current_action_cost = current_action_cost + local_current_action_cost
            next_state = self.mdp.compute_next_state(state, transition)
            # print("next_state: ", next_state)
            local_future_actions_cost = self.get_value(next_state) * transition.get_probability()
            # print("local_future_actions_cost: ", local_future_actions_cost)
            future_actions_cost = future_actions_cost + local_future_actions_cost
        return current_action_cost + future_actions_cost 


    def calculate_argmin_Q(self, state):
        # take the actions of the MDP and calculate their Q values, then takes the argmin of the Q values
        qvalues = []
        print("state: ", state)
        print("possible actions: ", self.mdp.get_possible_actions(state))
        if not self.mdp.get_possible_actions(state):
            print("No possible actions")
            return (0, state, "")
        for action in self.mdp.get_possible_actions(state):
            qvalues.append((self.calculate_Q(state, action),state, action))
        ## need to check if this is correct
        min = None
        print (qvalues)
        for qvalue in qvalues:
            if min is None:
                min = qvalue
            else:
                if qvalue[0] < min[0]:
                    min = qvalue
        print("min: ", min)
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
        return abs(self.get_value(state) - self.calculate_Q(state, action))

    def solved(self, state):
        return state in self.solved_set    

    def get_value(self, state):
        if state.to_string() in self.valueFunction:
            return self.valueFunction[state.to_string()]
        return 0

    def goal(self, state):
        return len(state.get_visited_vertices()) == len(self.occupancy_map.get_vertices_list())
    


    

    def check_solved(self, state, thetaparameter):
        solved_condition = True
        open = []
        closed = []
        open.append(state)
        while open:
            state = open.pop()
            closed.append(state)
            # print("len(open)", len(open))
            # print("residual", self.residual(state))
            if self.residual(state) > thetaparameter:
                solved_condition = False
                continue
            action = self.greedy_action(state)
            print("possible transitions:", self.mdp.get_possible_transitions_from_action(state, action))
            for transition in self.mdp.get_possible_transitions_from_action(state, action):
                next_state = self.mdp.compute_next_state(state, transition)
                # print("Next state: ", next_state.to_string())
                # print("solved: ", self.solved(next_state))
                if not self.solved(next_state) and not (next_state in open or next_state in closed):
                    open.append(next_state)
        print("solved_condition: ", solved_condition)
        if solved_condition:
            for state in closed:
                self.solved_set.add(state)
        else:
            while closed:
                state = closed.pop()
                self.update(state)
        
    
    def lrtdp_tvma(self):
        # need to check where to fit this (time_elapsed)
        initial_current_time = datetime.datetime.now()
        # print ("Time elapsed: ", (datetime.datetime.now() - initial_current_time).total_seconds())
        print(self.vinitState)
        print(self.vinitState.get_visited_vertices())
        while (not self.solved(self.vinitState)) and ((datetime.datetime.now() - initial_current_time)) < datetime.timedelta(seconds = self.time_bound_real):
            # print("Time elapsed: ", (datetime.datetime.now() - initial_current_time).total_seconds())
            # print("valueFunction", self.valueFunction)
            # print("policy", self.policy)
            self.lrtdp_tvma_trial(self.vinitState, self.convergenceThresholdGlobal, self.planner_time_bound)

    def lrtdp_tvma_trial(self, vinitStateParameter, thetaparameter, maxtimeparameter):
            visited = [] # this is a stack
            state = vinitStateParameter
            # check for termination
            while not self.solved(state):
                visited.append(state)
                print("State: ", state.to_string())
                print("Visited vertices: ", state.get_visited_vertices())   
                print("Time: ", state.get_time())
                print("goal: ", self.goal(state))
                if self.goal(state) or state.get_time() > maxtimeparameter:
                    break
                # perform bellman backup and update policy
                # print("State: ", state.to_string())
                state_string = state.to_string()
                # print(state.get_visited_vertices())
                # print(state.get_visited_vertices())
                self.policy[state_string] = self.calculate_argmin_Q(state)
                # print("Policy: ", self.policy[state_string])
                self.valueFunction[state_string] = self.calculate_Q(state, self.policy[state_string][2])
                # sample successor mdp state (random)
                most_probable_transition = None
                for transition in self.mdp.get_possible_transitions(state):
                    if most_probable_transition is None:
                        most_probable_transition = transition
                    else:
                        if transition.get_probability() < most_probable_transition.get_probability():
                            most_probable_transition = transition
                state = self.mdp.compute_next_state(state, most_probable_transition)
                # print("State: ", state.to_string())
            print("after while, until here it seems correct")
            
            # update solved label for visited states
            while visited:
                state = visited.pop()
                # print("State: ", state.to_string())
                if not self.check_solved(state, thetaparameter):
                    break        
