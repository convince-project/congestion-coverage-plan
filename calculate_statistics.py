import csv
import matplotlib.pyplot as plt
import sys 
import numpy as np
from datetime import datetime
from scipy.stats import mannwhitneyu
def get_time(row):
    return float(row.split('.')[0][1:])

    # convert the string to a float
    # row = float(row)

    # return eval(row)


def get_collisions(row):
    collisions = 0
    # row = list(row)
    # convert the string to a list of tuples
    row = eval(row)
    # print(row)
    for x in row:
        # print(type(x))
        collisions += x[1]
    return collisions
        

class Execution:
    def __init__(self, time):
        self.time = time
        self.executions = {}

    def add_execution(self, algorithm, levels, planning_time, number_of_collisions, execution_time, steps):
        algorithm_name  = algorithm + "_" + str(levels)
        if algorithm_name not in self.executions:
            self.executions[algorithm_name] = {}
        self.executions[algorithm_name]['planning_time'] = planning_time
        self.executions[algorithm_name]['number_of_collisions'] = number_of_collisions
        self.executions[algorithm_name]['execution_time'] = execution_time
        self.executions[algorithm_name]['steps'] = steps


    def calculate_min_execution_time(self):
        min_time = 99999999
        for algorithm in self.executions:
            if self.executions[algorithm]['execution_time'] < min_time:
                min_time = self.executions[algorithm]['execution_time']
        return min_time
    
    def calculate_min_collisions(self):
        min_collisions = 99999999
        for algorithm in self.executions:
            if self.executions[algorithm]['number_of_collisions'] < min_collisions:
                min_collisions = self.executions[algorithm]['number_of_collisions']
        return min_collisions
    
    def calculate_min_planning_time(self):
        min_planning_time = 99999999
        for algorithm in self.executions:
            if self.executions[algorithm]['planning_time'] < min_planning_time:
                min_planning_time = self.executions[algorithm]['planning_time']
        return min_planning_time

    # def calculate_statistics(self):

        


    


def get_statistics(csv_file, max_levels = 8):
    csv_file_tsp = csv_file.split(".")[0] + "_tsp30.csv"
    csv_file_lrtdp = csv_file.split(".")[0] + "_lrtdp30.csv"
    with open(csv_file_tsp, 'r') as file:
        reader = csv.reader(file)
        # next(reader)
        data_tsp = [row for row in reader]
    with open(csv_file_lrtdp, 'r') as file:
        reader = csv.reader(file)
        # next(reader)
        data_lrtdp = [row for row in reader]
    # if csv_file2 is not None:
    #     with open(csv_file, 'r') as file:
    #         reader = csv.reader(file)
    #         next(reader)
    #         data2 = [row for row in reader]
    lrtdp_count = 0
    time_equal = 0
    time_best_tsp = 0
    row_count = 0
    num_rows = 4
    collisions_better_lrtdp = []
    collisions_better_tsp = []
    time_delta_better_lrtdp = []
    time_delta_better_tsp = []
    time_delta_min_lrtdp = 99999999
    time_delta_max_lrtdp = -99999999
    time_delta_min_tsp = 99999999
    time_delta_max_tsp = -99999999
    planning_time_lrtdp_per_step_per_level = {}

    times = []
    execution_time = {}
    cpu_time = {}
    collisions = {}

    labels = ["steps_avg", "steps_min", "steps_max", "steps_curr", "steps_lrtdp"]
    num_rows = len(labels)
    for label in labels:
        execution_time[label] = {}
        cpu_time[label] = {}
        collisions[label] = {}
        for i in [2,5,8]:
            execution_time[label][str(i)] = []
            cpu_time[label][str(i)] = []
            collisions[label][str(i)] = []
            planning_time_lrtdp_per_step_per_level[str(i)] = {}
    for i in range(0, len(data_lrtdp), num_rows * 6):
        times.append(float(data_lrtdp[i][0]))
    # print(len(data_lrtdp), "rows in the csv file", csv_file_lrtdp)
    for row_id in range(0, len(data_lrtdp), num_rows):
        print("Processing row", row_id, "of", len(data_lrtdp))
        ## PROCESS LRTDP RESULTS
        time_lrtdp = get_time(data_lrtdp[row_id][2])
        times_lrtdp = data_lrtdp[row_id][-2]
        times_lrtdp = eval(times_lrtdp)

        if len(times_lrtdp) != 0:
            for i in range(0, len(times_lrtdp)):
                if str(i) not in planning_time_lrtdp_per_step_per_level[str(data_lrtdp[row_id][-1])]:
                    planning_time_lrtdp_per_step_per_level[str(data_lrtdp[row_id][-1])][str(i)] = []
                planning_time_lrtdp_per_step_per_level[str(data_lrtdp[row_id][-1])][str(i)].append(float(times_lrtdp[i]))
        cpu_time["steps_lrtdp"][str(data_lrtdp[row_id][-1])].append(float(datetime.strptime(data_lrtdp[row_id][4], "%H:%M:%S.%f").microsecond / 1000000 + datetime.strptime(data_lrtdp[row_id][4], "%H:%M:%S.%f").second + datetime.strptime(data_lrtdp[row_id][4], "%H:%M:%S.%f").minute * 60 + datetime.strptime(data_lrtdp[row_id][4], "%H:%M:%S.%f").hour * 3600))
        times_steps_local = eval(data_lrtdp[row_id][-3])
        times_cpu_local = eval(data_lrtdp[row_id][-2])
        execution_time_local = times_cpu_local[0]
        for j in range(1, len(times_steps_local)-1):
            execution_time_local += max(times_steps_local[j], times_cpu_local[j+1])
        execution_time[data_lrtdp[row_id][1]][str(data_lrtdp[row_id][-1])].append(execution_time_local)
        collisions[data_lrtdp[row_id][1]][str(data_lrtdp[row_id][-1])].append(get_collisions(data_lrtdp[row_id][3]))
        min_time = 99999999
        min_collisions_tsp = 9999999
        for tsp_row_id in range(row_id, row_id + num_rows):
            if get_time(data_tsp[tsp_row_id][2]) < min_time:
                min_time = get_time(data_tsp[tsp_row_id][2])

            execution_time[data_tsp[tsp_row_id][1]][str(data_tsp[tsp_row_id][-1])].append(float(data_tsp[tsp_row_id][2]))
            cpu_time[data_tsp[tsp_row_id][1]][str(data_tsp[tsp_row_id][-1])].append(float(datetime.strptime(data_tsp[tsp_row_id][4], "%H:%M:%S.%f").microsecond / 1000000 + datetime.strptime(data_tsp[tsp_row_id][4], "%H:%M:%S.%f").second + datetime.strptime(data_tsp[tsp_row_id][4], "%H:%M:%S.%f").minute * 60 + datetime.strptime(data_tsp[tsp_row_id][4], "%H:%M:%S.%f").hour * 3600))
            collisions[data_tsp[tsp_row_id][1]][str(data_tsp[tsp_row_id][-1])].append(get_collisions(data_tsp[tsp_row_id][3]))

            if collisions[data_tsp[tsp_row_id][1]][str(data_tsp[tsp_row_id][-1])][-1] < min_collisions_tsp:
                min_collisions_tsp = collisions[data_tsp[tsp_row_id][1]][str(data_tsp[tsp_row_id][-1])][-1]


        ### evaluation
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

        if collisions[data_lrtdp[row_id][1]][str(data_lrtdp[row_id][-1])][-1] < min_collisions_tsp:
            collisions_better_lrtdp.append(collisions[data_lrtdp[row_id][1]][str(data_lrtdp[row_id][-1])][-1])
        elif collisions[data_lrtdp[row_id][1]][str(data_lrtdp[row_id][-1])][-1] > min_collisions_tsp:
            collisions_better_tsp.append(collisions[data_lrtdp[row_id][1]][str(data_lrtdp[row_id][-1])][-1])

    print ("---- DONE READING CSV FILE ----")
    # print("execution time", execution_time)
    for j in range (2, max_levels):
        # print(len(execution_time["steps_avg"][str(j)]), "times for level", j, "in steps_avg")
        # print (len(times))
        if len(execution_time["steps_avg"][str(j)]) != len(times):
            print("ERROR: number of times does not match the number of steps for level", j, "in steps_avg")
    for j in range (0, len(execution_time["steps_lrtdp"]["2"])):
        # time_local = execution_time["steps_lrtdp"]["2"][j]
        for i in range(3, max_levels):
            if (float(execution_time["steps_lrtdp"][str(i)][j]) - float(execution_time["steps_lrtdp"]["2"][j])) > 0.01:
                print("WARNING: execution time for lrtdp is not the same for all levels for time:", times[j], execution_time["steps_lrtdp"]["2"][j], execution_time["steps_lrtdp"][str(i)][j])


    for i in range(2, max_levels):

        p = mannwhitneyu( execution_time["steps_lrtdp"][str(i)], execution_time["steps_avg"][str(i)], alternative='less')
        print("p-value avg tsp level", i, p[1])
        p = mannwhitneyu( execution_time["steps_lrtdp"][str(i)], execution_time["steps_min"][str(i)], alternative='less')
        print("p-value min tsp level", i, p[1])
        p = mannwhitneyu( execution_time["steps_lrtdp"][str(i)], execution_time["steps_max"][str(i)], alternative='less')
        print("p-value max tsp level", i, p[1])
        p = mannwhitneyu( execution_time["steps_lrtdp"][str(i)], execution_time["steps_curr"][str(i)], alternative='less')
        print("p-value current tsp level", i, p[1])
        p = mannwhitneyu( collisions["steps_lrtdp"][str(i)], collisions["steps_avg"][str(i)], alternative='less')
        print("p-value collisions avg tsp level", i, p[1])
        p = mannwhitneyu( collisions["steps_lrtdp"][str(i)], collisions["steps_min"][str(i)], alternative='less')
        print("p-value collisions min tsp level", i, p[1])
        p = mannwhitneyu( collisions["steps_lrtdp"][str(i)], collisions["steps_max"][str(i)], alternative='less')
        print("p-value collisions max tsp level", i, p[1])
        p = mannwhitneyu( collisions["steps_lrtdp"][str(i)], collisions["steps_curr"][str(i)], alternative='less')
        print("p-value collisions current tsp level", i, p[1])
        print("Average execution time for tsp avg level", i, np.mean(execution_time["steps_avg"][str(i)]))
        print("Average execution time for tsp min level", i, np.mean(execution_time["steps_min"][str(i)]))
        print("Average execution time for tsp max level", i, np.mean(execution_time["steps_max"][str(i)]))
        print("Average execution time for tsp curr level", i, np.mean(execution_time["steps_curr"][str(i)]))
        print("Average execution time for lrtdp level", i, np.mean(execution_time["steps_lrtdp"][str(i)]))
        print("maximum execution time for lrtdp level", i, np.max(execution_time["steps_lrtdp"][str(i)]))
        print("minimum execution time for lrtdp level", i, np.min(execution_time["steps_lrtdp"][str(i)]))
        print("Average planning time for tsp avg level", i, np.mean(cpu_time["steps_avg"][str(i)]))
        print("Average planning time for tsp min level", i, np.mean(cpu_time["steps_min"][str(i)]))
        print("Average planning time for tsp max level", i, np.mean(cpu_time["steps_max"][str(i)]))
        print("Average planning time for tsp curr level", i, np.mean(cpu_time["steps_curr"][str(i)]))
        print("Average planning time for lrtdp level", i, np.mean(cpu_time["steps_lrtdp"][str(i)]))
        print("Average number of collisions for tsp avg level", i, np.mean(collisions["steps_avg"][str(i)]))
        print("Average number of collisions for tsp min level", i, np.mean(collisions["steps_min"][str(i)]))
        print("Average number of collisions for tsp max level", i, np.mean(collisions["steps_max"][str(i)]))
        print("Average number of collisions for tsp curr level", i, np.mean(collisions["steps_curr"][str(i)]))
        print("Average number of collisions for lrtdp level", i, np.mean(collisions["steps_lrtdp"][str(i)]))

    print("---- DONE CALCULATING STATISTICS ----")
    print("Number of times lrtdp was faster than tsp:", lrtdp_count)
    print("Number of times tsp was faster than lrtdp:", time_best_tsp)
    print("Number of times lrtdp and tsp had the same execution time:", time_equal)
    print("number of times collisions better tsp ", len(collisions_better_tsp))
    print("number of times collisions better lrtdp ", len(collisions_better_lrtdp))
    # print("Minimum time delta for lrtdp:", np.min(time_delta_min_lrtdp))
    # print("Maximum time delta for lrtdp:", np.max(time_delta_max_lrtdp))
    # print("Minimum time delta for tsp:", time_delta_min_tsp)
    # print("Maximum time delta for tsp:", time_delta_max_tsp)   
    # print("Average time delta for lrtdp:", np.mean(time_delta_better_lrtdp))
    # print("Average time delta for tsp:", np.mean(time_delta_better_tsp))

    for i in range(2, max_levels):
        fig = plt.figure(figsize =(10, 7))
        ax = fig.add_subplot(111)
        ax.set_title(csv_file.split("/")[-1].split(".")[0] + " planning time per step (level " + str(i) + ")")
        # set y-axis scale to be multiple of 2
        max_y = np.max([np.max(planning_time_lrtdp_per_step_per_level[str(i)][str(x)]) for x in planning_time_lrtdp_per_step_per_level[str(i)].keys()])
        plt.yticks(np.arange(0, max_y + 2, step=2))
        max_steps = len(planning_time_lrtdp_per_step_per_level[str(i)].keys())
        data = [planning_time_lrtdp_per_step_per_level[str(i)][str(x)] for x in range(0, max_steps)]
        ax.boxplot(data, tick_labels = [str(x) for x in range(1, max_steps+1)])
        plt.ylabel("Planning time per step (s)")
        plt.xlabel("Step")
        plt.grid()
        plt.show()

    # plot the execution time for the lrtdp and tsp algorithms for each level
    for i in range(2, max_levels):
        fig = plt.figure(figsize =(10, 7))
        ax = fig.add_subplot(111)
        ax.set_title(csv_file.split("/")[-1].split(".")[0] + " execution time (level " + str(i) + ") (first planning + max(planning, execution))")
        data = [execution_time["steps_avg"][str(i)], execution_time["steps_min"][str(i)], execution_time["steps_max"][str(i)], execution_time["steps_curr"][str(i)], execution_time["steps_lrtdp"][str(i)]]
        labels = ["tsp_avg", "tsp_min", "tsp_max", "tsp_curr", "lrtdp"]
        ax.boxplot(data, tick_labels = labels)
        plt.ylabel("Execution time (s)")
        plt.xlabel("Algorithms")
        plt.grid()
        plt.show()


    # plot the planning time for the execution of the lrtdp and tsp algorithms for each level
    for i in range(2, max_levels):
        fig = plt.figure(figsize =(10, 7))
        ax = fig.add_subplot(111)
        ax.set_title(csv_file.split("/")[-1].split(".")[0] + " planning time (level " + str(i) + ")")
        data = [cpu_time["steps_avg"][str(i)], cpu_time["steps_min"][str(i)], cpu_time["steps_max"][str(i)], cpu_time["steps_curr"][str(i)], cpu_time["steps_lrtdp"][str(i)]]
        labels = ["tsp_avg", "tsp_min", "tsp_max", "tsp_curr", "lrtdp"]
        ax.boxplot(data, tick_labels = labels)
        plt.ylabel("Planning time (s)")
        plt.xlabel("Algorithms")
        plt.grid()
        plt.show()

    # plot the number of collisions for the execution of the lrtdp and tsp algorithms for each level
    for i in range(2, max_levels):
        fig = plt.figure(figsize =(10, 7))
        ax = fig.add_subplot(111)
        ax.set_title(csv_file.split("/")[-1].split(".")[0] + " number of collisions (level " + str(i) + ")")
        data = [collisions["steps_avg"][str(i)], collisions["steps_min"][str(i)], collisions["steps_max"][str(i)], collisions["steps_curr"][str(i)], collisions["steps_lrtdp"][str(i)]]
        labels = ["tsp_avg", "tsp_min", "tsp_max", "tsp_curr", "lrtdp"]
        ax.boxplot(data, tick_labels = labels)
        plt.ylabel("Number of collisions")
        plt.xlabel("Algorithms")
        plt.grid()
        plt.show()



def plot_cpu_times_per_number_of_vertices(csv_file):
    cpu_times_per_level = {}
    for j in range(19, 23):
        cpu_times_per_level[str(j)] = []
        with open(csv_file.split(".")[0] + "_" + str(j) + "_lrtdp30.csv", 'r') as file:
            reader = csv.reader(file)
            next(reader)
            data = [row for row in reader]
        for row in data:
            times_lrtdp = eval(row[-2])

            if len(times_lrtdp) != 0:
                for i in range(0, len(times_lrtdp)):
                    if str(j) not in cpu_times_per_level:
                        cpu_times_per_level[str(j)] = []
                    cpu_times_per_level[str(j)].append(float(times_lrtdp[i]))
    print(cpu_times_per_level)

    ## PLOT

    fig = plt.figure(figsize =(10, 7))
    ax = fig.add_subplot(111)
    ax.set_title("Planning time (average)")
    data = [cpu_times_per_level["19"], cpu_times_per_level["20"], cpu_times_per_level["21"], cpu_times_per_level["22"]]
    labels = ["19", "20", "21", "22"]
    ax.boxplot(data, tick_labels = labels)
    plt.ylabel("Planning time (s)")
    plt.xlabel("Algorithms")
    plt.grid()
    plt.show()



    print("---- DONE PLOTTING ----")

if __name__ == '__main__':
    # get_statistics("steps_iit_time_iter.csv")
    # get_statistics("steps_small_occupancy_map_atc_corridor_mixed.csv")
    # get_statistics("steps_medium_occupancy_map_atc_corridor_mixed.csv")
    if sys.argv[1] == "statistics":
        get_statistics(sys.argv[2], int(sys.argv[3]))
    elif sys.argv[1] == "times":
        plot_cpu_times_per_number_of_vertices(sys.argv[2])