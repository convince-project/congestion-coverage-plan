import csv
import matplotlib.pyplot as plt
import sys 
import numpy as np
from datetime import datetime
from scipy.stats import mannwhitneyu
def get_time(row):
    return float(row.split(',')[0][1:])

def get_statistics(csv_file, max_levels = 8):
    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        # next(reader)
        data = [row for row in reader]
    # if csv_file2 is not None:
    #     with open(csv_file, 'r') as file:
    #         reader = csv.reader(file)
    #         next(reader)
    #         data2 = [row for row in reader]
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
    # cpu_time_tsp = []
    cpu_time_avg_tsp_levels = {}
    cpu_time_min_tsp_levels = {}
    cpu_time_max_tsp_levels = {}
    cpu_time_current_tsp_levels = {}
    cpu_time_lrtdp_levels = {}

    for i in range (2, max_levels):
        cpu_time_avg_tsp_levels[str(i)] = []
        cpu_time_lrtdp_levels[str(i)] = []
    cpu_time_avg_tsp = []
    cpu_time_min_tsp = []
    cpu_time_max_tsp = []
    cpu_time_current_tsp = []
    cpu_time_lrtdp = []

    for row_id in range(0, len(data), num_rows):
        min_time = 99999999
        for i in range(0,num_rows -1 ):
            if get_time(data[row_id+i][2]) < min_time:
                min_time = get_time(data[row_id+i][2])
        time_lrtdp = get_time(data[row_id+num_rows -1][2])
        for i in range(0,num_rows ):
            if data[row_id+i][1] == "steps_avg":
                time_avg_tsp.append(get_time(data[row_id+i][2]))
                time_occured = datetime.strptime(data[row_id+i][3], "%H:%M:%S.%f")
                cpu_time_avg_tsp.append(float(time_occured.microsecond / 1000000 + time_occured.second + time_occured.minute * 60 + time_occured.hour * 3600))
                if data[row_id+i][-1] not in cpu_time_avg_tsp_levels:
                    cpu_time_avg_tsp_levels[str(data[row_id+i][-1])] = []
                cpu_time_avg_tsp_levels[str(data[row_id+i][-1])].append(cpu_time_avg_tsp[-1])
                number_of_collisions_avg_tsp.append(get_collisions(data[row_id+i][3]))
            
            if data[row_id+i][1] == "steps_min":
                time_min_tsp.append(get_time(data[row_id+i][2]))
                time_occured = datetime.strptime(data[row_id+i][3], "%H:%M:%S.%f")
                cpu_time_min_tsp.append(float(time_occured.microsecond / 1000000 + time_occured.second + time_occured.minute * 60 + time_occured.hour * 3600))
                if data[row_id+i][-1] not in cpu_time_min_tsp_levels:
                    cpu_time_min_tsp_levels[str(data[row_id+i][-1])] = []
                cpu_time_min_tsp_levels[str(data[row_id+i][-1])].append(cpu_time_min_tsp[-1])
                number_of_collisions_min_tsp.append(get_collisions(data[row_id+i][3]))


            if data[row_id+i][1] == "steps_max":
                time_max_tsp.append(get_time(data[row_id+i][2]))
                time_occured = datetime.strptime(data[row_id+i][3], "%H:%M:%S.%f")
                cpu_time_max_tsp.append(float(time_occured.microsecond / 1000000 + time_occured.second + time_occured.minute * 60 + time_occured.hour * 3600))
                if data[row_id+i][-1] not in cpu_time_max_tsp_levels:
                    cpu_time_max_tsp_levels[str(data[row_id+i][-1])] = []
                cpu_time_max_tsp_levels[str(data[row_id+i][-1])].append(cpu_time_max_tsp[-1])
                number_of_collisions_max_tsp.append(get_collisions(data[row_id+i][3]))
                # print("cpu_time_max_tsp", cpu_time_max_tsp[-1])
            if data[row_id+i][1] == "steps_curr":
                time_current_tsp.append(get_time(data[row_id+i][2]))
                time_occured = datetime.strptime(data[row_id+i][3], "%H:%M:%S.%f")
                cpu_time_current_tsp.append(float(time_occured.microsecond / 1000000 + time_occured.second + time_occured.minute * 60 + time_occured.hour * 3600))
                if data[row_id+i][-1] not in cpu_time_current_tsp_levels:
                    cpu_time_current_tsp_levels[str(data[row_id+i][-1])] = []
                cpu_time_current_tsp_levels[str(data[row_id+i][-1])].append(cpu_time_current_tsp[-1])
                number_of_collisions_current_tsp.append(get_collisions(data[row_id+i][3]))

            if data[row_id+i][1] == "steps_lrtdp":
                time_avg_lrtdp.append(get_time(data[row_id+i][2]))
                if data[row_id+i][-1] not in time_lrtdp_levels:
                    time_lrtdp_levels[str(data[row_id+i][-1])] = []
                time_lrtdp_levels[str(data[row_id+i][-1])].append(get_time(data[row_id+i][2]))
                if data[row_id+i][-1] not in collisions_lrtdp_levels:
                    collisions_lrtdp_levels[str(data[row_id+i][-1])] = []
                collisions_lrtdp_levels[str(data[row_id+i][-1])].append(get_collisions(data[row_id+i][3]))
                time_occured = datetime.strptime(data[row_id+i][4], "%H:%M:%S.%f")
                cpu_time_local = float(time_occured.microsecond / 1000000 + time_occured.second + time_occured.minute * 60 + time_occured.hour * 3600)
                cpu_time_lrtdp.append(cpu_time_local)
                cpu_time_lrtdp_levels[str(data[row_id+i][-1])].append(cpu_time_local)
                number_of_collisions_lrtdp.append(get_collisions(data[row_id+i][3]))

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
    

    # print("colllisions_avg_tsp", number_of_collisions_avg_tsp)
    # print("colllisions_min_tsp", number_of_collisions_min_tsp)
    # print("colllisions_max_tsp", number_of_collisions_max_tsp)
    # print("colllisions_current_tsp", number_of_collisions_current_tsp)
    # print("colllisions_lrtdp", number_of_collisions_lrtdp)

    # for i in range(0, len(data)):
    #     print(labels[i], np.mean(data[i]))
    # plt.show()
    # plt.ylim(0, 50)
    p = mannwhitneyu( time_avg_lrtdp, time_avg_tsp, alternative='less')
    print("p-value avg tsp", p[1])
    p = mannwhitneyu( time_avg_lrtdp, time_min_tsp, alternative='less')
    print("p-value min tsp", p[1])
    p = mannwhitneyu( time_avg_lrtdp, time_max_tsp, alternative='less')
    print("p-value max tsp", p[1])
    p = mannwhitneyu( time_avg_lrtdp, time_current_tsp, alternative='less')
    print("p-value current tsp", p[1])
    p = mannwhitneyu( number_of_collisions_lrtdp, number_of_collisions_avg_tsp, alternative='less')
    print("p-value collisions avg tsp", p[1])
    p = mannwhitneyu( number_of_collisions_lrtdp, number_of_collisions_min_tsp, alternative='less')
    print("p-value collisions min tsp", p[1])
    p = mannwhitneyu( number_of_collisions_lrtdp, number_of_collisions_max_tsp, alternative='less')
    print("p-value collisions max tsp", p[1])
    p = mannwhitneyu( number_of_collisions_lrtdp, number_of_collisions_current_tsp, alternative='less')
    print("p-value collisions current tsp", p[1])
    for i in range(2, max_levels):
        p = mannwhitneyu( time_lrtdp_levels[str(i)], time_avg_tsp_levels[str(i)], alternative='less')
        print("p-value avg tsp level", i, p[1])
        p = mannwhitneyu( time_lrtdp_levels[str(i)], time_min_tsp_levels[str(i)], alternative='less')
        print("p-value min tsp level", i, p[1])
        p = mannwhitneyu( time_lrtdp_levels[str(i)], time_max_tsp_levels[str(i)], alternative='less')
        print("p-value max tsp level", i, p[1])
        p = mannwhitneyu( time_lrtdp_levels[str(i)], time_current_tsp_levels[str(i)], alternative='less')
        print("p-value current tsp level", i, p[1])
        p = mannwhitneyu( collisions_lrtdp_levels[str(i)], collisions_avg_tsp_levels[str(i)], alternative='less')
        print("p-value collisions avg tsp level", i, p[1])
        p = mannwhitneyu( collisions_lrtdp_levels[str(i)], collisions_min_tsp_levels[str(i)], alternative='less')
        print("p-value collisions min tsp level", i, p[1])
        p = mannwhitneyu( collisions_lrtdp_levels[str(i)], collisions_max_tsp_levels[str(i)], alternative='less')
        print("p-value collisions max tsp level", i, p[1])
        p = mannwhitneyu( collisions_lrtdp_levels[str(i)], collisions_current_tsp_levels[str(i)], alternative='less')
        print("p-value collisions current tsp level", i, p[1])
    # ax.boxplot(time_avg_tsp, label = "tsp_avg")
    # ax.boxplot(time_min_tsp, label = "tsp_min")
    # ax.boxplot(time_max_tsp, label = "tsp_max")
    # ax.boxplot(time_current_tsp, label = "tsp_curr")
    # ax.boxplot(time_avg_lrtdp, label = "lrtdp")

    print("mean time avg tsp", np.mean(time_avg_tsp), "min time avg tsp", np.min(time_avg_tsp), "max time avg tsp", np.max(time_avg_tsp))
    print("mean time min tsp", np.mean(time_min_tsp), "min time min tsp", np.min(time_min_tsp), "max time min tsp", np.max(time_min_tsp))
    print("mean time max tsp", np.mean(time_max_tsp), "min time max tsp", np.min(time_max_tsp), "max time max tsp", np.max(time_max_tsp))
    print("mean time current tsp", np.mean(time_current_tsp), "min time current tsp", np.min(time_current_tsp), "max time current tsp", np.max(time_current_tsp))
    print("mean time avg lrtdp", np.mean(time_avg_lrtdp), "min time avg lrtdp", np.min(time_avg_lrtdp), "max time avg lrtdp", np.max(time_avg_lrtdp))

    print("mean cpu time avg tsp", np.mean(cpu_time_avg_tsp), "min cpu time avg tsp", np.min(cpu_time_avg_tsp), "max cpu time avg tsp", np.max(cpu_time_avg_tsp))
    print("mean cpu time min tsp", np.mean(cpu_time_min_tsp), "min cpu time min tsp", np.min(cpu_time_min_tsp), "max cpu time min tsp", np.max(cpu_time_min_tsp))
    print("mean cpu time max tsp", np.mean(cpu_time_max_tsp), "min cpu time max tsp", np.min(cpu_time_max_tsp), "max cpu time max tsp", np.max(cpu_time_max_tsp))
    print("mean cpu time current tsp", np.mean(cpu_time_current_tsp), "min cpu time current tsp", np.min(cpu_time_current_tsp), "max cpu time current tsp", np.max(cpu_time_current_tsp))
    print("mean cpu time avg lrtdp", np.mean(cpu_time_lrtdp), "min cpu time avg lrtdp", np.min(cpu_time_lrtdp), "max cpu time avg lrtdp", np.max(cpu_time_lrtdp))
    # plot the times for the execution of the lrtdp and tsp algorithms
    fig = plt.figure(figsize =(10, 7))
    ax = fig.add_subplot(111)
    data = [time_avg_tsp, time_min_tsp, time_max_tsp, time_current_tsp, time_avg_lrtdp]
    labels = ["tsp_avg", "tsp_min", "tsp_max", "tsp_curr", "lrtdp"]
    ax.boxplot(data, labels = labels)
    ax.set_title(csv_file.split("/")[-1].split(".")[0] + " execution time (no planning time considered)")
    plt.ylabel("Execution time (s)")
    plt.xlabel("Algorithms")
    plt.grid()
    print("lrtdp_best", lrtdp_count, "tsp_best", time_best_tsp, "equal", time_equal, "row_count", row_count)
    print("lrtdp_time_delta", np.mean(time_delta_better_lrtdp), "min_lrtdp", time_delta_min_lrtdp, "max_lrtdp", time_delta_max_lrtdp)
    print("tsp_time_delta", np.mean(time_delta_better_tsp), "min_tsp", time_delta_min_tsp, "max_tsp", time_delta_max_tsp)
    plt.show()




    # plot the execution time for the lrtdp and tsp algorithms for each level
    for i in range(2, max_levels):
        fig = plt.figure(figsize =(10, 7))
        ax = fig.add_subplot(111)
        ax.set_title(csv_file.split("/")[-1].split(".")[0] + " execution time (level " + str(i) + ") (no planning time considered)")
        data = [time_avg_tsp_levels[str(i)], time_min_tsp_levels[str(i)], time_max_tsp_levels[str(i)], time_current_tsp_levels[str(i)], time_lrtdp_levels[str(i)]]
        labels = ["tsp_avg", "tsp_min", "tsp_max", "tsp_curr", "lrtdp"]
        ax.boxplot(data, labels = labels)
        plt.ylabel("Execution time (s)")
        plt.xlabel("Algorithms")
        plt.grid()
        plt.show()


    # plot the times for the planning of the lrtdp and tsp algorithms
    fig = plt.figure(figsize =(10, 7))
    ax = fig.add_subplot(111)
    ax.set_title(csv_file.split("/")[-1].split(".")[0] + " execution time")
    # data = [cpu_time_tsp, cpu_time_lrtdp]
    # labels = ["tsp_avg", "lrtdp"]
    data = [cpu_time_avg_tsp, cpu_time_min_tsp, cpu_time_max_tsp, cpu_time_current_tsp, cpu_time_lrtdp]
    labels = ["tsp_avg", "tsp_min", "tsp_max", "tsp_curr", "lrtdp"]
    # plt.ylim(0, 50)
    ax.boxplot(data, labels = labels)
    plt.ylabel("Planning time (s)")
    plt.xlabel("Algorithms")
    plt.grid()
    plt.show()

    # plot the planning time for the execution of the lrtdp and tsp algorithms for each level
    for i in range(2, max_levels):
        fig = plt.figure(figsize =(10, 7))
        ax = fig.add_subplot(111)
        ax.set_title(csv_file.split("/")[-1].split(".")[0] + " planning time (level " + str(i) + ")")
        data = [cpu_time_avg_tsp_levels[str(i)], cpu_time_min_tsp_levels[str(i)], cpu_time_max_tsp_levels[str(i)], cpu_time_current_tsp_levels[str(i)], cpu_time_lrtdp_levels[str(i)]]
        labels = ["tsp_avg", "tsp_min", "tsp_max", "tsp_curr", "lrtdp"]
        ax.boxplot(data, labels = labels)
        plt.ylabel("Planning time (s)")
        plt.xlabel("Algorithms")
        plt.grid()
        plt.show()

    # plot the number of collisions for the lrtdp and tsp algorithms
    fig = plt.figure(figsize =(10, 7))
    ax = fig.add_subplot(111)
    ax.set_title(csv_file.split("/")[-1].split(".")[0] + " number of collisions")
    data = [number_of_collisions_avg_tsp, number_of_collisions_min_tsp, number_of_collisions_max_tsp, number_of_collisions_current_tsp, number_of_collisions_lrtdp]
    labels = ["tsp_avg", "tsp_min", "tsp_max", "tsp_curr", "lrtdp"]
    ax.boxplot(data, labels = labels)
    plt.ylabel("Number of collisions")
    plt.xlabel("Algorithms")
    plt.grid()
    plt.show()

    # plot the number of collisions for the execution of the lrtdp and tsp algorithms for each level
    for i in range(2, max_levels):
        fig = plt.figure(figsize =(10, 7))
        ax = fig.add_subplot(111)
        ax.set_title(csv_file.split("/")[-1].split(".")[0] + " number of collisions (level " + str(i) + ")")
        data = [collisions_avg_tsp_levels[str(i)], collisions_min_tsp_levels[str(i)], collisions_max_tsp_levels[str(i)], collisions_current_tsp_levels[str(i)], collisions_lrtdp_levels[str(i)]]
        labels = ["tsp_avg", "tsp_min", "tsp_max", "tsp_curr", "lrtdp"]
        ax.boxplot(data, labels = labels)
        plt.ylabel("Number of collisions")
        plt.xlabel("Algorithms")
        plt.grid()
        plt.show()

    # plot the times for the execution of the lrtdp and tsp algorithms for each level
    fig = plt.figure(figsize =(10, 7))
    ax = fig.add_subplot(111)
    # print(cpu_time_lrtdp_levels)
    ax.set_title(csv_file.split("/")[-1].split(".")[0] + " cpu time (levels)")
    data = [cpu_time_lrtdp_levels[str(i)] for i in range(2, max_levels)]
    labels = ["lrtdp_" + str(i) for i in range(2, max_levels)]
    ax.boxplot(data, labels = labels)
    plt.ylabel("CPU time (s)")
    plt.xlabel("Algorithms")
    plt.grid()
    plt.show()
    print("---- DONE PLOTTING ----")

    # plot the times for the execution of the tsp algorithms for each level

    # fig = plt.figure(figsize =(10, 7))
    # ax = fig.add_subplot(111)
    # labels = ["tsp_avg_" + str(i) for i in range(2, max_levels)]
    # data = [time_delta_better_lrtdp, time_delta_better_tsp]
    # labels = ["lrtdp", "tsp"]
    # ax.boxplot(data, labels = labels)
    # plt.show()
if __name__ == '__main__':
    # get_statistics("steps_iit_time_iter.csv")
    # get_statistics("steps_small_occupancy_map_atc_corridor_mixed.csv")
    # get_statistics("steps_medium_occupancy_map_atc_corridor_mixed.csv")
    get_statistics(sys.argv[1], int(sys.argv[2]))