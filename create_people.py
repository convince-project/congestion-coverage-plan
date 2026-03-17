from congestion_coverage_plan.cliff_predictor.CliffPredictor import CliffPredictor
from congestion_coverage_plan.cliff_predictor.PredictorCreator import create_generic_cliff_predictor, create_madama3_cliff_predictor

import sys
import matplotlib.pyplot as plt
import random





















def predict_next_position(predictor, track, planning_horizon, final_track):
    predictions = predictor.predict_positions({"person_1": track}, planning_horizon=planning_horizon)
    if predictions is None or len(predictions) == 0 or len(predictions[0]) == 0:
        print("No predictions available, stopping.")
        return False, track

    person_predictions = predictions[0]
    selected_trajectory = person_predictions[random.randrange(len(person_predictions))]

    last_timestamp = float(track[-1]["timestamp"])
    next_pose = None
    for pose in selected_trajectory:
        if float(pose[0]) > last_timestamp:
            next_pose = pose
            break

    if next_pose is None:
        print("No future pose found in prediction, stopping.")
        return False, track
    next_position = {
        "timestamp": float(next_pose[0]),
        "id": track[-1]["id"],
        "x": float(next_pose[1]),
        "y": float(next_pose[2]),
        "velocity": float(next_pose[3]),
        "motion_angle": float(next_pose[4]),
    }

    final_track["person_1"].append(next_position)
    updated_track = track[1:] + [next_position]
    return True, updated_track





if __name__ == "__main__":
    
    args = sys.argv[1:]
    map_name = ""
    append_mode = False
    file_backround = "data/maps/madama3.jpg"
    fig_size = [-21.2,36.4, -53.4, 9.2 ]
    show_map = False
    if "--map" in args:
        map_index = args.index("--map")
        if map_index + 1 < len(args):
            map_name = args[map_index + 1]
        else:
            print("Error: --map option requires a value.")
            sys.exit(1)

    if "--append-mode" in args:
        append_mode = True

    if "--show-map" in args:
        show_map = True

    # Create predictor
    predictor = create_madama3_cliff_predictor()
    # create a fake track composed of {person_id: [{time: t, x: x, y: y, velocity: v, motion_angle: a}, ...]}
    track = {
        "person_1": [
            {"timestamp": 0, "id": 0, "x": -1.5, "y": -30.5, "velocity": 1, "motion_angle": 0},
            {"timestamp": 1, "id": 0, "x": -1, "y": -30.5, "velocity": 1, "motion_angle": 0},
            {"timestamp": 2, "id": 0, "x": -0.5, "y": -30.5, "velocity": 1, "motion_angle": 0},
            {"timestamp": 3, "id": 0, "x": 0, "y": -30.5, "velocity": 1, "motion_angle": 0},
            {"timestamp": 4, "id": 0, "x": 0.5, "y": -30.5, "velocity": 1, "motion_angle": 0},
        ]
    }
    final_track = {"person_1": list(track["person_1"])}
    return_val = True
    # Predict final  
    while return_val and not (final_track["person_1"][-1]["x"] < 0.7 and final_track["person_1"][-1]["x"] > 0.5 and final_track["person_1"][-1]["y"] < -30.5 and final_track["person_1"][-1]["y"] > -30.7):
        return_val, track["person_1"] = predict_next_position(
            predictor,
            track["person_1"],
            planning_horizon=5,
            final_track=final_track,
        )

    # save the final track to a file
    import csv
    if append_mode:
        with open("final_track.csv", "a", newline="") as csvfile:
            fieldnames = ["timestamp", "id", "x", "y", "velocity", "motion_angle"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            for pose in final_track["person_1"]:
                writer.writerow(pose)
    else:
        with open("final_track.csv", "w", newline="") as csvfile:
            fieldnames = ["timestamp", "id", "x", "y", "velocity", "motion_angle"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for pose in final_track["person_1"]:
                writer.writerow(pose)
    predictor.display_cliff_map()

    if show_map:
        fig, ax = plt.subplots(facecolor='grey')
        img = plt.imread(file_backround)
        plt.imshow(img, cmap='gray', vmin=0, vmax=255, extent=fig_size)
        plt.scatter([pose["x"] for pose in final_track["person_1"]], [pose["y"] for pose in final_track["person_1"]], marker='D', alpha=1, color="b", s=100, label="Predicted position")
        plt.show()
    print(final_track)