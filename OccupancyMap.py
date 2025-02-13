# based on the TopologicalMap class we add information about edge and vertices occupancy, as well as the limits of the edges and vertices in order to consider them as occupied or not.
# the occupancy map is a dictionary with the following structure:
# {
#   'name': 'map_name',
#   'vertex_limits' : [{'id': uuidvertex, 'limit': n_people}, ....],
#   'edge_limits' : [{'id': uuidedge, 'limit': n_people}, ....],
#   'edge_traverse_time': {'uuidedge': {'high': time, 'low': time}, ....}, 
#   'vertex_occupancy': {uuidvertex: high_or_low, ....},
#   'edge_occupancy': {uuidedge: high_or_low, ....},
#   'vertex_expected_occupancy': {time: {uuidvertex: {'high': n_people, 'low': n_people}, ....}, ....},
#   'edge_expected_occupancy': {time: {uuidedge: {'high': n_people, 'low': n_people}, ....}, ....}
# }
# The occupancy map can be saved and loaded to/from a yaml file.
from tqdm import *
import numpy as np
import yaml
from TopologicalMap import TopologicalMap
import matplotlib.pyplot as plt
import random
import csv
from utils import read_iit_human_traj_data
# , get_human_traj_data_by_person_id
from cliff_predictor import CliffPredictor

class OccupancyMap(TopologicalMap):
    def __init__(self, cliffPredictor):
        self.name = ""
        self.vertex_occupancy = {}
        self.edge_occupancy = {}
        self.vertex_limits = {}
        self.edge_limits = {}
        self.edge_traverse_times = {}
        self.vertex_expected_occupancy = {}
        self.edge_expected_occupancy = {}
        self.cliffPredictor = cliffPredictor
        self.people_trajectories = {}
        self.people_predicted_positions = {}
        self.predicted_positions = None
        self.current_occupancies = {}
        super().__init__()

    def set_name(self, name):
        self.name = name
    


    # add the traverse time for an edge
    def add_edge_traverse_time(self, edge_id, occupancy_high_or_low, time):
        # check if the edge exists
        if self.find_edge_from_id(edge_id) is None:
            return False
        # add the edge traverse time
        if edge_id not in self.edge_traverse_times.keys():
            self.edge_traverse_times[edge_id] = {}
        if occupancy_high_or_low in self.edge_traverse_times[edge_id].keys():
            return False
        self.edge_traverse_times[edge_id][occupancy_high_or_low] = time
        return True
    


    # add the limits for vertices and edges
    def add_vertex_limit(self, vertex_id, limit):
        # check if the vertex exists
        if self.find_vertex_from_id(vertex_id) is None:
            return False
        # add the vertex limit
        self.vertex_limits[vertex_id] = limit
        return True

    def add_edge_limit(self, edge_id, limit):
        # check if the edge exists
        if self.find_edge_from_id(edge_id) is None:
            return False
        # add the edge limit
        self.edge_limits[edge_id] = limit
        return True
    

    # find the limits for vertices and edges
    def find_vertex_limit(self, vertex_id):
        if vertex_id in self.vertex_limits:
            return self.vertex_limits[vertex_id]
        return None
    
    def find_edge_limit(self, edge_id):
        if edge_id in self.edge_limits:
            return self.edge_limits[edge_id]
        print("errorrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr")
        return 0


    # get the occupancy of the vertices and edges
    def get_edge_expected_occupancy(self, time, edge_id):
        if time in self.edge_expected_occupancy:
            if edge_id in self.edge_expected_occupancy[time]:
                return self.edge_expected_occupancy[time][edge_id]
        return None
    
    def get_vertex_expected_occupancy(self, time, vertex_id):
        if time in self.vertex_expected_occupancy:
            if vertex_id in self.vertex_expected_occupancy[time]:
                return self.vertex_expected_occupancy[time][vertex_id]
        return None
    

    # get the traverse time of an edge
    def get_edge_traverse_time(self, edge_id):
        if edge_id in self.edge_traverse_times:
            return self.edge_traverse_times[edge_id]
        return None


    def remove_verted_expected_occupancy(self, time, vertex_id):
        if time in self.vertex_expected_occupancy:
            if vertex_id in self.vertex_expected_occupancy[time]:
                del self.vertex_expected_occupancy[time][vertex_id]

    def remove_edge_expected_occupancy(self, time, edge_id):
        if time in self.edge_expected_occupancy:
            if edge_id in self.edge_expected_occupancy[time]:
                del self.edge_expected_occupancy[time][edge_id]
    
    def _calculate_edge_traverse_time(self, edge_id, occupancy_data):
        robot_speed = 0.8
        edge = self.find_edge_from_id(edge_id)
        if edge is None:
            return None
        edge_length = edge.get_length()
        # edge_traverse_time = {}
        edge_occupancy = 0
        if edge_id in occupancy_data.keys():
            edge_occupancy = occupancy_data[edge_id]
        traverse_time = edge_length * robot_speed + edge_occupancy*random.uniform(0.7, 1.3)
        # if edge_occupancy > 0:
        #     print("edge: ", edge_id, "occupancy: ", edge_occupancy, "traverse_time: ", traverse_time)
        edge_traverse_time = {"num_people" : edge_occupancy, "traverse_time" : traverse_time}
        return edge_traverse_time

    def _calculate_edges_traverse_times(self, number_of_trials):
        # print(self.cliffPredictor.ground_truth_data_file)
        human_traj_data = read_iit_human_traj_data(self.cliffPredictor.ground_truth_data_file)
        human_traj_data_by_time = human_traj_data.time.unique()
        if number_of_trials > len(human_traj_data_by_time):
            number_of_trials = len(human_traj_data_by_time)
        step_length = len(human_traj_data_by_time) // number_of_trials
        traverse_times = {}
        for time_index in tqdm(range(0, len(human_traj_data_by_time), step_length)):
            # print("time: ", human_traj_data_by_time[time_index])
            occupancies = self.get_current_occupancies(human_traj_data_by_time[time_index])
            for edge in self.edges:
                if edge.get_id() not in traverse_times.keys():
                    traverse_times[edge.get_id()] = {}
                traverse_time = self._calculate_edge_traverse_time(edge.get_id(), occupancies)
                if traverse_time is not None:
                    if traverse_time["num_people"] > self.find_edge_limit(edge.get_id()):
                        if "high" not in traverse_times[edge.get_id()]:
                            traverse_times[edge.get_id()]["high"] = []
                        traverse_times[edge.get_id()]["high"].append(traverse_time["traverse_time"])
                    else:
                        if "low" not in traverse_times[edge.get_id()]:
                            traverse_times[edge.get_id()]["low"] = []
                        traverse_times[edge.get_id()]["low"].append(traverse_time["traverse_time"])
        
        return traverse_times
        
    def calculate_average_edge_occupancy(self, number_of_trials):
        human_traj_data = read_iit_human_traj_data(self.cliffPredictor.ground_truth_data_file)
        human_traj_data_by_time = human_traj_data.time.unique()
        if number_of_trials > len(human_traj_data_by_time):
            number_of_trials = len(human_traj_data_by_time)
        step_length = len(human_traj_data_by_time) // number_of_trials
        average_occupancies = {}
        for time_index in tqdm(range(0, len(human_traj_data_by_time), step_length)):
            # print("time: ", human_traj_data_by_time[time_index])
            occupancies = self.get_current_occupancies(human_traj_data_by_time[time_index])
            for edge in self.edges:
                if edge.get_id() not in average_occupancies.keys():
                    average_occupancies[edge.get_id()] = []
                traverse_time = self._calculate_edge_traverse_time(edge.get_id(), occupancies)
                if traverse_time is not None and traverse_time["num_people"] > 0:
                    average_occupancies[edge.get_id()].append(traverse_time["num_people"])
        for edge in average_occupancies.keys():
            print("edge: ", edge, "occupancies: ", average_occupancies[edge])
            if len(average_occupancies[edge]) > 0:
                median = int(np.median(average_occupancies[edge])+ 1)
            else:
                median = 2
            self.edge_limits[edge] = median
            
        # return average_occupancies



    def calculate_average_edge_traverse_times(self, number_of_trials):
        traverse_times = self._calculate_edges_traverse_times(number_of_trials)
        # print("traverse_times: ", traverse_times.keys())
        for edge in traverse_times.keys():

            if edge not in self.edge_traverse_times.keys():
                self.edge_traverse_times[edge] = {}
            # print(traverse_times[edge].keys())
            if "high" in traverse_times[edge]:
                if "high" not in self.edge_traverse_times[edge]:
                    self.edge_traverse_times[edge]["high"] = 0
                self.edge_traverse_times[edge]["high"] = np.mean(traverse_times[edge]["high"])
            if "low" in traverse_times[edge]:
                if "low" not in self.edge_traverse_times[edge]:
                    self.edge_traverse_times[edge]["low"] = 0
                # print("low: ", traverse_times[edge]["low"])
                self.edge_traverse_times[edge]["low"] = np.mean(traverse_times[edge]["low"])
            if "high" not in self.edge_traverse_times[edge]:
                self.edge_traverse_times[edge]["high"] = self.edge_traverse_times[edge]["low"]
            if "low" not in self.edge_traverse_times[edge]:
                self.edge_traverse_times[edge]["low"] = self.edge_traverse_times[edge]["high"]
        




    # save and load the occupancy map
    def save_occupancy_map(self, filename):
        self.save_topological_map(filename.split('.')[0] + "-topological." + filename.split('.')[1])
        # print(self.edge_limits)
        with open(filename, 'w') as f:
            yaml.dump({'name': self.name,
                       'edge_limits':  [{'id': edge_id, "limit": self.edge_limits[edge_id]} for edge_id in self.edge_limits.keys()], 
                       'edge_traverse_times': [{'id': edge_id, "high": float(self.edge_traverse_times[edge_id]["high"]), "low": float(self.edge_traverse_times[edge_id]["low"])} for edge_id in self.edge_traverse_times.keys()]
                       }, f, default_flow_style=False)


                    #    'edge_limits': self.edge_limits, 
                    #    'edge_traverse_times': self.edge_traverse_times},
            
    def load_occupancy_map(self, filename):
        self.load_topological_map(filename.split('.')[0] + "-topological." + filename.split('.')[1])
        with open(filename, 'r') as f:
            data = yaml.load(f, Loader=yaml.FullLoader)
            self.name = data['name']
            for edge_id in data['edge_limits']:
                self.edge_limits[edge_id['id']] = edge_id['limit']
            for edge_id in data['edge_traverse_times']:
                self.edge_traverse_times[edge_id['id']] = {}
                self.edge_traverse_times[edge_id['id']]["high"] = edge_id['high']
                self.edge_traverse_times[edge_id['id']]["low"] = edge_id['low']

    def get_occupancies_at_time(self, current_time, time_to_predict):
        self.get_tracks_by_time(current_time)
        self.predict_people_positions(time_to_predict)
        self.assign_people_to_areas(time_to_predict)
        return (self.vertex_expected_occupancy[time_to_predict], self.edge_expected_occupancy[time_to_predict])


    # this is only for simulation purposes
    def get_tracks_by_time(self, time):
        human_traj_data = read_iit_human_traj_data(self.cliffPredictor.ground_truth_data_file)
        human_traj_data_by_time = human_traj_data.loc[human_traj_data['time'] == time]
        people_ids = list(human_traj_data_by_time.person_id.unique())
        tracks = {}
        self.people_trajectories = {}
        # print("people_ids: ", people_ids)

        for id in people_ids:
            human_traj_data_by_person_id = human_traj_data.loc[human_traj_data['person_id'] == id]
            human_traj_array = human_traj_data_by_person_id[["time", "x", "y", "velocity", "motion_angle"]].to_numpy()

            # if len(human_traj_array) < 6:
            #     continue
            # for traj in human_traj_data_by_person_id:
                # print("traj: ", traj)
            track_before_now = human_traj_array[human_traj_array[:, 0] <= time]
            track_filtered = track_before_now[-6:]
            # for i in track_filtered:
            #     print("i: ", i[0], "id: ", id)
            tracks[id] = track_filtered
            # print("tracks: ", tracks)
            

        self.people_trajectories = tracks
        return tracks
    

    def get_current_occupancies(self, time):
        # time = float(int(time))
        human_traj_data = read_iit_human_traj_data(self.cliffPredictor.ground_truth_data_file)
        human_traj_data_by_time = human_traj_data.loc[human_traj_data['time'] == time]
        self.current_occupancies = {}   
        for index, row in human_traj_data_by_time.iterrows():
            # print("x: ", row['x'], "y: ", row['y'])
            for vertex in self.vertices:
                if vertex.is_inside_area(row['x'], row['y']):
                    if vertex.get_id() not in self.current_occupancies:
                        self.current_occupancies[vertex.get_id()] = 0
                    self.current_occupancies[vertex.get_id()] += 1
            for edge in self.edges:
                if edge.is_inside_area(row['x'], row['y']):
                    if edge.get_id() not in self.current_occupancies:
                        self.current_occupancies[edge.get_id()] = 0
                    self.current_occupancies[edge.get_id()] += 1
                    # print("edge: ", edge.get_id(), "time", time)
                    # print("edge: ", edge.get_id())
            #plot current occupancy
        # self.plot_topological_map()
        # for index, row in human_traj_data_by_time.iterrows():
            # plt.plot(row['x'], row['y'], 'bo')
        # plt.show()    
        return self.current_occupancies
            
    

    def predict_people_positions(self, time_now, time_to_predict):
        delta_time = time_to_predict - time_now
        self.people_predicted_positions = {}
        self.people_predicted_positions = self.cliffPredictor.predict_positions(self.people_trajectories, delta_time)
        # for person in self.people_predicted_positions:
        #     for trajectory in person:
        #         for position in trajectory:
        #             print("time" + str(position[0]) + " x: " + str(position[1]) + " y: " + str(position[2]))
        # self.cliffPredictor.display_cliff_map(self.people_predicted_positions)
        return self.people_predicted_positions

    
    def plot_predicted_positions(self, time):
        self.plot_topological_map()
        for person_prediction in self.people_predicted_positions:
            for trajectory in person_prediction:
                for position in trajectory:
                    # print(position[0], time)
                    if int(position[0]) == time:
                        in_area = False
                        for vertex in self.vertices:
                            if vertex.is_inside_area(position[1], position[2]):
                                plt.plot(position[1], position[2], 'ro')
                                in_area = True

                        for edge in self.edges: 
                            if edge.is_inside_area(position[1], position[2]):
                                plt.plot(position[1], position[2], 'ro')
                                in_area = True
                        if not in_area:
                            plt.plot(position[1], position[2], 'go')
        plt.show()


    def predict_occupancies_for_edge(self, time, edge_id):
        if time not in self.edge_expected_occupancy:
            return False
        if edge_id not in self.edge_expected_occupancy[time]:
            return False
        if "poisson_binomial" not in self.edge_expected_occupancy[time][edge_id]:
            self.calculate_poisson_binomial(time)
        edge_limit = self.find_edge_limit(edge_id)
        self.edge_expected_occupancy[time][edge_id]['high'] = 0
        self.edge_expected_occupancy[time][edge_id]['low'] = 0
        for i in range(0, len(self.edge_expected_occupancy[time][edge_id]['poisson_binomial'])):
            if i >= edge_limit:
                self.edge_expected_occupancy[time][edge_id]['high'] += self.edge_expected_occupancy[time][edge_id]['poisson_binomial'][i]
            else:
                self.edge_expected_occupancy[time][edge_id]['low'] +=  self.edge_expected_occupancy[time][edge_id]['poisson_binomial'][i]


    def predict_occupancies_for_vertex(self, time, vertex_id):
        if time not in self.vertex_expected_occupancy:
            return False
        if vertex_id not in self.vertex_expected_occupancy[time]:
            return False
        if "poisson_binomial" not in self.vertex_expected_occupancy[time][vertex_id]:
            self.calculate_poisson_binomial(time)
        vertex_limit = self.find_vertex_limit(vertex_id)
        self.vertex_expected_occupancy[time][vertex_id]['high'] = 0
        self.vertex_expected_occupancy[time][vertex_id]['low'] = 0
        for i in range(0, len(self.vertex_expected_occupancy[time][vertex_id]['poisson_binomial'])):
            if i >= vertex_limit:
                self.vertex_expected_occupancy[time][vertex_id]['high'] += self.vertex_expected_occupancy[time][vertex_id]['poisson_binomial'][i]
            else:
                self.vertex_expected_occupancy[time][vertex_id]['low'] +=  self.vertex_expected_occupancy[time][vertex_id]['poisson_binomial'][i]


    def predict_occupancies(self, time_now, time_to_predict):
        self.get_tracks_by_time(time_now)
        self.predict_people_positions(time_now, time_to_predict)
        self.assign_people_to_areas(time_to_predict)
        self.calculate_poisson_binomial(time_to_predict)
        for vertex in self.vertices:
            self.predict_occupancies_for_vertex(time_to_predict, vertex.get_id())
        for edge in self.edges:
            self.predict_occupancies_for_edge(time_to_predict, edge.get_id())
        if time_to_predict not in self.vertex_expected_occupancy or time_to_predict not in self.edge_expected_occupancy:
            return None
        return (self.vertex_expected_occupancy[time_to_predict], self.edge_expected_occupancy[time_to_predict])


    def get_occupancies(self, time):
        if time not in self.vertex_expected_occupancy or time not in self.edge_expected_occupancy:
            return None
        return (self.vertex_expected_occupancy[time], self.edge_expected_occupancy[time])



    def plot_tracked_people(self):
        self.plot_topological_map()
        for person in self.people_trajectories:
            # print("person: ", self.people_trajectories[person])
            for person_position in self.people_trajectories[person]:
                plt.plot(person_position[1], person_position[2], 'bo')
        plt.show()

    
    def poisson_binomial(self, probabilities):
        # probabilities is a list of probabilities
        if not probabilities:
            return np.array([1.0, 0.0])

        P = [1.0-probabilities[0], probabilities[0]] # array of probabilities

        for i in range(1, len(probabilities)):
            new_probabilities = [0.0]*(len(P)+1)

            # fill in the new probabilities
            new_probabilities[0] = P[0]*(1-probabilities[i])
            new_probabilities[len(P)] = P[len(P) - 1]*probabilities[i]

            for j in range(1, len(P)):
                new_probabilities[j] = (P[j-1]*probabilities[i]) + (P[j]*(1-probabilities[i]))
            
            P = new_probabilities
        
        return np.array(P)


    def calculate_poisson_binomial(self, time):
        for time_probabilities in self.vertex_expected_occupancy:
            if time_probabilities == time:
                for vertex in self.vertex_expected_occupancy[time]:
                    probabilities = self.vertex_expected_occupancy[time][vertex]['probabilities']
                    poisson_binomial = self.poisson_binomial(probabilities)
                    self.vertex_expected_occupancy[time][vertex]['poisson_binomial'] = poisson_binomial

        for time_probabilities in self.edge_expected_occupancy:
            if time_probabilities == time:
                for edge in self.edge_expected_occupancy[time]:
                    probabilities = self.edge_expected_occupancy[time][edge]['probabilities']
                    poisson_binomial = self.poisson_binomial(probabilities)
                    self.edge_expected_occupancy[time][edge]['poisson_binomial'] = poisson_binomial


    def assign_people_to_areas(self, time):
        # print(self.predicted_positions)
        if not self.predicted_positions:
            return False
        self.vertex_expected_occupancy[time] = {}
        self.edge_expected_occupancy[time] = {}
        for person_predictions in self.predicted_positions:
            if person_predictions == []:
                continue
            weight_of_prediction = 1 /  len(person_predictions)
            
            person_vertex_occupancy = {}
            person_edge_occupancy = {}
            for position in person_predictions:
                for vertex in self.vertices:
                    if vertex.is_inside_area(position[1], position[2]):
                        if vertex.get_id() not in person_vertex_occupancy:
                            person_vertex_occupancy[vertex.get_id()] = 0
                        person_vertex_occupancy[vertex.get_id()] += weight_of_prediction

                for edge in self.edges: 
                    if edge.is_inside_area(position[1], position[2]):
                        if edge.get_id() not in person_edge_occupancy:
                            person_edge_occupancy[edge.get_id()] = 0
                        person_edge_occupancy[edge.get_id()] += weight_of_prediction
            
            for vertex in person_vertex_occupancy:
                if vertex not in self.vertex_expected_occupancy[time]:
                    self.vertex_expected_occupancy[time][vertex] = {}
                    self.vertex_expected_occupancy[time][vertex]['probabilities'] = []
                self.vertex_expected_occupancy[time][vertex]['probabilities'].append(person_vertex_occupancy[vertex])
            
            for edge in person_edge_occupancy:
                if edge not in self.edge_expected_occupancy[time]:
                    self.edge_expected_occupancy[time][edge] = {}
                    self.edge_expected_occupancy[time][edge]['probabilities'] = []
                self.edge_expected_occupancy[time][edge]['probabilities'].append(person_edge_occupancy[edge])


    def print_people_in_areas(self, time):
        for vertex in self.vertex_expected_occupancy[time]:
            print("Vertex: ", vertex)
            print("People in area: ", self.vertex_expected_occupancy[time][vertex]['probabilities'])
        
        for edge in self.edge_expected_occupancy[time]:
            print("Edge: ", edge)
            print("People in area: ", self.edge_expected_occupancy[time][edge]['probabilities'])

    def print_poisson_binomial(self, time):
        for vertex in self.vertex_expected_occupancy[time]:
            print("Vertex: ", vertex)
            print("Poisson Binomial: ", self.vertex_expected_occupancy[time][vertex]['poisson_binomial'])
        
        for edge in self.edge_expected_occupancy[time]:
            print("Edge: ", edge)
            print("Poisson Binomial: ", self.edge_expected_occupancy[time][edge]['poisson_binomial'])
            


    # remove the occupancy of the vertices and edges
    def reset_occupancies(self):
        self.vertex_occupancy = {}
        self.edge_occupancy = {}
        self.vertex_expected_occupancy = {}
        self.edge_expected_occupancy = {}































    # # find the occupancy for vertices and edges
    # def find_vertex_occupancy(self, vertex_id):
    #     if vertex_id in [vertex['id'] for vertex in self.vertex_occupancy]:
    #         return self.vertex_occupancy[vertex_id]
    #     return None
    
    # def find_edge_occupancy(self, edge_id):
    #     if edge_id in [edge['id'] for edge in self.edge_occupancy]:
    #         return self.edge_occupancy[edge_id]
    #     return None
    

    # # add the occupancy for vertices and edges
    # def add_vertex_occupancy(self, vertex_id, occupancy_high, occupancy_low, time):
    #     # check if the vertex exists
    #     if self.find_vertex_from_id(vertex_id) is None:
    #         return False
    #     if occupancy_high != (1 - occupancy_low):
    #         return False
    #     if time not in self.vertex_expected_occupancy:
    #         self.vertex_expected_occupancy[time] = {}
    #     elif vertex_id in self.vertex_expected_occupancy[time]:
    #         return False
    #     for vertex in self.vertices:
    #         if vertex.get_id() == vertex_id:
    #             if vertex_id not in self.vertex_expected_occupancy[time].keys():
    #                 self.vertex_expected_occupancy[time][vertex_id] = {}
    #                 self.vertex_expected_occupancy[time][vertex_id]['high'] = occupancy_high
    #                 self.vertex_expected_occupancy[time][vertex_id]['low'] = occupancy_low
    #     # add the vertex occupancy
    #     return True
    

    # def add_edge_occupancy(self, edge_id, occupancy_high, occupancy_low, time):
    #     # check if the edge exists
    #     if self.find_edge_from_id(edge_id) is None:
    #         return False
    #     if occupancy_high != (1 - occupancy_low):
    #         return False
    #     if time not in self.edge_expected_occupancy:
    #         self.edge_expected_occupancy[time] = {}
    #     elif edge_id in self.edge_expected_occupancy[time]:
    #         return False
    #     for edge in self.edges:
    #         if edge.get_id() == edge_id:
    #             if edge_id not in self.edge_expected_occupancy[time].keys():
    #                 self.edge_expected_occupancy[time][edge_id] = {}
    #                 self.edge_expected_occupancy[time][edge_id]['high'] = occupancy_high
    #                 self.edge_expected_occupancy[time][edge_id]['low'] = occupancy_low
    #     # add the edge occupancy
    #     return True        
        

    # # predict the occupancy of the vertices and edges
    # def predict_occupancies_for_edge_fixed(self, time, edge_id):
    #     # here I should call cliff
    #     if time not in self.edge_expected_occupancy:
    #         self.edge_expected_occupancy[time] = {}
    #     for edge in self.edges:
    #         if edge.get_id() == edge_id:
    #             if edge_id not in self.edge_expected_occupancy[time].keys():
    #                 self.edge_expected_occupancy[time][edge_id] = {}
    #                 self.edge_expected_occupancy[time][edge_id]['high'] = self.edge_expected_occupancy[0][edge_id]['high'] 
    #                 self.edge_expected_occupancy[time][edge_id]['low'] = self.edge_expected_occupancy[0][edge_id]['low'] 
    #     if edge_id in self.edge_expected_occupancy[time]:
    #         return True
    #     return False

    # def predict_occupancies_random(self, time):
    #     # here I should call cliff
    #     ret = True
    #     for vertex in self.vertices:
    #         ret = ret and self.predict_occupancies_for_vertex(time, vertex.get_id())
    #     for edge in self.edges:
    #         ret = ret and self.predict_occupancies_for_edge(time, edge.get_id())
    #     return ret
    
    # def predict_occupancies_for_edge_random(self, time, edge_id):
    #     # here I should call cliff
    #     if time not in self.edge_expected_occupancy:
    #         self.edge_expected_occupancy[time] = {}
    #     for edge in self.edges:
    #         if edge.get_id() == edge_id:
    #             if edge_id not in self.edge_expected_occupancy[time].keys():
    #                 self.edge_expected_occupancy[time][edge_id] = {}
    #                 self.edge_expected_occupancy[time][edge_id]['high'] = random.uniform(0,1)
    #                 self.edge_expected_occupancy[time][edge_id]['low'] = 1-self.edge_expected_occupancy[time][edge_id]['high']
    #     if edge_id in self.edge_expected_occupancy[time]:
    #         return True
    #     return False

    # def predict_occupancies_for_vertex_random(self, time, vertex_id):
    #     # here I should call cliff
    #     if time not in self.vertex_expected_occupancy:
    #         self.vertex_expected_occupancy[time] = {}
    #     for vertex in self.vertices:
    #         if vertex.get_id() == vertex_id:
    #             if vertex_id not in self.vertex_expected_occupancy[time].keys():
    #                 self.vertex_expected_occupancy[time][vertex_id] = {}
    #                 self.vertex_expected_occupancy[time][vertex_id]['high'] = random.uniform(0,1)
    #                 self.vertex_expected_occupancy[time][vertex_id]['low'] = 1-self.vertex_expected_occupancy[time][vertex_id]['high']
                    
    #     if vertex_id in self.vertex_expected_occupancy[time]:
    #         return True
    #     return False




    # # remove the occupancy of the vertices and edges
    # def remove_vertex_occupancy(self, vertex_id):
    #     self.vertex_occupancy = [vertex for vertex in self.vertex_occupancy if vertex['id'] != vertex_id]

    # def remove_edge_occupancy(self, edge_id):
    #     self.edge_occupancy = [edge for edge in self.edge_occupancy if edge['id'] != edge_id]





        # for vertex in self.vertices:
        #     if vertex.is_inside_area(person_position[0], person_position[1]):
        #         if time not in self.vertex_expected_occupancy:
        #             self.vertex_expected_occupancy[time] = {}
        #         if vertex.get_id() not in self.vertex_expected_occupancy[time]:
        #             self.vertex_expected_occupancy[time][vertex.get_id()] = {}
        #             self.vertex_expected_occupancy[time][vertex.get_id()]['high'] = 0
        #             self.vertex_expected_occupancy[time][vertex.get_id()]['low'] = 0
        #         self.vertex_expected_occupancy[time][vertex.get_id()]['high'] += 1
        #         self.vertex_expected_occupancy[time][vertex.get_id()]['low'] += 1
        #         return True
            


    # def assign_people_to_areas(self, people_positions, time):
    #     if time not in self.vertex_expected_occupancy:
    #         self.vertex_expected_occupancy[time] = {}
    #     for vertex in self.vertices:
    #         if vertex.get_id() not in self.vertex_expected_occupancy[time]:
    #             self.vertex_expected_occupancy[time][vertex.get_id()] = {}
    #             self.vertex_expected_occupancy[time][vertex.get_id()]['high'] = 0
    #             self.vertex_expected_occupancy[time][vertex.get_id()]['low'] = 0
    #     for person in people_positions:


    
    # return the people predicted positions at a certain time
    # return a list of lists of positions
    # def get_people_predicted_positions(self, time):
    #     to_return = []
    #     for person in self.people_predicted_positions:
    #         person_prediction = []
    #         for trajectory in person:
    #             timedelta = len(trajectory) - 1
    #             if timedelta >= time:
    #                 person_prediction.append(trajectory[time])
    #         to_return.append(person_prediction)
    #     self.predicted_positions = to_return


    # def get_people_detections(self, time_to_detect, timespan):
    #     human_traj_data = read_iit_human_traj_data(self.cliffPredictor.ground_truth_data_file)
    #     human_traj_data_by_time = human_traj_data.loc[human_traj_data['time'] in range(time_to_detect-timespan, time_to_detect)]
    #     return human_traj_data_by_time
    #     # get the people by time



    # def get_current_occupancies(self, time):
    #     tracks = self.get_tracks_by_time(time)
    #     self.people_predicted_positions = {}
    #     self.people_predicted_positions = self.cliffPredictor.predict_positions(tracks, time)
    #     self.assign_people_to_areas(time)

        
    # def track_current_people(self):
    #     human_traj_data = read_iit_human_traj_data(self.cliffPredictor.ground_truth_data_file)
    #     human_ids = list(human_traj_data.person_id.unique())

    #     # print("human_traj_data: ", human_traj_data)
    #     self.people_trajectories = {}
    #     for person_number in range(0, 200):
    #         id = human_ids[person_number]
            
    #         human_traj_data_by_person_id = human_traj_data.loc[human_traj_data['person_id'] == id]
    #         human_traj_array = human_traj_data_by_person_id[["time", "x", "y", "velocity", "motion_angle"]].to_numpy()

    #         # human_traj = get_human_traj_data_by_person_id(human_traj_data, id)
    #         if len(human_traj_array) < 6:
    #             continue
    #         # for i in range(0, len(human_traj)):
    #         # if not self.people_trajectories.get(id):
    #         #     self.people_trajectories[id] = []
    #         self.people_trajectories[id] = human_traj_array