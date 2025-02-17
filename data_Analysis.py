import csv
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


def analyze_data(data_file):
    with open (data_file, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            



if __name__ == "__main__":
    data_file = "dataset/iit/iit.csv"
    analyze_data(data_file)