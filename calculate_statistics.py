import csv

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
    for row_id in range(0, len(data), num_rows):
        min_time = 99999999
        for i in range(0,num_rows -1 ):
            if get_time(data[row_id+i][2]) < min_time:
                min_time = get_time(data[row_id+i][2])
        
        time_lrtdp = get_time(data[row_id+num_rows -1][2])
        

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

    print("lrtdp_best", lrtdp_count, "tsp_best", time_best_tsp, "equal", time_equal, "row_count", row_count)
    print("lrtdp_time_delta", np.mean(time_delta_better_lrtdp), "min_lrtdp", time_delta_min_lrtdp, "max_lrtdp", time_delta_max_lrtdp)
    print("tsp_time_delta", np.mean(time_delta_better_tsp), "min_tsp", time_delta_min_tsp, "max_tsp", time_delta_max_tsp)

if __name__ == '__main__':
    get_statistics(sys.argv[1])