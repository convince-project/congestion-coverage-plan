import csv
import numpy as np

def count_number_of_detections(result_file):
    with open(result_file, 'r') as f:
        reader = csv.reader(f)
        data = list(reader)
    # count the number of detections in the second column for each number
    # of observed tracklets
    # print(data)
    number_of_detections = {}
    for row in data:
        if row[1] not in number_of_detections:
            number_of_detections[row[1]] = 0
        number_of_detections[row[1]] += 1
    
    for detected in number_of_detections:
        if number_of_detections[detected] > 25:
            print(detected, number_of_detections[detected])
    

def count_time(result_file, filter_limit = 7):
    # count the number of occurrencies in the first position of the csv file
    # if it is higher than 8 print it
    with open(result_file, 'r') as f:
        reader = csv.reader(f)
        data = list(reader)
    number_of_detections = {}
    for row in data:
        if row[0] not in number_of_detections:
            number_of_detections[row[0]] = 0
        number_of_detections[row[0]] += 1
    detected_times = []
    for detected in number_of_detections:
        if number_of_detections[detected] > filter_limit:
            detected_times.append(detected)
    return detected_times

if __name__ == "__main__":
    # times = count_time("dataset/iit/85_june_occupancy_over_time-09-28-2024_06:59:02_millisecond_tracked.csv", 7)
    times = count_time("dataset/atc/atc_reduced.csv", 17)
    # write the times to csv
    with open("times_higher_17_atc_reduced.csv", 'w') as f:
        writer = csv.writer(f)
        writer.writerow(times)
