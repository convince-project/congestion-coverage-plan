import matplotlib.pyplot as plt
from tqdm import *
import csv

from trajectory_predictor import TrajectoryPredictor
import plot_figures
import utils
from datetime import datetime
import numpy as np

class CliffPredictor:

    def __init__(self, dataset, map_file, mod_file, observed_tracklet_length, start_length, planning_horizon, beta, sample_radius, delta_t, method, fig_size):
        self.map_file = map_file
        self.mod_file = mod_file
        # self.ground_truth_data_file = ground_truth_data_file
        # self.result_file = result_file
        self.observed_tracklet_length = observed_tracklet_length
        self.start_length = start_length
        self.planning_horizon = planning_horizon
        self.beta = beta
        self.sample_radius = sample_radius
        self.delta_t = delta_t
        self.method = method
        self.dataset = dataset
        self.fig_size = fig_size
        self.cliff_map_data = utils.read_cliff_map_data(mod_file)
        # print(fig_size)
        # self.human_traj_data = utils.read_iit_human_traj_data(self.ground_truth_data_file)
    def get_all_person_id(self, data):
        person_id_list = list(data.person_id.unique())
        return person_id_list


    def get_human_traj_data_by_person_id(self, human_traj_origin_data, person_id):
        human_traj_data_by_person_id = human_traj_origin_data.loc[human_traj_origin_data['person_id'] == person_id]
        human_traj_array = human_traj_data_by_person_id[["time", "x", "y", "velocity", "motion_angle"]].to_numpy()

        return human_traj_array

    def display_cliff_map(self, all_predicted_trajectory_list, planning_horizon = 50):
        plt.subplot(111, facecolor='grey')
        img = plt.imread(self.map_file)
        plt.imshow(img, cmap='gray', vmin=0, vmax=255, extent=self.fig_size)
        plot_figures.plot_cliff_map(self.cliff_map_data)
        plot_figures.plot_all_predicted_trajs(all_predicted_trajectory_list, self.observed_tracklet_length)
        for predicted_people in all_predicted_trajectory_list:

            # plot_figures.plot_observed_tracklet(predicted_people, self.observed_tracklet_length)
            # print("all_predicted_trajectory_list", predicted_people)
            # print(len(predicted_people))
            for predicted_traj in predicted_people:
                # print("predicted_traj", len(predicted_traj))
                if len(predicted_traj) < planning_horizon:
                    continue
                final_pose = predicted_traj[planning_horizon - 1]
                # initial_pose = predicted_traj[0]
                # print("initial_pose", initial_pose)
                # plt.scatter(initial_pose[1], initial_pose[2], marker='D', alpha=1, color="r", s=100, label="Initial position")
                plt.scatter(final_pose[1], final_pose[2], marker='D', alpha=1, color="b", s=100, label="Predicted position")

        plt.show()

    # here person_positions is a list of person positions
    # it is a dictionary composed of: {person_id: [{time: t, x: x, y: y, velocity: v, motion_angle: a}, ...]}
    def predict_positions(self, person_positions, planning_horizon = 50):
        if planning_horizon:
            self.planning_horizon = planning_horizon
        all_predictions = []
        # human_traj_data = utils.read_iit_human_traj_data("dataset/iit/iit.csv)
        for person_id in person_positions.keys():
            traj = person_positions[person_id]
            # print("person_positions", person_positions)
            # sort the trajectory by time
            traj = sorted(traj, key=lambda x: float(x[0]))
            # print("traj", traj)
            human_traj_data_by_person_id = np.array([[pose[0], pose[1], pose[2], pose[3], pose[4]] for pose in traj])
            # human_traj_data_by_person_id = self.get_human_traj_data_by_person_id(human_traj_data, person_id)

            
            # print("human_traj_data_by_person_id", human_traj_data_by_person_id)
            trajectory_predictor = TrajectoryPredictor(
                cliff_map_origin_data=self.cliff_map_data,
                human_traj_origin_data=human_traj_data_by_person_id,
                person_id=person_id,
                start_length=self.start_length,
                observed_tracklet_length=self.observed_tracklet_length,
                max_planning_horizon=self.planning_horizon,
                beta=self.beta,
                sample_radius=self.sample_radius,
                delta_t=self.delta_t,
                result_file="out.txt"
            )
            # print("trajectory_predictor.check_human_traj_data()", trajectory_predictor.check_human_traj_data())
            if not trajectory_predictor.check_human_traj_data():
                print("trajectory_predictor.check_human_traj_data() failed")
                continue

            if self.method == utils.Method.MoD:
                all_predicted_trajectory_list = trajectory_predictor.predict_one_human_traj_mod()
            elif self.method == utils.Method.CVM:
                all_predicted_trajectory_list = trajectory_predictor.predict_one_human_traj_cvm()
            all_predictions.append(all_predicted_trajectory_list)
            # self.display_cliff_map(all_predicted_trajectory_list)

        return all_predictions


def main_iit():
    map_file = "maps/iit.png"
    mod_file = "MoDs/iit/iit_cliff.csv"
    # ground_truth_data_file = "dataset/iit/iit.csv"
    # result_file = "iit_results.csv"
    observed_tracklet_length = 5
    start_length = 0
    planning_horizon = 50
    beta = 1
    sample_radius = 0.5
    delta_t = 0.4
    method = utils.Method.MoD
    # method = utils.Method.CVM
    dataset = utils.Dataset.IIT
    fig_size = [-12.83, 12.83, -12.825, 12.825]
    predictor = CliffPredictor(dataset, map_file, mod_file, observed_tracklet_length, start_length, planning_horizon, beta, sample_radius, delta_t, method, fig_size)

    person_detected = {"199":[{"time": 1717229086.0, "x": 6.884506949983775, "y": -9.296345384207825, "velocity": 0.021053802771527092, "motion_angle": 0.09452520269564246},
                               {"time": 1717229090.0, "x": 5.876670840167281, "y": -10.933077918614604, "velocity": -0.0013049241170085917, "motion_angle": 0.05971127789006422},
                               {"time": 1717229091.0, "x": 5.862268079727243, "y": -10.831767252735226, "velocity": -0.011048673899152798, "motion_angle": 0.008346491410102649},
                               {"time": 1717229092.0, "x": 5.803650109950623, "y": -10.70635623211404, "velocity": -0.011214256009512388, "motion_angle": 0.08736293855365555},
                               {"time": 1717229093.0, "x": 5.798884118078008, "y": -10.549682048879458, "velocity": 0.0397422776123341, "motion_angle": 0.051822531223469546},
                               {"time": 1717229094.0, "x": 5.803588380590247, "y": -10.434168184237723, "velocity": -0.09044022578547366, "motion_angle": 0.057646655954435744},
                               {"time": 1717229095.0, "x": 5.647815956123152, "y": -10.333253937054728, "velocity": -0.013874304966478235, "motion_angle": 0.03268024103782352},
                               {"time": 1717229096.0, "x": 5.62196054108788, "y": -10.277020815905736, "velocity": 0.10578314841184107, "motion_angle": -0.03319805495547475},
                               {"time": 1717229097.0, "x": 5.75307760138967, "y": -10.312087449429166, "velocity": 0.05938933087318551, "motion_angle": -0.02283293856143705}],
                       "206":[{"time": 1717229122.0, "x": 8.72901968371897, "y": -9.456386819566086, "velocity": -0.20325664584181405, "motion_angle": 0.045395211512255194},
                               {"time": 1717229123.0, "x": 8.313963191399088, "y": -9.364847873339052, "velocity": -0.280376577421593, "motion_angle": 0.013725297037674741},
                               {"time": 1717229124.0, "x": 7.762598863268496, "y": -9.337655453490681, "velocity": -0.31664566485331846, "motion_angle": 0.031777455943554855},
                               {"time": 1717229126.0, "x": 7.138609685171262, "y": -9.27762227862824, "velocity": -0.653625084622614, "motion_angle": 0.22872150347145256},
                               {"time": 1717229127.0, "x": 5.9658971909867455, "y": -8.837267649500436, "velocity": -0.2898968723594386, "motion_angle": 0.19271345702177575},
                               {"time": 1717229128.0, "x": 5.417798045836835, "y": -8.4588395786524, "velocity": -0.20405370110863608, "motion_angle": 0.22356973641983893},
                               {"time": 1717229129.0, "x": 5.05185846882955, "y": -8.005165907139455, "velocity": -0.14672729282062313, "motion_angle": 0.29428074592897363},
                               {"time": 1717229130.0, "x": 4.765996312342052, "y": -7.444054925234129, "velocity": -0.19503691919027114, "motion_angle": 0.3038401808544637},
                               {"time": 1717229131.0, "x": 4.371768619229263, "y": -6.887462239506613, "velocity": -0.25953332589639483, "motion_angle": 0.20062631892771657},
                               {"time": 1717229132.0, "x": 3.863407528318328, "y": -6.497490370459041, "velocity": -0.30184035946675775, "motion_angle": 0.1720920706905004},
                               {"time": 1717229133.0, "x": 3.296139335164492, "y": -6.175712743633693, "velocity": -0.22438842217108737, "motion_angle": 0.16700026062205828},
                               {"time": 1717229134.0, "x": 2.8759396802508923, "y": -5.842793535918824, "velocity": -0.14068596837526215, "motion_angle": 0.15321203537816666}],
                       "210":[{"time": 1717229224.0, "x": 8.709070840710801, "y": -9.866005415861775, "velocity": -0.22512908345905913, "motion_angle": 0.05874590786995881},
                                 {"time": 1717229225.0, "x": 8.24157295394755, "y": -9.738923813213026, "velocity": -0.2946991020812746, "motion_angle": 0.10276074457264055},
                                 {"time": 1717229226.0, "x": 7.665151913450706, "y": -9.521599702292026, "velocity": -0.3145305618842779, "motion_angle": 0.13700470055841643},
                                 {"time": 1717229229.0, "x": 6.140151303467802, "y": -8.5355657189282, "velocity": -0.3738373971299449, "motion_angle": 0.3222749427454528},
                                 {"time": 1717229230.0, "x": 5.4521914243014145, "y": -7.894928630082974, "velocity": -0.23037800717124193, "motion_angle": 0.28628547245116565},
                                 {"time": 1717229231.0, "x": 5.01147133098408, "y": -7.332665074906068, "velocity": -0.2417980594501176, "motion_angle": 0.3003156400036128},
                                 {"time": 1717229232.0, "x": 4.552287921448818, "y": -6.770477594273297, "velocity": -0.20715244437335834, "motion_angle": 0.29015868868984523},
                                 {"time": 1717229233.0, "x": 4.154740862886403, "y": -6.218715348277853, "velocity": -0.17782289706582213, "motion_angle": 0.27164485910657926},
                                 {"time": 1717229234.0, "x": 3.832173288765578, "y": -5.694527576346078, "velocity": -0.11226921692644432, "motion_angle": 0.21182746634453645},
                                 {"time": 1717229235.0, "x": 3.614734727981833, "y": -5.287743402142496, "velocity": -0.0671618714488978, "motion_angle": 0.16388979566853182},
                                 {"time": 1717229236.0, "x": 3.4806910391580006, "y": -4.99480612039438, "velocity": -0.06734077300074996, "motion_angle": 0.08682820253644745}]}
    
    prediction = predictor.predict_positions(person_detected, 50)
    print("prediction", len(prediction[2]))
    predictor.display_cliff_map(prediction, 20)

    # prediction = predictor.predict_positions(person_detected, 20)
    # print("prediction", prediction)
    # predictor.display_cliff_map(prediction)

    # prediction = predictor.predict_positions(person_detected, 10)
    # print("prediction", prediction)
    # predictor.display_cliff_map(prediction)


if __name__ == "__main__":
    # main_atc()
    main_iit()