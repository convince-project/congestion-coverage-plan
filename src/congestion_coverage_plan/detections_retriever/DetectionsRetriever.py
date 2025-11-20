# topic subrscriber for retrieving detections from a ROS topic
# it keeps the latest detection messages in a member variable

import rclpy
from threading import Lock
import threading
from static_devices_msgs.msg import DetectionsArray, SingleDetection
from congestion_coverage_plan.utils.dataset_utils import read_human_traj_data_from_file

class Detection:
    def __init__(self, person_id, positionx, positiony, timestamp, vx, vy):
        self.person_id = person_id
        self.positionx = positionx
        self.positiony = positiony
        self.timestamp = timestamp
        self.vx = vx
        self.vy = vy

    


class DetectionsRetriever:
    def __init__(self, topic_name = "static_tracks", queue_size=10):
        self._lock = Lock()
        self._detections = {}
        self._current_occupancies = {}
        self._queue_size = queue_size
        self._subscriber = rclpy.Subscriber(topic_name, DetectionsArray, self._callback)


    # keep last 5 detections for each person, if it is too old, remove the person
    # TODO: check the correctness of this function
    def _callback(self, msg):
        detections_local = {}
        current_occupancies_local = []
        for detection in msg.detections:
            detection: SingleDetection
            detection_obj = Detection(
                person_id=detection.id,
                positionx=detection.x,
                positiony=detection.y,
                timestamp=detection.ts,
                vx=detection.vx,
                vy=detection.vy
            )
            detections_local[detection.id] = sorted([detection_obj] + self._detections.get(detection.id, [])[0:self._queue_size-1] if self._detections and detection.id in self._detections else [detection_obj], key=lambda x: x.timestamp, reverse=True)
            
            current_occupancies_local.append(Detection(
                person_id=detection.id,
                positionx=detection.x,
                positiony=detection.y,
                timestamp=detection.ts,
                vx=detection.vx,
                vy=detection.vy
            ))

        with self._lock:
            self._detections = detections_local
            self._current_occupancies = current_occupancies_local

    # retrieve the latest detections
    # return a dictionary of person_id to list of Detection objects
    def get_detections(self):
        with self._lock:
            return self._detections


    # retrieve the latest current occupancies
    # return a list of Detection objects
    def get_current_occupancies(self):
        with self._lock:
            return self._current_occupancies


    # start on a new thread
    def start(self):
        thread = threading.Thread(target=self.start_ros)
        thread.start()


    def start_ros(self):

        rclpy.init_node('detections_retriever_node', anonymous=True)
        rclpy.loginfo("DetectionsRetriever node started, listening to topic: %s", self._subscriber.name)
        rclpy.spin()


class FakeDetectionsRetriever:
    def __init__(self, dataset, queue_size=5):
        self._lock = Lock()
        self._detections = {}
        self._current_occupancies = {}
        self._queue_size = queue_size
        self._dataset = dataset
        self.human_traj_data = None
        self.load_dataset()

    def load_dataset(self):
        self.human_traj_data = read_human_traj_data_from_file(self._dataset)

    # def get_detections(self):
    #     with self._lock:
    #         return self._detections


    def get_detections(self, timestamp):
        human_traj_data_by_time = self.human_traj_data.loc[abs(self.human_traj_data['time'] - timestamp) < 1 ]
        people_ids = list(human_traj_data_by_time.person_id.unique())
        tracks = {}
        self.people_trajectories = {}

        for id in people_ids:
            human_traj_data_by_person_id = self.human_traj_data.loc[self.human_traj_data['person_id'] == id]
            human_traj_array = human_traj_data_by_person_id[["time", "x", "y", "vx", "vy"]].to_numpy()
            print("human_traj_array:", human_traj_array)
            track_before_now = human_traj_array[human_traj_array[:, 0] <= timestamp]
            track_filtered = track_before_now[-(self._queue_size + 1):]
            if len(track_filtered) >= self._queue_size:
                tracks[id] = track_filtered

        self.people_trajectories = tracks
        for track in tracks:
            detections_list = []
            for point in tracks[track]:
                detection_obj = Detection(
                    person_id=0,
                    positionx=point[1],
                    positiony=point[2],
                    timestamp=point[0],
                    vx=point[3],
                    vy=point[4]
                )
                detections_list.append(detection_obj)
            self._detections[track] = sorted(detections_list, key=lambda x: x.timestamp, reverse=True)
        return self._detections



    def get_current_occupancies(self, timestamp):
        human_traj_data_by_time = self.human_traj_data.loc[abs(self.human_traj_data['time'] - timestamp) < 1 ]
        people_ids = list(human_traj_data_by_time.person_id.unique())
        current_occupancies_local = []
        for id in people_ids:
            human_traj_data_by_person_id = self.human_traj_data.loc[self.human_traj_data['person_id'] == id]
            human_traj_array = human_traj_data_by_person_id[["time", "x", "y", "vx", "vy"]].to_numpy()
            track_before_now = human_traj_array[human_traj_array[:, 0] <= timestamp]
            if len(track_before_now) > 0:
                last_position = track_before_now[-1]
                current_occupancies_local.append(Detection(
                    person_id=id,
                    positionx=last_position[1],
                    positiony=last_position[2],
                    timestamp=timestamp,
                    vx=last_position[3],
                    vy=last_position[4]
                ))
        return current_occupancies_local
        


    # start on a new thread
    def start(self):
        return True
        # thread = threading.Thread(target=self.start_ros)
        # thread.start()

