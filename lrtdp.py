from MDP import MDP
from OccupancyMap import OccupancyMap


def LrtdpTvmaAlgorithm():
    def __init__(self, occupancy_map_name, initial_state_name, convergence_threshold):
        self.occupancy_map = OccupancyMap(occupancy_map_name)
        self.mdp = MDP(self.occupancy_map, initial_state_name)
        self.vinitGlobal = initial_state_name
        self.tGlobal = 0
        self.convergenceThresholdGlobal = convergence_threshold
        self.policy = {}
        self.valueFunction = {}
        self.labeled = set()

    def lrtdp_tvma(self):
        while ...:
            self.lrtdp_tvma_trial()

    def calculate_Q(self, vertex, currentTime, action, remainingTime):
        # need to calculate Q(v, a, t)
        # get the cost of the action a from the MDP
        value = 0
        if remainingTime < 0:
            return (False, 0)
        for transition in self.mdp.get_possible_actions():
            calculate_Q(transition['end'], currentTime + transition., transition, remainingTime - 1)
        self.mdp.get_transition_cost(vertex, action)
        pass

    def calculate_argmin_Q(self, v, t):
        # need to calculate A_A_i
        # take the actions of the MDP and calculate their Q values, then takes the argmin of the Q values
        qvalues = []
        for action in self.mdp.get_possible_actions():
            qvalues.append(self.calculate_Q(v, t, action))
        return qvalues.index(min(qvalues))

    def labeled(self, v, t):
        if (v, t) in self.labeled:
            return True
        return False

    def is_goal(self, v, t, maxtimeparameter):
        if v in self.mdp.get_terminal_states() and t < maxtimeparameter:
            return True
        return False

    def lrtdp_tvma_trial(self, tvmaparameter, vinitparameter, thetaparameter, maxtimeparameter):
        visited = [] # this is a stack
        v = vinitparameter
        t = 0
        # check for termination
        while not labeled(v, t):
            visited.append((v, t))
            if t > maxtimeparameter or is_goal(v, t, maxtimeparameter):
                break
        # perform bellman backup and update policy
        self.policy[v][t] = self.calculate_argmin_Q(v, t)
        self.valueFunction[v][t] = self.calculate_Q(v, t, self.policy[v][t])
        # sample successor mdp state
        