import csv
import matplotlib.pyplot as plt
import sys 
import numpy as np
def get_time(row):
    return float(row.split(',')[0][1:])

def get_statistics(csv_file):
    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        next(reader)
        data = [row for row in reader]
    
    lrtdp_count = 0
    time_equal = 0
    time_best_tsp = 0
    row_count = 0
    num_rows = 5
    time_delta_better_lrtdp = []
    time_delta_better_tsp = []
    time_delta_min_tsp = 999999
    time_delta_max_tsp = 0
    time_delta_min_lrtdp = 999999
    time_delta_max_lrtdp = 0
    time_avg_tsp = []
    time_avg_lrtdp = []
    time_min_tsp = []
    time_max_tsp = []
    time_current_tsp = []

    for row_id in range(0, len(data), num_rows):
        min_time = 99999999
        for i in range(0,num_rows -1 ):
            if get_time(data[row_id+i][2]) < min_time:
                min_time = get_time(data[row_id+i][2])
        time_lrtdp = get_time(data[row_id+num_rows -1][2])
        for i in range(0,num_rows ):
            if data[row_id+i][1] == "steps_avg":
                time_avg_tsp.append(get_time(data[row_id+i][2]))
            if data[row_id+i][1] == "steps_min":
                time_min_tsp.append(get_time(data[row_id+i][2]))
            if data[row_id+i][1] == "steps_max":
                time_max_tsp.append(get_time(data[row_id+i][2]))
            if data[row_id+i][1] == "steps_curr":
                time_current_tsp.append(get_time(data[row_id+i][2]))
            if data[row_id+i][1] == "steps_lrtdp":
                time_avg_lrtdp.append(get_time(data[row_id+i][2]))

        if time_lrtdp < min_time:
            lrtdp_count += 1
            time_delta_better_lrtdp.append(min_time - time_lrtdp)
            if min_time - time_lrtdp < time_delta_min_lrtdp:
                time_delta_min_lrtdp = min_time - time_lrtdp
            if min_time - time_lrtdp > time_delta_max_lrtdp:
                time_delta_max_lrtdp = min_time - time_lrtdp
        elif time_lrtdp > min_time:
            time_best_tsp += 1
            time_delta_better_tsp.append(time_lrtdp - min_time)
            if time_lrtdp - min_time < time_delta_min_tsp:
                time_delta_min_tsp = time_lrtdp - min_time
            if time_lrtdp - min_time > time_delta_max_tsp:
                time_delta_max_tsp = time_lrtdp - min_time
        elif time_lrtdp == min_time:
            time_equal += 1
        row_count += 1
    
    fig = plt.figure(figsize =(10, 7))
    ax = fig.add_subplot(111)
    data = [time_avg_tsp, time_min_tsp, time_max_tsp, time_current_tsp, time_avg_lrtdp]
    labels = ["tsp_avg", "tsp_min", "tsp_max", "tsp_curr", "lrtdp"]
    ax.boxplot(data, labels = labels)
    # ax.boxplot(time_avg_tsp, label = "tsp_avg")
    # ax.boxplot(time_min_tsp, label = "tsp_min")
    # ax.boxplot(time_max_tsp, label = "tsp_max")
    # ax.boxplot(time_current_tsp, label = "tsp_curr")
    # ax.boxplot(time_avg_lrtdp, label = "lrtdp")
    print("lrtdp_best", lrtdp_count, "tsp_best", time_best_tsp, "equal", time_equal, "row_count", row_count)
    print("lrtdp_time_delta", np.mean(time_delta_better_lrtdp), "min_lrtdp", time_delta_min_lrtdp, "max_lrtdp", time_delta_max_lrtdp)
    print("tsp_time_delta", np.mean(time_delta_better_tsp), "min_tsp", time_delta_min_tsp, "max_tsp", time_delta_max_tsp)
    for i in range(0, len(data)):
        print(labels[i], np.mean(data[i]))
    # plt.show()

    # fig = plt.figure(figsize =(10, 7))
    # ax = fig.add_subplot(111)
    # data = [time_delta_better_lrtdp, time_delta_better_tsp]
    # labels = ["lrtdp", "tsp"]
    # ax.boxplot(data, labels = labels)
    # plt.show()
if __name__ == '__main__':
    # get_statistics("steps_iit_time_iter.csv")
    # get_statistics("steps_small_occupancy_map_atc_corridor_mixed.csv")
    get_statistics("steps_medium_occupancy_map_atc_corridor_mixed.csv")
    # get_statistics(sys.argv[1])