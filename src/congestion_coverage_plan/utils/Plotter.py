import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import matplotlib.cm as cm
from matplotlib.colors import Normalize
import congestion_coverage_plan.utils.dataset_utils as dataset_utils



def plot_positions(filename):
    data = dataset_utils.read_human_traj_data_from_file(filename)
    data = data.to_numpy()
    positions = []
    for data_index in range(len(data)):
        positions.append([data[data_index][2], data[data_index][3]])
    positions = np.array(positions)
    plt.scatter(positions[:, 0], positions[:, 1], s=1)
    # assert occupancy_map.add_vertex_with_id("vertex1", 0, -12)
    # assert occupancy_map.add_vertex_with_id("vertex2", 1, -2)
    # assert occupancy_map.add_vertex_with_id("vertex3", 3, -6)
    # assert occupancy_map.add_vertex_with_id("vertex4", 8, -10)
    # assert occupancy_map.add_vertex_with_id("vertex5", 6, -3)
    plt.scatter(0, -12, s=100, c='red', label='vertex1')
    plt.scatter(1, -2, s=100, c='red', label='vertex2')
    plt.scatter(3, -6, s=100, c='red', label='vertex3')
    plt.scatter(8, -10, s=100, c='red', label='vertex4')
    plt.scatter(6, -3, s=100, c='red', label='vertex5')


    plt.show()

def plot_human_traj(human_traj_data, observed_tracklet_length):
    # plt.scatter(human_traj_data[observed_tracklet_length:, 1], human_traj_data[observed_tracklet_length:, 2], marker='o', alpha=1, color="y", s=50, label="Ground truth")
    plt.scatter(human_traj_data[observed_tracklet_length:, 1], human_traj_data[observed_tracklet_length:, 2], marker='o', alpha=1, color="b", s=50, label="Ground truth")


def plot_observed_tracklet(total_predicted_motion_list, observed_tracklet_length):
    for predicted_traj in total_predicted_motion_list:
        shape = predicted_traj.shape
        (u, v) = dataset_utils.pol2cart(predicted_traj[:, 3], predicted_traj[:, 4])
        for i in range(0, observed_tracklet_length):
            plt.scatter(predicted_traj[i, 1], predicted_traj[i, 2], color="limegreen", marker="o", s=50)

# observed_tracklet_length 
def plot_all_predicted_trajs(total_predicted_motion_list, observed_tracklet_length):
    for predicted_traj in total_predicted_motion_list:
        print(predicted_traj)
        shape = predicted_traj.shape
        (u, v) = dataset_utils.pol2cart(predicted_traj[:, 3], predicted_traj[:, 4])
        for i in range(0, observed_tracklet_length):
            plt.scatter(predicted_traj[i, 1], predicted_traj[i, 2], color="limegreen", marker="o", s=50)
        # plt.scatter(predicted_traj[observed_tracklet_length:, 1], predicted_traj[observed_tracklet_length:, 2], color="b", marker="o", s=50)
        for i in range(observed_tracklet_length, shape[0]):
            total = shape[0] - observed_tracklet_length
            plt.scatter(predicted_traj[i, 1], predicted_traj[i, 2], color="b", marker="o", alpha=1-(i-observed_tracklet_length)/total, s=50)


def plot_cliff_map(cliff_map_data):
    (u, v) = dataset_utils.pol2cart(cliff_map_data[:, 3], cliff_map_data[:, 2])
    color = cliff_map_data[:, 2]
    plt.quiver(cliff_map_data[:, 0], cliff_map_data[:, 1], u, v, color, alpha=0.7, cmap="hsv")

