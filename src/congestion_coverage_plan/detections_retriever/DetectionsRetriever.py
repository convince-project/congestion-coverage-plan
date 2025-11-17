# topic subrscriber for retrieving detections from a ROS topic
# it keeps the latest detection messages in a member variable

import rospy
from threading import Lock
import threading
from static_devices_msgs import DetectionsArray, SingleDetection


class Detection:
    def __init__(self, person_id, positionx, positiony, timestamp, vx, vy):
        self.person_id = person_id
        self.positionx = positionx
        self.positiony = positiony
        self.timestamp = timestamp
        self.vx = vx
        self.vy = vy

    


class DetectionsRetriever:
    def __init__(self, topic_name):
        self._lock = Lock()
        self._detections = {}
        self._current_occupancies = {}
        self._subscriber = rospy.Subscriber(topic_name, DetectionsArray, self._callback)


    # keep last 5 detections for each person, if it is too old, remove the person
    # TODO: check the correctness of this function
    def _callback(self, msg):
        detections_local = {}
        current_occupancies_local = {}
        for detection in msg.detections:
            detection: SingleDetection
            detection_obj = Detection(
                person_id=detection.person_id,
                positionx=detection.position.x,
                positiony=detection.position.y,
                timestamp=detection.header.stamp,
                vx=detection.velocity.x,
                vy=detection.velocity.y
            )
            detections_local[detection.person_id] = sorted([detection_obj] + self._detections.get(detection.person_id, [])[0:4] if self._detections and detection.person_id in self._detections else [detection_obj], key=lambda x: x.timestamp.secs, reverse=True)
            current_occupancies_local[detection.person_id] = (detection.position.x, detection.position.y)
        with self._lock:
            self._detections = detections_local
            self._current_occupancies = current_occupancies_local


    def get_detections(self):
        with self._lock:
            return self._detections


    def get_current_occupancies(self):
        with self._lock:
            return self._current_occupancies


    # start on a new thread
    def start(self):
        thread = threading.Thread(target=self.start_ros)
        thread.start()


    def start_ros(self):

        rospy.init_node('detections_retriever_node', anonymous=True)
        rospy.loginfo("DetectionsRetriever node started, listening to topic: %s", self._subscriber.name)
        rospy.spin()
