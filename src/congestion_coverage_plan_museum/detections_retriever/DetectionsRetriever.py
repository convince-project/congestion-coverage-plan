# topic subrscriber for retrieving detections from a ROS topic
# it keeps the latest detection messages in a member variable

from threading import Lock
from static_devices_msgs.msg import DetectionsArray, SingleDetection
from matplotlib import pyplot as plt
from congestion_coverage_plan_museum.utils.dataset_utils import read_human_traj_data_from_file

class Detection:
    def __init__(self, person_id, positionx, positiony, timestamp, vx, vy):
        self.person_id = person_id
        self.positionx = positionx
        self.positiony = positiony
        self.timestamp = timestamp
        self.vx = vx
        self.vy = vy


class DetectionsRetriever:
    def __init__(self, node=None, topic_name="static_tracks", queue_size=10):
        """
        If `node` (rclpy.node.Node) is provided, subscription is created immediately.
        Otherwise call start(node=...) or start_background_node() to run standalone.
        """
        self._node = node
        self._topic_name = topic_name
        self._lock = Lock()
        self._detections = {}
        self._current_occupancies = {}
        self._queue_size = queue_size
        self._subscriber = None

        self.start_with_node(node)


        


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
            existing = self._detections.get(detection.id, [])
            # keep newest first, limit to queue_size
            combined = [detection_obj] + existing[:5] if existing else [detection_obj]
            detections_local[detection.id] = sorted(combined, key=lambda x: x.timestamp, reverse=True)
            
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

    def get_detections(self):
        with self._lock:
            return self._detections

    def get_current_occupancies(self):
        with self._lock:
            return self._current_occupancies

    def start_with_node(self, node):
        """Attach to an existing node (create subscription if needed)."""
        self._node = node
        if self._subscriber is None:
            self._subscriber = self._node.create_subscription(DetectionsArray, self._topic_name, self._callback, self._queue_size)
        return True

    # def start_background_node(self, node_name='detections_retriever_node'):
    #     """Create a private rclpy node and spin it in a background thread."""
    #     # initialize rclpy if not already
    #     try:
    #         if not rclpy.ok():
    #             rclpy.init()
    #     except Exception:
    #         # rclpy.ok() may raise if rclpy not initialized in some versions; ensure init
    #         try:
    #             rclpy.init()
    #         except Exception:
    #             pass

    #     # create node and subscription
    #     if self._node is None:
    #         self._node = rclpy.create_node(node_name)
    #     if self._subscriber is None:
    #         self._subscriber = self._node.create_subscription(DetectionsArray, self._topic_name, self._callback, self._queue_size)

    #     # spin in background thread
    #     thread = threading.Thread(target=rclpy.spin, args=(self._node,), daemon=True)
    #     thread.start()
    #     self._node.get_logger().info(f"DetectionsRetriever started, listening to: {self._topic_name}")
    #     return True

class FakeDetectionsRetriever:
    def __init__(self, dataset_filename, queue_size=5):
        self._lock = Lock()
        self._detections = {}
        self._current_occupancies = {}
        self._queue_size = queue_size
        self._dataset_filename = dataset_filename
        self.human_traj_data = None
        self.load_dataset()
        self.timestamp = 1725184820.0

    def load_dataset(self):
        self.human_traj_data = read_human_traj_data_from_file(self._dataset_filename)

    # def get_detections(self):
    #     with self._lock:
    #         return self._detections


    def get_detections(self, timestamp=None):
        if timestamp is not None:
            self.timestamp = timestamp
        human_traj_data_by_time = self.human_traj_data.loc[abs(self.human_traj_data['time'] - self.timestamp) < 1 ]
        people_ids = list(human_traj_data_by_time.person_id.unique())
        tracks = {}
        self.people_trajectories = {}

        for id in people_ids:
            human_traj_data_by_person_id = self.human_traj_data.loc[self.human_traj_data['person_id'] == id]
            human_traj_array = human_traj_data_by_person_id[["time", "x", "y", "vx", "vy"]].to_numpy()
            print("human_traj_array:", human_traj_array)
            track_before_now = human_traj_array[human_traj_array[:, 0] <= self.timestamp]
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

    

    def get_current_occupancies(self, timestamp=None):
        if timestamp is not None:
            self.timestamp = timestamp
        human_traj_data_by_time = self.human_traj_data.loc[abs(self.human_traj_data['time'] - self.timestamp) < 1 ]
        people_ids = list(human_traj_data_by_time.person_id.unique())
        current_occupancies_local = []
        for id in people_ids:
            human_traj_data_by_person_id = self.human_traj_data.loc[self.human_traj_data['person_id'] == id]
            human_traj_array = human_traj_data_by_person_id[["time", "x", "y", "vx", "vy"]].to_numpy()
            track_before_now = human_traj_array[human_traj_array[:, 0] <= self.timestamp]
            if len(track_before_now) > 0:
                last_position = track_before_now[-1]
                current_occupancies_local.append(Detection(
                    person_id=id,
                    positionx=last_position[1],
                    positiony=last_position[2],
                    timestamp=self.timestamp,
                    vx=last_position[3],
                    vy=last_position[4]
                ))
        return current_occupancies_local
        


    # start on a new thread
    def start(self):
        return True
        # thread = threading.Thread(target=self.start_ros)
        # thread.start()

