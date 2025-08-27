import csv
import sys
if __name__ == '__main__':

    with open(sys.argv[1], 'r') as file:
        reader = csv.reader(file)
        # header = next(reader)
        # Find the index of the "time" column
        time_index = 0
        # Sort the rows by the "time" column
        sorted_rows = sorted(reader, key=lambda row: float(row[time_index]))
    with open(sys.argv[2], 'w', newline='') as file:
        writer = csv.writer(file)
        # writer.writerow(header)
        #
        for row_id in range(0, len(sorted_rows)):
            if row_id != 0 and row_id != len(sorted_rows)-1:
                if sorted_rows[row_id][1] == sorted_rows[row_id-1][1] or sorted_rows[row_id][1] == sorted_rows[row_id+1][1]:
                    
                    sorted_rows[row_id][2] = float(sorted_rows[row_id][2])-36.0
                    sorted_rows[row_id][3] = float(sorted_rows[row_id][3])-36.0
                    writer.writerow(sorted_rows[row_id])

        