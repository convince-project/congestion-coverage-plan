from MDP import MDP, State, Transition
from OccupancyMap import OccupancyMap
import datetime


def LrtdpTvmaAlgorithm():
    def __init__(self, occupancy_map_name, initial_state_name, convergence_threshold, time_bound):
        self.occupancy_map = OccupancyMap(occupancy_map_name)
        self.mdp = MDP(self.occupancy_map)
        self.vinitState = State(initial_state_name, 
                                   0, 
                                   (self.occupancy_map.find_vertex_from_id(initial_state_name).get_posx(), 
                                    self.occupancy_map.find_vertex_from_id(initial_state_name).get_posy())
                                    [initial_state_name])
        self.vinitStateName = initial_state_name
        self.timeBoundGlobal = time_bound
        self.convergenceThresholdGlobal = convergence_threshold
        self.policy = {}
        self.valueFunction = {}
        self.solved = set()
        self.labeled = set()
        # self.value = {}


    ### STATE FUNCTIONS
    def update(self, state):
        action = self.greedy_action(state)[2]
        self.valueFunction[str(state)] = self.calculate_Q(state, action)


    def greedy_action(self, state):
        return calculate_argmin_Q(state)


    def residual(self, state):
        action = self.greedy_action(state)[2]
        return abs(self.get_value(state) - self.calculate_Q(state, action))

    def solved(self, state):
        return state in self.solved
    

    def labeled(self, state):
        return state in self.labeled
    

    def is_goal(self, state):
        return self.mdp.solved(state)
    

    def get_value(self, state):
        if str(state) in self.valueFunction:
            return self.valueFunction[str(state)]
        return 0
    

    ### Q VALUES
    def calculate_Q(self, state, action):
        # need to calculate Q(v, a, t)
        # get the cost of the action 
        current_action_cost = 0
        future_actions_cost = 0
        possible_transitions = self.mdp.calculate_transitions_from_action(state, action)
        for transition in possible_transitions:
            current_action_cost = current_action_cost + transition.get_cost() * transition.get_probability()
            next_state = self.mdp.calculate_next_state(self, state, transition)
            future_actions_cost = future_actions_cost + self.get_value(next_state) * transition.get_probability()
        return current_action_cost + future_actions_cost 


    def calculate_argmin_Q(self, state):
        # take the actions of the MDP and calculate their Q values, then takes the argmin of the Q values
        qvalues = []
        for action in self.mdp.get_possible_actions():
            qvalues.append((self.calculate_Q(state, action),state, action))
        ## need to check if this is correct
        return qvalues[qvalues.index(min(qvalues[0], key=lambda x: x[0]))]
    

    

    def check_solved(self, state, thetaparameter):
        solved = True
        open = []
        closed = []
        open.append(state)
        while not open.isEmpty():
            state = open.pop()
            closed.append(state)
            if residual(state) > thetaparameter:
                solved = False
                continue
            action = greedy_action(state)
            for transition in self.mdp.calculate_transitions_from_action(state, action):
                next_state = self.mdp.calculate_next_state(state, transition)
                if not solved(next_state) and not (next_state in open or next_state in closed):
                    open.append(next_state)

        if solved:
            for state in closed:
                self.solved.add(state)
        else:
            while not closed.isEmpty():
                state = closed.pop()
                self.update(state)
        
    
    def lrtdp_tvma(self):
        # need to check where to fit this (time_elapsed)
        initial_current_time = datetime.datetime.now()
        while (not solved(self.vinitState)) and ((datetime.datetime.now() - initial_current_time) / 60) < self.timeBoundGlobal:
            self.lrtdp_tvma_trial(self.vinitState, self.convergenceThresholdGlobal, self.timeBoundGlobal)

    def lrtdp_tvma_trial(self, vinitStateParameter, thetaparameter, maxtimeparameter):
            visited = [] # this is a stack
            state = vinitStateParameter
            # check for termination
            while not labeled(state):
                visited.append(state)
                if is_goal(state, maxtimeparameter) or state.get_time() > maxtimeparameter:
                    break
                # perform bellman backup and update policy
                self.policy[str(state)] = self.calculate_argmin_Q(state)
                self.valueFunction[str(state)] = self.calculate_Q(state, self.policy[str(state)[2]])
                # sample successor mdp state (random)
                most_probable_transition = None
                for transition in self.mdp.calculate_transitions(state):
                    if most_probable_transition is None:
                        most_probable_transition = transition
                    else:
                        if transition.get_probability() < most_probable_transition.get_probability():
                            most_probable_transition = transition
                state = self.mdp.calculate_next_state(state, most_probable_transition)
            
            # update solved label for visited states
            while not visited.isEmpty():
                state = visited.pop()
                if not self.check_solved(state, thetaparameter):
                    break        








    # def labeled(self, v, t):
    #     if (v, t) in self.labeled:
    #         return True
    #     return False

    # def is_goal(self, v, t, maxtimeparameter):
    #     if v in self.mdp.get_terminal_states() and t < maxtimeparameter:
    #         return True
    #     return False
    
    # def greedy_action(self, v, t):
    #     return calculate_argmin_Q(v, t)
    
    # def update(self, v, t, value):
    #     action = greedy_action(v, t)
    #     value = calculate_Q(v, t, action)

    # def residual(self, v, t, old_valueFunction):
    #     action = greedy_action(v, t)
    #     return abs(calculate_Q(v, t, action) - old_valueFunction)
    


    # def checkSolved(self, v, t, thetaparameter):
    #     solved = True
    #     open = []
    #     closed = []
    #     # if not self.mdp.solved(v, t):
    #     old_valueFunction = 0
    #     open.append((v, t))
    #     while not open.isEmpty():
    #         (v, t) = open.pop()
    #         closed.append((v, t))
    #         if residual(v, t, old_valueFunction) > thetaparameter:
    #             solved = False
    #             continue
    #         action = greedy_action(v, t)
    #         # is this correct?
    #         self.mdp.execute_action(v, action)
    #         for transition in self.mdp.get_possible_actions():
    #             if transition.







            
    #         if not self.mdp.solved(v, t):
    #             solved = False
    #             break
    #         for transition in self.mdp.get_possible_actions():
    #             if not self.labeled(transition['end'], t + self.mdp.get_transition_cost(v, transition['end'], t)):
    #                 open.append((transition['end'], t + self.mdp.get_transition_cost(v, transition['end'], t)))

