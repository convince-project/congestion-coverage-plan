import matplotlib
from congestion_coverage_plan.detections_retriever.DetectionsRetriever import DetectionsRetriever
import time
from rclpy.impl import rcutils_logger
from ament_index_python.packages import get_package_share_directory
import os
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from static_devices_msgs.msg import DetectionsArray, SingleDetection

import rclpy
from rclpy.action import ActionServer, GoalResponse, CancelResponse
from rclpy.node import Node
from congestion_coverage_plan.mdp.MDP import MDP, State
from congestion_coverage_plan.map_utils.OccupancyMap import OccupancyMap
from congestion_coverage_plan.cliff_predictor.PredictorCreator import create_generic_cliff_predictor
from congestion_coverage_plan.bt_utils.BTWriter import BTWriter
from congestion_coverage_plan.detections_retriever.DetectionsRetriever import DetectionsRetriever
from congestion_coverage_plan.solver.LrtdpTvmaAlgorithm import LrtdpTvmaAlgorithm
import sys

class DetectionsVisualizer(Node):

    def __init__(self, detections_topic):
        super().__init__('detections_visualizer')
        self._detections_retriever = DetectionsRetriever(self, detections_topic)
        self.img_path = os.path.join(
            get_package_share_directory('detections_visualizer'),
            'resource',
            'madama3.jpg'
        )
        self._cliff_map_file = os.path.join(
            get_package_share_directory('detections_visualizer'),
            'config',
            'map_madama3_september.csv'
        )
        self._cliff_predictor = create_generic_cliff_predictor(self._cliff_map_file)

        plt.ion()
        # set background image
        self.fig_size = [-21.2,36.4, -53.4, 9.2 ]
        self.fig, self.ax = plt.subplots()
        self.img = plt.imread(str(self.img_path))
        self.ax.imshow(self.img, cmap='gray', vmin=0, vmax=255, extent=self.fig_size)
    
        # create a graph to be updated dynamically with the detections
        # self.scatter = self.ax.scatter([], [])
        self.ax.set_xlim(-10, 10)
        self.ax.set_ylim(-10, 10)
        self.ax.set_title('Detections')
        self.ax.set_xlabel('X Position')
        self.ax.set_ylabel('Y Position')
        # plt.show(block=False)  # <-- Add this line
        self.create_timer(1, self.plot_detections)

    def plot_detections(self):
        detections_local = self._detections_retriever.get_detections()
        print(detections_local)
        self.ax.cla()
        self.ax.imshow(self.img, cmap='gray', vmin=0, vmax=255, extent=self.fig_size)
        for det_id in detections_local:
            for det in detections_local[det_id]:
                self.ax.plot(det.positionx, det.positiony, 'o', label=f'ID {det.person_id}')
        plt.draw()
        # self.fig.canvas.draw()
        # self.fig.canvas.flush_events()
        plt.pause(0.01)


def main(args=None):
    rclpy.init(args=args)
    detections_topic = "static_tracks"
    detections_visualizer = DetectionsVisualizer(detections_topic)
    try:
        rclpy.spin(detections_visualizer)
    except KeyboardInterrupt:
        pass
    detections_visualizer.destroy_node()
    rclpy.shutdown()