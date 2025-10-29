import csv

if __name__ == "__main__":
    with open("dataset/madama/detections_november_tracked.csv", "r") as f:
        reader = csv.reader(f)
        header = next(reader)  # Skip the header row
        rows = list(reader)

    with open("dataset/madama/detections_november_tracked_fixed.csv", "w", newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)  # Write the header row
        for row in rows:
            row[2] = float(row[2]) - 25.6
            row[3] = float(row[3]) - 25.6
            writer.writerow(row)  # Write the modified row
