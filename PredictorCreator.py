from congestion_coverage_plan.cliff_predictor.CliffPredictor import CliffPredictor
from congestion_coverage_plan.utils import dataset_utils

def create_atc_cliff_predictor():
    map_file = "data/maps/atc.jpg"
    mod_file = "data/MoDs/atc/atc-20121024-cliff.csv"
    ground_truth_data_file = "data/datasets/atc/atc_reduced.csv"
    observed_tracklet_length = 4
    start_length = 0
    planning_horizon = 50
    beta = 1
    sample_radius = 1
    delta_t = 1
    method = dataset_utils.Method.MoD
    # method = dataset_utils.Method.CVM
    dataset = dataset_utils.Dataset.ATC
    fig_size = [-60, 80, -40, 20]
    predictor = CliffPredictor(dataset, map_file, mod_file, observed_tracklet_length, start_length, planning_horizon, beta, sample_radius, delta_t, method, fig_size, ground_truth_data_file)
    return predictor

def create_iit_cliff_predictor():
    map_file = "data/maps/iit.png"
    mod_file = "data/MoDs/iit/iit_cliff.csv"
    ground_truth_data_file = "data/datasets/iit/iit.csv"
    observed_tracklet_length = 4
    start_length = 0
    planning_horizon = 50
    beta = 1
    sample_radius = 1
    delta_t = 1
    method = dataset_utils.Method.MoD
    # method = dataset_utils.Method.CVM
    dataset = dataset_utils.Dataset.IIT
    fig_size = [-12.83, 12.83, -12.825, 12.825]
    predictor = CliffPredictor(dataset, map_file, mod_file, observed_tracklet_length, start_length, planning_horizon, beta, sample_radius, delta_t, method, fig_size, ground_truth_data_file)
    return predictor


def create_madama_cliff_predictor():
    map_file = "data/maps/madama.png"
    mod_file = "data/MoDs/madama/map_november_reduced_v3_fixed_low_decimals.csv"
    ground_truth_data_file = "data/datasets/madama/madama_reduced_decimals.csv"
    observed_tracklet_length = 4
    start_length = 0
    planning_horizon = 50
    beta = 1
    sample_radius = 1
    delta_t = 1
    method = dataset_utils.Method.MoD
    # method = dataset_utils.Method.CVM
    dataset = dataset_utils.Dataset.MADAMA
    fig_size = [0,72, 72, 0 ]
    predictor = CliffPredictor(dataset, map_file, mod_file, observed_tracklet_length, start_length, planning_horizon, beta, sample_radius, delta_t, method, fig_size, ground_truth_data_file)
    return predictor


if __name__ == "__main__":
    madama_predictor = create_madama_cliff_predictor()
    madama_predictor.display_cliff_map_and_save()