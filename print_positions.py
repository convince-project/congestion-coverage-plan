from utils import *
import matplotlib.pyplot as plt

def print_positions(filename):
    data = read_human_traj_data_from_file(filename)
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

    
    

if __name__ == "__main__":
    # filename = "dataset/atc/atc_reduced.csv"
    filename = "dataset/iit/iit.csv"
    print_positions(filename)
