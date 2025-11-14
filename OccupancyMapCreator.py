from congestion_coverage_plan.map_utils.OccupancyMap import OccupancyMap
import congestion_coverage_plan.utils.dataset_utils as dataset_utils
import matplotlib.pyplot as plt
import csv
from congestion_coverage_plan.cliff_predictor.CliffPredictor import CliffPredictor
from PredictorCreator import create_atc_cliff_predictor,  create_madama_cliff_predictor
import warnings


# ---- ATC ----


def create_topological_map_atc_corridor_6(occupancy_map):
    occupancy_map.set_name('atc_corridor_6')
    occupancy_map.add_vertex_with_id("vertex1", 50.55, -26.44)
    occupancy_map.add_vertex_with_id("vertex2", 42.88, -24.13)
    occupancy_map.add_vertex_with_id("vertex3", 52.28, -23.13)
    occupancy_map.add_vertex_with_id("vertex4", 47.14, -20.26)
    occupancy_map.add_vertex_with_id("vertex5", 41.46, -21.41)
    occupancy_map.add_vertex_with_id("vertex6", 40.03, -18.72)
    
    occupancy_map.add_edge_with_incremental_id("vertex1", "vertex2")
    occupancy_map.add_edge_with_incremental_id("vertex1", "vertex3")
    occupancy_map.add_edge_with_incremental_id("vertex1", "vertex4")

    occupancy_map.add_edge_with_incremental_id("vertex2", "vertex1")
    occupancy_map.add_edge_with_incremental_id("vertex3", "vertex1")
    occupancy_map.add_edge_with_incremental_id("vertex4", "vertex1")

    occupancy_map.add_edge_with_incremental_id("vertex2", "vertex3")
    occupancy_map.add_edge_with_incremental_id("vertex2", "vertex4")
    occupancy_map.add_edge_with_incremental_id("vertex2", "vertex5")

    occupancy_map.add_edge_with_incremental_id("vertex3", "vertex2")
    occupancy_map.add_edge_with_incremental_id("vertex4", "vertex2")
    occupancy_map.add_edge_with_incremental_id("vertex5", "vertex2")

    occupancy_map.add_edge_with_incremental_id("vertex3", "vertex4")
    occupancy_map.add_edge_with_incremental_id("vertex4", "vertex3")



    occupancy_map.add_edge_with_incremental_id("vertex4", "vertex6")
    occupancy_map.add_edge_with_incremental_id("vertex4", "vertex5")
    occupancy_map.add_edge_with_incremental_id("vertex6", "vertex4")
    occupancy_map.add_edge_with_incremental_id("vertex5", "vertex4")

    occupancy_map.add_edge_with_incremental_id("vertex5", "vertex6")
    occupancy_map.add_edge_with_incremental_id("vertex6", "vertex5")


def create_topological_map_atc_corridor_11(occupancy_map):
    create_topological_map_atc_corridor_6(occupancy_map)
    occupancy_map.set_name('atc_corridor_11')
    occupancy_map.add_vertex_with_id("vertex7", 35.64, -21.17)
    occupancy_map.add_vertex_with_id("vertex8", 34.15, -17.47)
    occupancy_map.add_vertex_with_id("vertex9", 31.7, -18.0)
    occupancy_map.add_vertex_with_id("vertex10", 27.88, -18.22)
    occupancy_map.add_vertex_with_id("vertex11", 27.0, -15.14)

    occupancy_map.add_edge_with_incremental_id("vertex2", "vertex7")

    occupancy_map.add_edge_with_incremental_id("vertex7", "vertex2")

    # ----------------------------

    occupancy_map.add_edge_with_incremental_id("vertex5", "vertex7")
    occupancy_map.add_edge_with_incremental_id("vertex5", "vertex8")

    occupancy_map.add_edge_with_incremental_id("vertex7", "vertex5")
    occupancy_map.add_edge_with_incremental_id("vertex8", "vertex5")
    # ----------------------------

    occupancy_map.add_edge_with_incremental_id("vertex6", "vertex7")
    occupancy_map.add_edge_with_incremental_id("vertex6", "vertex8")

    occupancy_map.add_edge_with_incremental_id("vertex7", "vertex6")
    occupancy_map.add_edge_with_incremental_id("vertex8", "vertex6")

    # ----------------------------

    occupancy_map.add_edge_with_incremental_id("vertex7", "vertex8")
    occupancy_map.add_edge_with_incremental_id("vertex7", "vertex9")
    occupancy_map.add_edge_with_incremental_id("vertex7", "vertex10")

    occupancy_map.add_edge_with_incremental_id("vertex8", "vertex7")
    occupancy_map.add_edge_with_incremental_id("vertex9", "vertex7")
    occupancy_map.add_edge_with_incremental_id("vertex10", "vertex7")

    # ----------------------------

    occupancy_map.add_edge_with_incremental_id("vertex8", "vertex9")
    occupancy_map.add_edge_with_incremental_id("vertex8", "vertex11")

    occupancy_map.add_edge_with_incremental_id("vertex9", "vertex8")
    occupancy_map.add_edge_with_incremental_id("vertex11", "vertex8")

    # ----------------------------

    occupancy_map.add_edge_with_incremental_id("vertex9", "vertex10")
    occupancy_map.add_edge_with_incremental_id("vertex9", "vertex11")

    occupancy_map.add_edge_with_incremental_id("vertex10", "vertex9")
    occupancy_map.add_edge_with_incremental_id("vertex11", "vertex9")

    # ----------------------------

    occupancy_map.add_edge_with_incremental_id("vertex10", "vertex11")

    occupancy_map.add_edge_with_incremental_id("vertex11", "vertex10")


def create_topological_map_atc_corridor_16(occupancy_map):
    create_topological_map_atc_corridor_11(occupancy_map)
    occupancy_map.set_name('atc_corridor_16')
    occupancy_map.add_vertex_with_id("vertex12", 24.71, -16.0)
    occupancy_map.add_vertex_with_id("vertex13", 21.91, -16.2)
    occupancy_map.add_vertex_with_id("vertex14", 22.6, -11.38)
    occupancy_map.add_vertex_with_id("vertex15", 19.79, -13.51)
    occupancy_map.add_vertex_with_id("vertex16", 17.02, -14.14)

    occupancy_map.add_edge_with_incremental_id("vertex10", "vertex12")
    occupancy_map.add_edge_with_incremental_id("vertex10", "vertex13")

    occupancy_map.add_edge_with_incremental_id("vertex12", "vertex10")
    occupancy_map.add_edge_with_incremental_id("vertex13", "vertex10")
    # ----------------------------

    occupancy_map.add_edge_with_incremental_id("vertex11", "vertex12")
    occupancy_map.add_edge_with_incremental_id("vertex11", "vertex14")
    occupancy_map.add_edge_with_incremental_id("vertex11", "vertex15")

    occupancy_map.add_edge_with_incremental_id("vertex12", "vertex11")
    occupancy_map.add_edge_with_incremental_id("vertex14", "vertex11")
    occupancy_map.add_edge_with_incremental_id("vertex15", "vertex11")

    # ----------------------------

    occupancy_map.add_edge_with_incremental_id("vertex12", "vertex13")
    occupancy_map.add_edge_with_incremental_id("vertex12", "vertex14")
    occupancy_map.add_edge_with_incremental_id("vertex12", "vertex15")

    occupancy_map.add_edge_with_incremental_id("vertex13", "vertex12")
    occupancy_map.add_edge_with_incremental_id("vertex14", "vertex12")
    occupancy_map.add_edge_with_incremental_id("vertex15", "vertex12")

    # ----------------------------

    occupancy_map.add_edge_with_incremental_id("vertex13", "vertex15")
    occupancy_map.add_edge_with_incremental_id("vertex13", "vertex16")

    occupancy_map.add_edge_with_incremental_id("vertex15", "vertex13")
    occupancy_map.add_edge_with_incremental_id("vertex16", "vertex13")

    # ----------------------------

    occupancy_map.add_edge_with_incremental_id("vertex14", "vertex15")

    occupancy_map.add_edge_with_incremental_id("vertex15", "vertex14")

    # ----------------------------

    occupancy_map.add_edge_with_incremental_id("vertex15", "vertex16")

    occupancy_map.add_edge_with_incremental_id("vertex16", "vertex15")


def create_topological_map_atc_corridor_21(occupancy_map):
    create_topological_map_atc_corridor_16(occupancy_map)
    occupancy_map.set_name('atc_corridor_21')
    occupancy_map.add_vertex_with_id("vertex17", 20.6, -9.38)
    occupancy_map.add_vertex_with_id("vertex18", 16.59, -9.92)
    occupancy_map.add_vertex_with_id("vertex19", 11.28, -8.67)
    occupancy_map.add_vertex_with_id("vertex20", 17.08, -5.88)
    occupancy_map.add_vertex_with_id("vertex21", 11.5, -5.21)

    occupancy_map.add_edge_with_incremental_id("vertex14", "vertex17")
    occupancy_map.add_edge_with_incremental_id("vertex14", "vertex18")

    occupancy_map.add_edge_with_incremental_id("vertex17", "vertex14")
    occupancy_map.add_edge_with_incremental_id("vertex18", "vertex14")

    # ----------------------------

    occupancy_map.add_edge_with_incremental_id("vertex15", "vertex17")
    occupancy_map.add_edge_with_incremental_id("vertex15", "vertex18")

    occupancy_map.add_edge_with_incremental_id("vertex17", "vertex15")
    occupancy_map.add_edge_with_incremental_id("vertex18", "vertex15")

    # ----------------------------

    occupancy_map.add_edge_with_incremental_id("vertex16", "vertex18")
    occupancy_map.add_edge_with_incremental_id("vertex16", "vertex19")


    occupancy_map.add_edge_with_incremental_id("vertex18", "vertex16")
    occupancy_map.add_edge_with_incremental_id("vertex19", "vertex16")

    # ----------------------------


    occupancy_map.add_edge_with_incremental_id("vertex17", "vertex18")
    occupancy_map.add_edge_with_incremental_id("vertex17", "vertex20")

    occupancy_map.add_edge_with_incremental_id("vertex18", "vertex17")
    occupancy_map.add_edge_with_incremental_id("vertex20", "vertex17")


    # ----------------------------

    occupancy_map.add_edge_with_incremental_id("vertex18", "vertex19")
    occupancy_map.add_edge_with_incremental_id("vertex18", "vertex20")
    occupancy_map.add_edge_with_incremental_id("vertex18", "vertex21")

    occupancy_map.add_edge_with_incremental_id("vertex19", "vertex18")
    occupancy_map.add_edge_with_incremental_id("vertex20", "vertex18")
    occupancy_map.add_edge_with_incremental_id("vertex21", "vertex18")


    # ----------------------------

    occupancy_map.add_edge_with_incremental_id("vertex19", "vertex20")
    occupancy_map.add_edge_with_incremental_id("vertex19", "vertex21")

    occupancy_map.add_edge_with_incremental_id("vertex20", "vertex19")
    occupancy_map.add_edge_with_incremental_id("vertex21", "vertex19")

    # ----------------------------

    occupancy_map.add_edge_with_incremental_id("vertex20", "vertex21")

    occupancy_map.add_edge_with_incremental_id("vertex21", "vertex20")


def create_topological_map_atc_corridor_26(occupancy_map):
    create_topological_map_atc_corridor_21(occupancy_map)
    occupancy_map.set_name('atc_corridor_26')
    occupancy_map.add_vertex_with_id("vertex22", 7.11, -6.31)
    occupancy_map.add_vertex_with_id("vertex23", 11.10, -0.89)
    occupancy_map.add_vertex_with_id("vertex24", 7.00, -3.07)
    occupancy_map.add_vertex_with_id("vertex25", 6.80, 0.42)
    occupancy_map.add_vertex_with_id("vertex26", -0.09, -5.91)

    occupancy_map.add_edge_with_incremental_id("vertex19", "vertex22")
    occupancy_map.add_edge_with_incremental_id("vertex22", "vertex19")

    occupancy_map.add_edge_with_incremental_id("vertex21", "vertex22")
    occupancy_map.add_edge_with_incremental_id("vertex22", "vertex21")


    occupancy_map.add_edge_with_incremental_id("vertex20", "vertex23")
    occupancy_map.add_edge_with_incremental_id("vertex23", "vertex20")

    occupancy_map.add_edge_with_incremental_id("vertex21", "vertex23")
    occupancy_map.add_edge_with_incremental_id("vertex23", "vertex21")

    occupancy_map.add_edge_with_incremental_id("vertex21", "vertex24")
    occupancy_map.add_edge_with_incremental_id("vertex24", "vertex21")

    occupancy_map.add_edge_with_incremental_id("vertex22", "vertex24")
    occupancy_map.add_edge_with_incremental_id("vertex24", "vertex22")

    occupancy_map.add_edge_with_incremental_id("vertex23", "vertex24")
    occupancy_map.add_edge_with_incremental_id("vertex24", "vertex23")

    occupancy_map.add_edge_with_incremental_id("vertex23", "vertex25")
    occupancy_map.add_edge_with_incremental_id("vertex25", "vertex23")

    occupancy_map.add_edge_with_incremental_id("vertex24", "vertex25")
    occupancy_map.add_edge_with_incremental_id("vertex25", "vertex24")

    occupancy_map.add_edge_with_incremental_id("vertex22", "vertex26")
    occupancy_map.add_edge_with_incremental_id("vertex26", "vertex22")

    occupancy_map.add_edge_with_incremental_id("vertex24", "vertex26")
    occupancy_map.add_edge_with_incremental_id("vertex26", "vertex24")


    occupancy_map.add_edge_with_incremental_id("vertex25", "vertex26")
    
    occupancy_map.add_edge_with_incremental_id("vertex26", "vertex25")


# ---- MADAMA ----


def create_madama_topological_map_11(occupancy_map):
    occupancy_map.set_name('madama_11')
    occupancy_map.add_vertex_with_id("vertex1", 53.91, 26.05)
    occupancy_map.add_vertex_with_id("vertex2", 50.17, 32.65)
    occupancy_map.add_vertex_with_id("vertex3", 54.12, 32.65)
    occupancy_map.add_vertex_with_id("vertex4", 48.51, 43.02)
    occupancy_map.add_vertex_with_id("vertex5", 50.28, 50.69)
    occupancy_map.add_vertex_with_id("vertex6", 34.24, 41.64)
    occupancy_map.add_vertex_with_id("vertex7", 34.65, 50.53)
    occupancy_map.add_vertex_with_id("vertex8", 18.38, 45.31)
    occupancy_map.add_vertex_with_id("vertex9", 21.84, 41.71)
    occupancy_map.add_vertex_with_id("vertex10", 20.50, 28.87)
    occupancy_map.add_vertex_with_id("vertex11", 24.80, 29.86)

    occupancy_map.add_edge_with_incremental_id("vertex1", "vertex2")
    occupancy_map.add_edge_with_incremental_id("vertex1", "vertex3")
    occupancy_map.add_edge_with_incremental_id("vertex2", "vertex1")
    occupancy_map.add_edge_with_incremental_id("vertex3", "vertex1")

    occupancy_map.add_edge_with_incremental_id("vertex2", "vertex3")
    occupancy_map.add_edge_with_incremental_id("vertex3", "vertex2")
    occupancy_map.add_edge_with_incremental_id("vertex2", "vertex4")
    occupancy_map.add_edge_with_incremental_id("vertex2", "vertex5")
    occupancy_map.add_edge_with_incremental_id("vertex4", "vertex2")
    occupancy_map.add_edge_with_incremental_id("vertex5", "vertex2")

    occupancy_map.add_edge_with_incremental_id("vertex3", "vertex4")
    occupancy_map.add_edge_with_incremental_id("vertex3", "vertex5")
    occupancy_map.add_edge_with_incremental_id("vertex4", "vertex3")
    occupancy_map.add_edge_with_incremental_id("vertex5", "vertex3")

    occupancy_map.add_edge_with_incremental_id("vertex4", "vertex5")
    occupancy_map.add_edge_with_incremental_id("vertex5", "vertex4")

    occupancy_map.add_edge_with_incremental_id("vertex4", "vertex6")
    occupancy_map.add_edge_with_incremental_id("vertex4", "vertex7")
    occupancy_map.add_edge_with_incremental_id("vertex6", "vertex4")
    occupancy_map.add_edge_with_incremental_id("vertex7", "vertex4")

    occupancy_map.add_edge_with_incremental_id("vertex5", "vertex6")
    occupancy_map.add_edge_with_incremental_id("vertex5", "vertex7")
    occupancy_map.add_edge_with_incremental_id("vertex6", "vertex5")
    occupancy_map.add_edge_with_incremental_id("vertex7", "vertex5")

    occupancy_map.add_edge_with_incremental_id("vertex6", "vertex7")
    occupancy_map.add_edge_with_incremental_id("vertex7", "vertex6")

    occupancy_map.add_edge_with_incremental_id("vertex6", "vertex8")
    occupancy_map.add_edge_with_incremental_id("vertex6", "vertex9")
    occupancy_map.add_edge_with_incremental_id("vertex8", "vertex6")
    occupancy_map.add_edge_with_incremental_id("vertex9", "vertex6")

    occupancy_map.add_edge_with_incremental_id("vertex7", "vertex8")
    occupancy_map.add_edge_with_incremental_id("vertex7", "vertex9")
    occupancy_map.add_edge_with_incremental_id("vertex8", "vertex7")
    occupancy_map.add_edge_with_incremental_id("vertex9", "vertex7")

    occupancy_map.add_edge_with_incremental_id("vertex8", "vertex9")
    occupancy_map.add_edge_with_incremental_id("vertex9", "vertex8")

    occupancy_map.add_edge_with_incremental_id("vertex8", "vertex10")
    occupancy_map.add_edge_with_incremental_id("vertex8", "vertex11")
    occupancy_map.add_edge_with_incremental_id("vertex10", "vertex8")
    occupancy_map.add_edge_with_incremental_id("vertex11", "vertex8")

    occupancy_map.add_edge_with_incremental_id("vertex9", "vertex10")
    occupancy_map.add_edge_with_incremental_id("vertex9", "vertex11")
    occupancy_map.add_edge_with_incremental_id("vertex10", "vertex9")
    occupancy_map.add_edge_with_incremental_id("vertex11", "vertex9")

    occupancy_map.add_edge_with_incremental_id("vertex10", "vertex11")
    occupancy_map.add_edge_with_incremental_id("vertex11", "vertex10")


def create_madama_topological_map_16(occupancy_map):
    create_madama_topological_map_11(occupancy_map)
    occupancy_map.set_name('madama_16')
    occupancy_map.add_vertex_with_id("vertex12", 51.68, 30.24)
    occupancy_map.add_vertex_with_id("vertex13", 53.52, 42.5)
    occupancy_map.add_vertex_with_id("vertex14", 29.83, 46.08)
    occupancy_map.add_vertex_with_id("vertex15", 21.24, 48.84)
    occupancy_map.add_vertex_with_id("vertex16", 23.91, 34.07)

    occupancy_map.add_edge_with_incremental_id("vertex1", "vertex12")
    occupancy_map.add_edge_with_incremental_id("vertex12", "vertex1")

    # ***

    occupancy_map.add_edge_with_incremental_id("vertex2", "vertex12")
    occupancy_map.add_edge_with_incremental_id("vertex12", "vertex2")

    occupancy_map.add_edge_with_incremental_id("vertex3", "vertex12")
    occupancy_map.add_edge_with_incremental_id("vertex12", "vertex3")

    # ***

    occupancy_map.add_edge_with_incremental_id("vertex4", "vertex12")
    occupancy_map.add_edge_with_incremental_id("vertex12", "vertex4")

    occupancy_map.add_edge_with_incremental_id("vertex5", "vertex12")
    occupancy_map.add_edge_with_incremental_id("vertex12", "vertex5")

    occupancy_map.add_edge_with_incremental_id("vertex12", "vertex13")
    occupancy_map.add_edge_with_incremental_id("vertex13", "vertex12")

    # ----------------------------

    occupancy_map.add_edge_with_incremental_id("vertex3", "vertex13")
    occupancy_map.add_edge_with_incremental_id("vertex13", "vertex3")

    occupancy_map.add_edge_with_incremental_id("vertex2", "vertex13")
    occupancy_map.add_edge_with_incremental_id("vertex13", "vertex2")

    # ***

    occupancy_map.add_edge_with_incremental_id("vertex4", "vertex13")
    occupancy_map.add_edge_with_incremental_id("vertex13", "vertex4")

    occupancy_map.add_edge_with_incremental_id("vertex5", "vertex13")
    occupancy_map.add_edge_with_incremental_id("vertex13", "vertex5")

    # ***

    occupancy_map.add_edge_with_incremental_id("vertex6", "vertex13")
    occupancy_map.add_edge_with_incremental_id("vertex13", "vertex6")

    occupancy_map.add_edge_with_incremental_id("vertex7", "vertex13")
    occupancy_map.add_edge_with_incremental_id("vertex13", "vertex7")

    occupancy_map.add_edge_with_incremental_id("vertex13", "vertex14")
    occupancy_map.add_edge_with_incremental_id("vertex14", "vertex13")

    # ----------------------------

    occupancy_map.add_edge_with_incremental_id("vertex4", "vertex14")
    occupancy_map.add_edge_with_incremental_id("vertex14", "vertex4")

    occupancy_map.add_edge_with_incremental_id("vertex5", "vertex14")
    occupancy_map.add_edge_with_incremental_id("vertex14", "vertex5")

    # *** 

    occupancy_map.add_edge_with_incremental_id("vertex6", "vertex14")
    occupancy_map.add_edge_with_incremental_id("vertex14", "vertex6")

    occupancy_map.add_edge_with_incremental_id("vertex7", "vertex14")
    occupancy_map.add_edge_with_incremental_id("vertex14", "vertex7")

    # ***

    occupancy_map.add_edge_with_incremental_id("vertex8", "vertex14")
    occupancy_map.add_edge_with_incremental_id("vertex14", "vertex8")

    occupancy_map.add_edge_with_incremental_id("vertex9", "vertex14")
    occupancy_map.add_edge_with_incremental_id("vertex14", "vertex9")

    occupancy_map.add_edge_with_incremental_id("vertex14", "vertex15")
    occupancy_map.add_edge_with_incremental_id("vertex15", "vertex14")

    # ----------------------------

    occupancy_map.add_edge_with_incremental_id("vertex6", "vertex15")
    occupancy_map.add_edge_with_incremental_id("vertex15", "vertex6")

    occupancy_map.add_edge_with_incremental_id("vertex7", "vertex15")
    occupancy_map.add_edge_with_incremental_id("vertex15", "vertex7")

    # ***

    occupancy_map.add_edge_with_incremental_id("vertex8", "vertex15")
    occupancy_map.add_edge_with_incremental_id("vertex15", "vertex8")

    occupancy_map.add_edge_with_incremental_id("vertex9", "vertex15")
    occupancy_map.add_edge_with_incremental_id("vertex15", "vertex9")

    # ***

    occupancy_map.add_edge_with_incremental_id("vertex10", "vertex15")
    occupancy_map.add_edge_with_incremental_id("vertex15", "vertex10")

    occupancy_map.add_edge_with_incremental_id("vertex11", "vertex15")
    occupancy_map.add_edge_with_incremental_id("vertex15", "vertex11")

    occupancy_map.add_edge_with_incremental_id("vertex15", "vertex16")
    occupancy_map.add_edge_with_incremental_id("vertex16", "vertex15")

    # ----------------------------

    occupancy_map.add_edge_with_incremental_id("vertex8", "vertex16")
    occupancy_map.add_edge_with_incremental_id("vertex16", "vertex8")

    occupancy_map.add_edge_with_incremental_id("vertex9", "vertex16")
    occupancy_map.add_edge_with_incremental_id("vertex16", "vertex9")

    # ***

    occupancy_map.add_edge_with_incremental_id("vertex10", "vertex16")
    occupancy_map.add_edge_with_incremental_id("vertex16", "vertex10")

    occupancy_map.add_edge_with_incremental_id("vertex11", "vertex16")
    occupancy_map.add_edge_with_incremental_id("vertex16", "vertex11")


def create_madama_topological_map_21(occupancy_map):
    create_madama_topological_map_16(occupancy_map)
    occupancy_map.set_name('madama_21')
    occupancy_map.add_vertex_with_id("vertex17", 52.44, 34.06)
    occupancy_map.add_vertex_with_id("vertex18", 53.42, 45.28)
    occupancy_map.add_vertex_with_id("vertex19", 38.98, 44.86)
    occupancy_map.add_vertex_with_id("vertex20", 20.48, 43.66)
    occupancy_map.add_vertex_with_id("vertex21", 21.81, 32.66)

    # ---------------------------- 17 connections
    # *** Previous room
    occupancy_map.add_edge_with_incremental_id("vertex1", "vertex17")
    occupancy_map.add_edge_with_incremental_id("vertex17", "vertex1")

    # *** Current room

    occupancy_map.add_edge_with_incremental_id("vertex2", "vertex17")
    occupancy_map.add_edge_with_incremental_id("vertex17", "vertex2")

    occupancy_map.add_edge_with_incremental_id("vertex3", "vertex17")
    occupancy_map.add_edge_with_incremental_id("vertex17", "vertex3")

    occupancy_map.add_edge_with_incremental_id("vertex12", "vertex17")
    occupancy_map.add_edge_with_incremental_id("vertex17", "vertex12")

    # *** Next room

    occupancy_map.add_edge_with_incremental_id("vertex4", "vertex17")
    occupancy_map.add_edge_with_incremental_id("vertex17", "vertex4")

    occupancy_map.add_edge_with_incremental_id("vertex5", "vertex17")
    occupancy_map.add_edge_with_incremental_id("vertex17", "vertex5")

    occupancy_map.add_edge_with_incremental_id("vertex13", "vertex17")
    occupancy_map.add_edge_with_incremental_id("vertex17", "vertex13")



    # ---------------------------- 18 connections
    # *** Previous room
    occupancy_map.add_edge_with_incremental_id("vertex2", "vertex18")
    occupancy_map.add_edge_with_incremental_id("vertex18", "vertex2")

    occupancy_map.add_edge_with_incremental_id("vertex3", "vertex18")
    occupancy_map.add_edge_with_incremental_id("vertex18", "vertex3")

    occupancy_map.add_edge_with_incremental_id("vertex12", "vertex18")
    occupancy_map.add_edge_with_incremental_id("vertex18", "vertex12")

    occupancy_map.add_edge_with_incremental_id("vertex17", "vertex18")
    occupancy_map.add_edge_with_incremental_id("vertex18", "vertex17")
    
    # *** current room

    occupancy_map.add_edge_with_incremental_id("vertex4", "vertex18")
    occupancy_map.add_edge_with_incremental_id("vertex18", "vertex4")

    occupancy_map.add_edge_with_incremental_id("vertex5", "vertex18")
    occupancy_map.add_edge_with_incremental_id("vertex18", "vertex5")

    occupancy_map.add_edge_with_incremental_id("vertex13", "vertex18")
    occupancy_map.add_edge_with_incremental_id("vertex18", "vertex13")

    # *** Next room

    occupancy_map.add_edge_with_incremental_id("vertex6", "vertex18")
    occupancy_map.add_edge_with_incremental_id("vertex18", "vertex6")

    occupancy_map.add_edge_with_incremental_id("vertex7", "vertex18")
    occupancy_map.add_edge_with_incremental_id("vertex18", "vertex7")

    occupancy_map.add_edge_with_incremental_id("vertex18", "vertex14")
    occupancy_map.add_edge_with_incremental_id("vertex14", "vertex18")

    # ---------------------------- 19 connections
    # *** Previous room

    occupancy_map.add_edge_with_incremental_id("vertex4", "vertex19")
    occupancy_map.add_edge_with_incremental_id("vertex19", "vertex4")

    occupancy_map.add_edge_with_incremental_id("vertex5", "vertex19")
    occupancy_map.add_edge_with_incremental_id("vertex19", "vertex5")

    occupancy_map.add_edge_with_incremental_id("vertex13", "vertex19")
    occupancy_map.add_edge_with_incremental_id("vertex19", "vertex13")

    occupancy_map.add_edge_with_incremental_id("vertex18", "vertex19")  
    occupancy_map.add_edge_with_incremental_id("vertex19", "vertex18")

    # *** current room

    occupancy_map.add_edge_with_incremental_id("vertex6", "vertex19")
    occupancy_map.add_edge_with_incremental_id("vertex19", "vertex6")

    occupancy_map.add_edge_with_incremental_id("vertex7", "vertex19")
    occupancy_map.add_edge_with_incremental_id("vertex19", "vertex7")

    occupancy_map.add_edge_with_incremental_id("vertex14", "vertex19")
    occupancy_map.add_edge_with_incremental_id("vertex19", "vertex14")

    # *** Next room

    occupancy_map.add_edge_with_incremental_id("vertex8", "vertex19")
    occupancy_map.add_edge_with_incremental_id("vertex19", "vertex8")

    occupancy_map.add_edge_with_incremental_id("vertex9", "vertex19")
    occupancy_map.add_edge_with_incremental_id("vertex19", "vertex9")

    occupancy_map.add_edge_with_incremental_id("vertex15", "vertex20")
    occupancy_map.add_edge_with_incremental_id("vertex20", "vertex15")

    # ---------------------------- 20 connections

    # *** Previous room
    occupancy_map.add_edge_with_incremental_id("vertex6", "vertex20")
    occupancy_map.add_edge_with_incremental_id("vertex20", "vertex6")

    occupancy_map.add_edge_with_incremental_id("vertex7", "vertex20")
    occupancy_map.add_edge_with_incremental_id("vertex20", "vertex7")

    occupancy_map.add_edge_with_incremental_id("vertex14", "vertex20")
    occupancy_map.add_edge_with_incremental_id("vertex20", "vertex14")

    occupancy_map.add_edge_with_incremental_id("vertex19", "vertex20")
    occupancy_map.add_edge_with_incremental_id("vertex20", "vertex19")

    # *** current room

    occupancy_map.add_edge_with_incremental_id("vertex8", "vertex20")
    occupancy_map.add_edge_with_incremental_id("vertex20", "vertex8")

    occupancy_map.add_edge_with_incremental_id("vertex9", "vertex20")
    occupancy_map.add_edge_with_incremental_id("vertex20", "vertex9")

    occupancy_map.add_edge_with_incremental_id("vertex15", "vertex20")
    occupancy_map.add_edge_with_incremental_id("vertex20", "vertex15")

    # *** Next room

    occupancy_map.add_edge_with_incremental_id("vertex10", "vertex20")
    occupancy_map.add_edge_with_incremental_id("vertex20", "vertex10")

    occupancy_map.add_edge_with_incremental_id("vertex11", "vertex20")
    occupancy_map.add_edge_with_incremental_id("vertex20", "vertex11")

    occupancy_map.add_edge_with_incremental_id("vertex16", "vertex20")
    occupancy_map.add_edge_with_incremental_id("vertex20", "vertex16")

    # ---------------------------- 21 connections

    # *** Previous room

    occupancy_map.add_edge_with_incremental_id("vertex8", "vertex21")
    occupancy_map.add_edge_with_incremental_id("vertex21", "vertex8")

    occupancy_map.add_edge_with_incremental_id("vertex9", "vertex21")
    occupancy_map.add_edge_with_incremental_id("vertex21", "vertex9")

    occupancy_map.add_edge_with_incremental_id("vertex15", "vertex21")
    occupancy_map.add_edge_with_incremental_id("vertex21", "vertex15")

    occupancy_map.add_edge_with_incremental_id("vertex20", "vertex21")
    occupancy_map.add_edge_with_incremental_id("vertex21", "vertex20")

    # *** current room

    occupancy_map.add_edge_with_incremental_id("vertex10", "vertex21")
    occupancy_map.add_edge_with_incremental_id("vertex21", "vertex10")

    occupancy_map.add_edge_with_incremental_id("vertex11", "vertex21")
    occupancy_map.add_edge_with_incremental_id("vertex21", "vertex11")

    occupancy_map.add_edge_with_incremental_id("vertex16", "vertex21")
    occupancy_map.add_edge_with_incremental_id("vertex21", "vertex16")


def create_madama_topological_map_26(occupancy_map):
    create_madama_topological_map_21(occupancy_map)
    occupancy_map.set_name('madama_26')
    occupancy_map.add_vertex_with_id("vertex22", 48.99, 36.83)
    occupancy_map.add_vertex_with_id("vertex23", 47.82, 48.35)
    occupancy_map.add_vertex_with_id("vertex24", 36.67, 46.54)
    occupancy_map.add_vertex_with_id("vertex25", 22.16, 45.91)
    occupancy_map.add_vertex_with_id("vertex26", 20.20, 34.83)

    # ---------------------------- 22 connections
    # *** Previous room

    occupancy_map.add_edge_with_incremental_id("vertex1", "vertex22")
    occupancy_map.add_edge_with_incremental_id("vertex22", "vertex1")

    # *** Current room

    occupancy_map.add_edge_with_incremental_id("vertex2", "vertex22")
    occupancy_map.add_edge_with_incremental_id("vertex22", "vertex2")

    occupancy_map.add_edge_with_incremental_id("vertex3", "vertex22")
    occupancy_map.add_edge_with_incremental_id("vertex22", "vertex3")

    occupancy_map.add_edge_with_incremental_id("vertex12", "vertex22")
    occupancy_map.add_edge_with_incremental_id("vertex22", "vertex12")

    occupancy_map.add_edge_with_incremental_id("vertex17", "vertex22")
    occupancy_map.add_edge_with_incremental_id("vertex22", "vertex17")

    # *** Next room

    occupancy_map.add_edge_with_incremental_id("vertex4", "vertex22")
    occupancy_map.add_edge_with_incremental_id("vertex22", "vertex4")

    occupancy_map.add_edge_with_incremental_id("vertex5", "vertex22")
    occupancy_map.add_edge_with_incremental_id("vertex22", "vertex5")

    occupancy_map.add_edge_with_incremental_id("vertex13", "vertex22")
    occupancy_map.add_edge_with_incremental_id("vertex22", "vertex13")

    occupancy_map.add_edge_with_incremental_id("vertex18", "vertex22")
    occupancy_map.add_edge_with_incremental_id("vertex22", "vertex18")

    # ---------------------------- 23 connections

    # *** Previous room

    occupancy_map.add_edge_with_incremental_id("vertex2", "vertex23")
    occupancy_map.add_edge_with_incremental_id("vertex23", "vertex2")

    occupancy_map.add_edge_with_incremental_id("vertex3", "vertex23")
    occupancy_map.add_edge_with_incremental_id("vertex23", "vertex3")

    occupancy_map.add_edge_with_incremental_id("vertex12", "vertex23")
    occupancy_map.add_edge_with_incremental_id("vertex23", "vertex12")

    occupancy_map.add_edge_with_incremental_id("vertex17", "vertex23")
    occupancy_map.add_edge_with_incremental_id("vertex23", "vertex17")

    occupancy_map.add_edge_with_incremental_id("vertex22", "vertex23")
    occupancy_map.add_edge_with_incremental_id("vertex23", "vertex22")

    # *** current room

    occupancy_map.add_edge_with_incremental_id("vertex4", "vertex23")
    occupancy_map.add_edge_with_incremental_id("vertex23", "vertex4")

    occupancy_map.add_edge_with_incremental_id("vertex5", "vertex23")
    occupancy_map.add_edge_with_incremental_id("vertex23", "vertex5")

    occupancy_map.add_edge_with_incremental_id("vertex13", "vertex23")
    occupancy_map.add_edge_with_incremental_id("vertex23", "vertex13")

    occupancy_map.add_edge_with_incremental_id("vertex18", "vertex23")
    occupancy_map.add_edge_with_incremental_id("vertex23", "vertex18")

    # *** Next room

    occupancy_map.add_edge_with_incremental_id("vertex6", "vertex23")
    occupancy_map.add_edge_with_incremental_id("vertex23", "vertex6")

    occupancy_map.add_edge_with_incremental_id("vertex7", "vertex23")
    occupancy_map.add_edge_with_incremental_id("vertex23", "vertex7")

    occupancy_map.add_edge_with_incremental_id("vertex14", "vertex23")
    occupancy_map.add_edge_with_incremental_id("vertex23", "vertex14")

    occupancy_map.add_edge_with_incremental_id("vertex19", "vertex23")
    occupancy_map.add_edge_with_incremental_id("vertex23", "vertex19")

    # ---------------------------- 24 connections

    # *** Previous room

    occupancy_map.add_edge_with_incremental_id("vertex4", "vertex24")
    occupancy_map.add_edge_with_incremental_id("vertex24", "vertex4")

    occupancy_map.add_edge_with_incremental_id("vertex5", "vertex24")
    occupancy_map.add_edge_with_incremental_id("vertex24", "vertex5")

    occupancy_map.add_edge_with_incremental_id("vertex13", "vertex24")
    occupancy_map.add_edge_with_incremental_id("vertex24", "vertex13")

    occupancy_map.add_edge_with_incremental_id("vertex18", "vertex24")
    occupancy_map.add_edge_with_incremental_id("vertex24", "vertex18")

    occupancy_map.add_edge_with_incremental_id("vertex23", "vertex24")
    occupancy_map.add_edge_with_incremental_id("vertex24", "vertex23")

    # *** current room

    occupancy_map.add_edge_with_incremental_id("vertex6", "vertex24")
    occupancy_map.add_edge_with_incremental_id("vertex24", "vertex6")

    occupancy_map.add_edge_with_incremental_id("vertex7", "vertex24")
    occupancy_map.add_edge_with_incremental_id("vertex24", "vertex7")

    occupancy_map.add_edge_with_incremental_id("vertex14", "vertex24")
    occupancy_map.add_edge_with_incremental_id("vertex24", "vertex14")

    occupancy_map.add_edge_with_incremental_id("vertex19", "vertex24")
    occupancy_map.add_edge_with_incremental_id("vertex24", "vertex19")

    # *** Next room

    occupancy_map.add_edge_with_incremental_id("vertex8", "vertex24")
    occupancy_map.add_edge_with_incremental_id("vertex24", "vertex8")

    occupancy_map.add_edge_with_incremental_id("vertex9", "vertex24")
    occupancy_map.add_edge_with_incremental_id("vertex24", "vertex9")

    occupancy_map.add_edge_with_incremental_id("vertex15", "vertex24")
    occupancy_map.add_edge_with_incremental_id("vertex24", "vertex15")

    occupancy_map.add_edge_with_incremental_id("vertex20", "vertex24")
    occupancy_map.add_edge_with_incremental_id("vertex24", "vertex20")

    # ---------------------------- 25 connections

    # *** Previous room

    occupancy_map.add_edge_with_incremental_id("vertex6", "vertex25")
    occupancy_map.add_edge_with_incremental_id("vertex25", "vertex6")

    occupancy_map.add_edge_with_incremental_id("vertex7", "vertex25")
    occupancy_map.add_edge_with_incremental_id("vertex25", "vertex7")

    occupancy_map.add_edge_with_incremental_id("vertex14", "vertex25")
    occupancy_map.add_edge_with_incremental_id("vertex25", "vertex14")

    occupancy_map.add_edge_with_incremental_id("vertex19", "vertex25")
    occupancy_map.add_edge_with_incremental_id("vertex25", "vertex19")

    occupancy_map.add_edge_with_incremental_id("vertex24", "vertex25")
    occupancy_map.add_edge_with_incremental_id("vertex25", "vertex24")

    # *** current room

    occupancy_map.add_edge_with_incremental_id("vertex8", "vertex25")
    occupancy_map.add_edge_with_incremental_id("vertex25", "vertex8")

    occupancy_map.add_edge_with_incremental_id("vertex9", "vertex25")
    occupancy_map.add_edge_with_incremental_id("vertex25", "vertex9")

    occupancy_map.add_edge_with_incremental_id("vertex15", "vertex25")
    occupancy_map.add_edge_with_incremental_id("vertex25", "vertex15")

    occupancy_map.add_edge_with_incremental_id("vertex20", "vertex25")
    occupancy_map.add_edge_with_incremental_id("vertex25", "vertex20")

    # *** Next room

    occupancy_map.add_edge_with_incremental_id("vertex10", "vertex25")
    occupancy_map.add_edge_with_incremental_id("vertex25", "vertex10")

    occupancy_map.add_edge_with_incremental_id("vertex11", "vertex25")
    occupancy_map.add_edge_with_incremental_id("vertex25", "vertex11")

    occupancy_map.add_edge_with_incremental_id("vertex16", "vertex25")
    occupancy_map.add_edge_with_incremental_id("vertex25", "vertex16")

    occupancy_map.add_edge_with_incremental_id("vertex21", "vertex25")
    occupancy_map.add_edge_with_incremental_id("vertex25", "vertex21")

    # ---------------------------- 26 connections

    # *** Previous room

    occupancy_map.add_edge_with_incremental_id("vertex8", "vertex26")
    occupancy_map.add_edge_with_incremental_id("vertex26", "vertex8")

    occupancy_map.add_edge_with_incremental_id("vertex9", "vertex26")
    occupancy_map.add_edge_with_incremental_id("vertex26", "vertex9")

    occupancy_map.add_edge_with_incremental_id("vertex15", "vertex26")
    occupancy_map.add_edge_with_incremental_id("vertex26", "vertex15")

    occupancy_map.add_edge_with_incremental_id("vertex20", "vertex26")
    occupancy_map.add_edge_with_incremental_id("vertex26", "vertex20")

    occupancy_map.add_edge_with_incremental_id("vertex25", "vertex26")
    occupancy_map.add_edge_with_incremental_id("vertex26", "vertex25")

    # *** current room

    occupancy_map.add_edge_with_incremental_id("vertex10", "vertex26")
    occupancy_map.add_edge_with_incremental_id("vertex26", "vertex10")

    occupancy_map.add_edge_with_incremental_id("vertex11", "vertex26")
    occupancy_map.add_edge_with_incremental_id("vertex26", "vertex11")

    occupancy_map.add_edge_with_incremental_id("vertex16", "vertex26")
    occupancy_map.add_edge_with_incremental_id("vertex26", "vertex16")

    occupancy_map.add_edge_with_incremental_id("vertex21", "vertex26")
    occupancy_map.add_edge_with_incremental_id("vertex26", "vertex21")


# ---- MADAMA DOORS ----


def create_madama_topological_map_doors_16(occupancy_map):
    occupancy_map.set_name('madama_doors_16')
    occupancy_map.add_vertex_with_id("vertex1", 53.91, 26.05)
    occupancy_map.add_vertex_with_id("vertex2", 50.17, 32.65)
    occupancy_map.add_vertex_with_id("vertex3", 54.12, 32.65)
    occupancy_map.add_vertex_with_id("vertex4", 48.51, 43.02)
    occupancy_map.add_vertex_with_id("vertex5", 50.28, 50.69)
    occupancy_map.add_vertex_with_id("vertex6", 34.24, 41.64)
    occupancy_map.add_vertex_with_id("vertex7", 34.65, 50.53)
    occupancy_map.add_vertex_with_id("vertex8", 18.38, 45.31)
    occupancy_map.add_vertex_with_id("vertex9", 21.84, 41.71)
    occupancy_map.add_vertex_with_id("vertex10", 20.50, 28.87)
    occupancy_map.add_vertex_with_id("vertex11", 24.80, 29.86)
    occupancy_map.add_vertex_with_id("vertex12", 51.81, 39.04) # door 1
    occupancy_map.add_vertex_with_id("vertex13", 45.43, 41.42) # door 2
    occupancy_map.add_vertex_with_id("vertex14", 45.15, 49.20) # door 3
    occupancy_map.add_vertex_with_id("vertex15", 23.98, 40.09) # door 4
    occupancy_map.add_vertex_with_id("vertex16", 18.80, 37.43) # door 5


    # start poi
    occupancy_map.add_edge_with_incremental_id("vertex1", "vertex2")
    occupancy_map.add_edge_with_incremental_id("vertex1", "vertex3")
    occupancy_map.add_edge_with_incremental_id("vertex2", "vertex1")
    occupancy_map.add_edge_with_incremental_id("vertex3", "vertex1")

    # first room

    occupancy_map.add_edge_with_incremental_id("vertex2", "vertex3")
    occupancy_map.add_edge_with_incremental_id("vertex3", "vertex2")

    # first door

    occupancy_map.add_edge_with_incremental_id("vertex2", "vertex12")
    occupancy_map.add_edge_with_incremental_id("vertex12", "vertex2")
    occupancy_map.add_edge_with_incremental_id("vertex3", "vertex12")
    occupancy_map.add_edge_with_incremental_id("vertex12", "vertex3")

    occupancy_map.add_edge_with_incremental_id("vertex12", "vertex4")
    occupancy_map.add_edge_with_incremental_id("vertex4", "vertex12")
    occupancy_map.add_edge_with_incremental_id("vertex12", "vertex5")
    occupancy_map.add_edge_with_incremental_id("vertex5", "vertex12")

    # second room

    occupancy_map.add_edge_with_incremental_id("vertex4", "vertex5")
    occupancy_map.add_edge_with_incremental_id("vertex5", "vertex4")

    # second door

    occupancy_map.add_edge_with_incremental_id("vertex4", "vertex13")
    occupancy_map.add_edge_with_incremental_id("vertex13", "vertex4")
    occupancy_map.add_edge_with_incremental_id("vertex5", "vertex13")
    occupancy_map.add_edge_with_incremental_id("vertex13", "vertex5")

    occupancy_map.add_edge_with_incremental_id("vertex13", "vertex6")
    occupancy_map.add_edge_with_incremental_id("vertex6", "vertex13")
    occupancy_map.add_edge_with_incremental_id("vertex13", "vertex7")
    occupancy_map.add_edge_with_incremental_id("vertex7", "vertex13")

    # third door

    occupancy_map.add_edge_with_incremental_id("vertex4", "vertex14")
    occupancy_map.add_edge_with_incremental_id("vertex14", "vertex4")
    occupancy_map.add_edge_with_incremental_id("vertex5", "vertex14")
    occupancy_map.add_edge_with_incremental_id("vertex14", "vertex5")

    occupancy_map.add_edge_with_incremental_id("vertex14", "vertex6")
    occupancy_map.add_edge_with_incremental_id("vertex6", "vertex14")
    occupancy_map.add_edge_with_incremental_id("vertex14", "vertex7")
    occupancy_map.add_edge_with_incremental_id("vertex7", "vertex14")

    # third room

    occupancy_map.add_edge_with_incremental_id("vertex6", "vertex7")
    occupancy_map.add_edge_with_incremental_id("vertex7", "vertex6")

    # fourth door

    occupancy_map.add_edge_with_incremental_id("vertex6", "vertex15")
    occupancy_map.add_edge_with_incremental_id("vertex15", "vertex6")
    occupancy_map.add_edge_with_incremental_id("vertex7", "vertex15")
    occupancy_map.add_edge_with_incremental_id("vertex15", "vertex7")

    occupancy_map.add_edge_with_incremental_id("vertex15", "vertex8")
    occupancy_map.add_edge_with_incremental_id("vertex8", "vertex15")
    occupancy_map.add_edge_with_incremental_id("vertex15", "vertex9")
    occupancy_map.add_edge_with_incremental_id("vertex9", "vertex15")

    # fourth room

    occupancy_map.add_edge_with_incremental_id("vertex8", "vertex9")
    occupancy_map.add_edge_with_incremental_id("vertex9", "vertex8")

    # fifth door

    occupancy_map.add_edge_with_incremental_id("vertex8", "vertex16")
    occupancy_map.add_edge_with_incremental_id("vertex16", "vertex8")
    occupancy_map.add_edge_with_incremental_id("vertex9", "vertex16")
    occupancy_map.add_edge_with_incremental_id("vertex16", "vertex9")

    occupancy_map.add_edge_with_incremental_id("vertex16", "vertex10")
    occupancy_map.add_edge_with_incremental_id("vertex10", "vertex16")
    occupancy_map.add_edge_with_incremental_id("vertex16", "vertex11")
    occupancy_map.add_edge_with_incremental_id("vertex11", "vertex16")

    # fifth room

    occupancy_map.add_edge_with_incremental_id("vertex10", "vertex11")
    occupancy_map.add_edge_with_incremental_id("vertex11", "vertex10")


def create_madama_topological_map_doors_21(occupancy_map):
    create_madama_topological_map_doors_16(occupancy_map)
    occupancy_map.set_name('madama_doors_21')
    occupancy_map.add_vertex_with_id("vertex17", 50.20, 28.17)
    occupancy_map.add_vertex_with_id("vertex18", 54.19, 46.19)
    occupancy_map.add_vertex_with_id("vertex19", 38.98, 44.86)
    occupancy_map.add_vertex_with_id("vertex20", 21.48, 46.66)
    occupancy_map.add_vertex_with_id("vertex21", 21.81, 32.66)

    # 17 is in the first room

    occupancy_map.add_edge_with_incremental_id("vertex1", "vertex17")
    occupancy_map.add_edge_with_incremental_id("vertex17", "vertex1")

    occupancy_map.add_edge_with_incremental_id("vertex2", "vertex17")
    occupancy_map.add_edge_with_incremental_id("vertex17", "vertex2")

    occupancy_map.add_edge_with_incremental_id("vertex3", "vertex17")
    occupancy_map.add_edge_with_incremental_id("vertex17", "vertex3")

    # 17 door connections

    occupancy_map.add_edge_with_incremental_id("vertex12", "vertex17")
    occupancy_map.add_edge_with_incremental_id("vertex17", "vertex12")

    # 18 is in the second room

    occupancy_map.add_edge_with_incremental_id("vertex4", "vertex18")
    occupancy_map.add_edge_with_incremental_id("vertex18", "vertex4")

    occupancy_map.add_edge_with_incremental_id("vertex5", "vertex18")
    occupancy_map.add_edge_with_incremental_id("vertex18", "vertex5")

    # 18 to first door connections

    occupancy_map.add_edge_with_incremental_id("vertex12", "vertex18")
    occupancy_map.add_edge_with_incremental_id("vertex18", "vertex12")

    # 18 to second door connections

    occupancy_map.add_edge_with_incremental_id("vertex13", "vertex18")
    occupancy_map.add_edge_with_incremental_id("vertex18", "vertex13")

    #18 to third door connections

    occupancy_map.add_edge_with_incremental_id("vertex14", "vertex18")
    occupancy_map.add_edge_with_incremental_id("vertex18", "vertex14")

    # 19 is in the third room

    occupancy_map.add_edge_with_incremental_id("vertex6", "vertex19")
    occupancy_map.add_edge_with_incremental_id("vertex19", "vertex6")

    occupancy_map.add_edge_with_incremental_id("vertex7", "vertex19")
    occupancy_map.add_edge_with_incremental_id("vertex19", "vertex7")

    # 19 to second door connections

    occupancy_map.add_edge_with_incremental_id("vertex13", "vertex19")
    occupancy_map.add_edge_with_incremental_id("vertex19", "vertex13")

    # 19 to third door connections

    occupancy_map.add_edge_with_incremental_id("vertex14", "vertex19")
    occupancy_map.add_edge_with_incremental_id("vertex19", "vertex14")

    # 19 to fourth door connections

    occupancy_map.add_edge_with_incremental_id("vertex15", "vertex19")
    occupancy_map.add_edge_with_incremental_id("vertex19", "vertex15")

    # 20 is in the fourth room

    occupancy_map.add_edge_with_incremental_id("vertex8", "vertex20")
    occupancy_map.add_edge_with_incremental_id("vertex20", "vertex8")

    occupancy_map.add_edge_with_incremental_id("vertex9", "vertex20")
    occupancy_map.add_edge_with_incremental_id("vertex20", "vertex9")

    # 20 to fourth door connections

    occupancy_map.add_edge_with_incremental_id("vertex15", "vertex20")
    occupancy_map.add_edge_with_incremental_id("vertex20", "vertex15")

    # 20 to fifth door connections

    occupancy_map.add_edge_with_incremental_id("vertex16", "vertex20")
    occupancy_map.add_edge_with_incremental_id("vertex20", "vertex16")

    # 21 is in the fifth room

    occupancy_map.add_edge_with_incremental_id("vertex10", "vertex21")
    occupancy_map.add_edge_with_incremental_id("vertex21", "vertex10")

    occupancy_map.add_edge_with_incremental_id("vertex11", "vertex21")
    occupancy_map.add_edge_with_incremental_id("vertex21", "vertex11")

    # 21 to fifth door connections

    occupancy_map.add_edge_with_incremental_id("vertex16", "vertex21")
    occupancy_map.add_edge_with_incremental_id("vertex21", "vertex16")


def create_madama_topological_map_doors_26(occupancy_map):
    create_madama_topological_map_doors_21(occupancy_map)
    occupancy_map.set_name('madama_doors_26')
    occupancy_map.add_vertex_with_id("vertex22", 48.99, 36.83)
    occupancy_map.add_vertex_with_id("vertex23", 49.82, 47.35)
    occupancy_map.add_vertex_with_id("vertex24", 31.67, 46.54)
    occupancy_map.add_vertex_with_id("vertex25", 18.16, 41.91)
    occupancy_map.add_vertex_with_id("vertex26", 23.20, 25.83)

    # 22 is in the first room

    occupancy_map.add_edge_with_incremental_id("vertex1", "vertex22")
    occupancy_map.add_edge_with_incremental_id("vertex22", "vertex1")

    occupancy_map.add_edge_with_incremental_id("vertex2", "vertex22")
    occupancy_map.add_edge_with_incremental_id("vertex22", "vertex2")

    occupancy_map.add_edge_with_incremental_id("vertex3", "vertex22")
    occupancy_map.add_edge_with_incremental_id("vertex22", "vertex3")

    occupancy_map.add_edge_with_incremental_id("vertex17", "vertex22")
    occupancy_map.add_edge_with_incremental_id("vertex22", "vertex17")

    # 22 to first door connections

    occupancy_map.add_edge_with_incremental_id("vertex12", "vertex22")
    occupancy_map.add_edge_with_incremental_id("vertex22", "vertex12")

    # 23 is in the second room

    occupancy_map.add_edge_with_incremental_id("vertex4", "vertex23")
    occupancy_map.add_edge_with_incremental_id("vertex23", "vertex4")

    occupancy_map.add_edge_with_incremental_id("vertex5", "vertex23")
    occupancy_map.add_edge_with_incremental_id("vertex23", "vertex5")

    occupancy_map.add_edge_with_incremental_id("vertex18", "vertex23")
    occupancy_map.add_edge_with_incremental_id("vertex23", "vertex18")


    # 23 to first door connections

    occupancy_map.add_edge_with_incremental_id("vertex12", "vertex23")
    occupancy_map.add_edge_with_incremental_id("vertex23", "vertex12")


    # 23 to second door connections


    occupancy_map.add_edge_with_incremental_id("vertex13", "vertex23")
    occupancy_map.add_edge_with_incremental_id("vertex23", "vertex13")


    # 23 to third door connections


    occupancy_map.add_edge_with_incremental_id("vertex14", "vertex23")
    occupancy_map.add_edge_with_incremental_id("vertex23", "vertex14")


    # 24 is in the third room

    occupancy_map.add_edge_with_incremental_id("vertex6", "vertex24")
    occupancy_map.add_edge_with_incremental_id("vertex24", "vertex6")
    
    occupancy_map.add_edge_with_incremental_id("vertex7", "vertex24")
    occupancy_map.add_edge_with_incremental_id("vertex24", "vertex7")

    occupancy_map.add_edge_with_incremental_id("vertex19", "vertex24")
    occupancy_map.add_edge_with_incremental_id("vertex24", "vertex19")

    # 24 to second door connections

    occupancy_map.add_edge_with_incremental_id("vertex13", "vertex24")
    occupancy_map.add_edge_with_incremental_id("vertex24", "vertex13")

    # 24 to third door connections

    occupancy_map.add_edge_with_incremental_id("vertex14", "vertex24")
    occupancy_map.add_edge_with_incremental_id("vertex24", "vertex14")

    # 24 to fourth door connections

    occupancy_map.add_edge_with_incremental_id("vertex15", "vertex24")
    occupancy_map.add_edge_with_incremental_id("vertex24", "vertex15")

    # 25 is in the fourth room

    occupancy_map.add_edge_with_incremental_id("vertex8", "vertex25")
    occupancy_map.add_edge_with_incremental_id("vertex25", "vertex8")

    occupancy_map.add_edge_with_incremental_id("vertex9", "vertex25")
    occupancy_map.add_edge_with_incremental_id("vertex25", "vertex9")

    occupancy_map.add_edge_with_incremental_id("vertex20", "vertex25")
    occupancy_map.add_edge_with_incremental_id("vertex25", "vertex20")

    # 25 to fourth door connections

    occupancy_map.add_edge_with_incremental_id("vertex15", "vertex25")
    occupancy_map.add_edge_with_incremental_id("vertex25", "vertex15")

    # 25 to fifth door connections

    occupancy_map.add_edge_with_incremental_id("vertex16", "vertex25")
    occupancy_map.add_edge_with_incremental_id("vertex25", "vertex16")

    # 26 is in the fifth room

    occupancy_map.add_edge_with_incremental_id("vertex10", "vertex26")
    occupancy_map.add_edge_with_incremental_id("vertex26", "vertex10")

    occupancy_map.add_edge_with_incremental_id("vertex11", "vertex26")
    occupancy_map.add_edge_with_incremental_id("vertex26", "vertex11")

    occupancy_map.add_edge_with_incremental_id("vertex21", "vertex26")
    occupancy_map.add_edge_with_incremental_id("vertex26", "vertex21")

    # 26 to fifth door connections

    occupancy_map.add_edge_with_incremental_id("vertex16", "vertex26")
    occupancy_map.add_edge_with_incremental_id("vertex26", "vertex16")



# ---- MADAMA SEQUENTIAL ----



def create_madama_topological_map_sequential_11(occupancy_map):
    create_madama_topological_map_11(occupancy_map)
    occupancy_map.set_name('madama_sequential_11')


def create_madama_topological_map_sequential_16(occupancy_map):
    occupancy_map.set_name('madama_sequential_16')
    occupancy_map.add_vertex_with_id("vertex1", 53.91, 26.05)
    occupancy_map.add_vertex_with_id("vertex2", 50.17, 32.65)
    occupancy_map.add_vertex_with_id("vertex3", 54.12, 32.65)
    occupancy_map.add_vertex_with_id("vertex4", 48.51, 43.02)
    occupancy_map.add_vertex_with_id("vertex5", 50.28, 50.69)
    occupancy_map.add_vertex_with_id("vertex6", 34.24, 41.64)
    occupancy_map.add_vertex_with_id("vertex7", 34.65, 50.53)
    occupancy_map.add_vertex_with_id("vertex8", 18.38, 45.31)
    occupancy_map.add_vertex_with_id("vertex9", 21.84, 41.71)
    occupancy_map.add_vertex_with_id("vertex10", 20.50, 28.87)
    occupancy_map.add_vertex_with_id("vertex11", 24.80, 29.86)
    occupancy_map.add_vertex_with_id("vertex12", 42.92, 51.01)
    occupancy_map.add_vertex_with_id("vertex13", 41.92, 43.24)
    occupancy_map.add_vertex_with_id("vertex14", 27.66, 40.50)
    occupancy_map.add_vertex_with_id("vertex15", 26.6, 48.84)
    occupancy_map.add_vertex_with_id("vertex16", 23.6, 25.9)

    # first room

    occupancy_map.add_edge_with_incremental_id("vertex1", "vertex2")
    occupancy_map.add_edge_with_incremental_id("vertex2", "vertex1")

    occupancy_map.add_edge_with_incremental_id("vertex1", "vertex3")
    occupancy_map.add_edge_with_incremental_id("vertex3", "vertex1")

    occupancy_map.add_edge_with_incremental_id("vertex2", "vertex3")
    occupancy_map.add_edge_with_incremental_id("vertex3", "vertex2")


    # connections first and second room 

    occupancy_map.add_edge_with_incremental_id("vertex2", "vertex4")
    occupancy_map.add_edge_with_incremental_id("vertex4", "vertex2")

    occupancy_map.add_edge_with_incremental_id("vertex2", "vertex5")
    occupancy_map.add_edge_with_incremental_id("vertex5", "vertex2")

    occupancy_map.add_edge_with_incremental_id("vertex3", "vertex4")
    occupancy_map.add_edge_with_incremental_id("vertex4", "vertex3")

    occupancy_map.add_edge_with_incremental_id("vertex3", "vertex5")
    occupancy_map.add_edge_with_incremental_id("vertex5", "vertex3")

    # second room

    occupancy_map.add_edge_with_incremental_id("vertex4", "vertex5")
    occupancy_map.add_edge_with_incremental_id("vertex5", "vertex4")

    # connections second and third room

    occupancy_map.add_edge_with_incremental_id("vertex4", "vertex12")
    occupancy_map.add_edge_with_incremental_id("vertex12", "vertex4")

    occupancy_map.add_edge_with_incremental_id("vertex5", "vertex12")
    occupancy_map.add_edge_with_incremental_id("vertex12", "vertex5")

    occupancy_map.add_edge_with_incremental_id("vertex4", "vertex13")
    occupancy_map.add_edge_with_incremental_id("vertex13", "vertex4")

    occupancy_map.add_edge_with_incremental_id("vertex5", "vertex13")
    occupancy_map.add_edge_with_incremental_id("vertex13", "vertex5")

    # third room

    occupancy_map.add_edge_with_incremental_id("vertex12", "vertex13")
    occupancy_map.add_edge_with_incremental_id("vertex13", "vertex12")

    occupancy_map.add_edge_with_incremental_id("vertex12", "vertex6")
    occupancy_map.add_edge_with_incremental_id("vertex6", "vertex12")

    occupancy_map.add_edge_with_incremental_id("vertex13", "vertex6")
    occupancy_map.add_edge_with_incremental_id("vertex6", "vertex13")

    occupancy_map.add_edge_with_incremental_id("vertex12", "vertex7")
    occupancy_map.add_edge_with_incremental_id("vertex7", "vertex12")

    occupancy_map.add_edge_with_incremental_id("vertex13", "vertex7")
    occupancy_map.add_edge_with_incremental_id("vertex7", "vertex13")

    occupancy_map.add_edge_with_incremental_id("vertex6", "vertex7")
    occupancy_map.add_edge_with_incremental_id("vertex7", "vertex6")

    occupancy_map.add_edge_with_incremental_id("vertex6", "vertex14")
    occupancy_map.add_edge_with_incremental_id("vertex14", "vertex6")

    occupancy_map.add_edge_with_incremental_id("vertex7", "vertex14")
    occupancy_map.add_edge_with_incremental_id("vertex14", "vertex7")

    occupancy_map.add_edge_with_incremental_id("vertex6", "vertex15")
    occupancy_map.add_edge_with_incremental_id("vertex15", "vertex6")

    occupancy_map.add_edge_with_incremental_id("vertex7", "vertex15")
    occupancy_map.add_edge_with_incremental_id("vertex15", "vertex7")

    # connections third and fourth room

    occupancy_map.add_edge_with_incremental_id("vertex14", "vertex8")
    occupancy_map.add_edge_with_incremental_id("vertex8", "vertex14")

    occupancy_map.add_edge_with_incremental_id("vertex14", "vertex9")
    occupancy_map.add_edge_with_incremental_id("vertex9", "vertex14")

    occupancy_map.add_edge_with_incremental_id("vertex15", "vertex8")
    occupancy_map.add_edge_with_incremental_id("vertex8", "vertex15")

    occupancy_map.add_edge_with_incremental_id("vertex15", "vertex9")
    occupancy_map.add_edge_with_incremental_id("vertex9", "vertex15")


    # fourth room

    occupancy_map.add_edge_with_incremental_id("vertex8", "vertex9")
    occupancy_map.add_edge_with_incremental_id("vertex9", "vertex8")

    # connections fourth and fifth room

    occupancy_map.add_edge_with_incremental_id("vertex8", "vertex10")
    occupancy_map.add_edge_with_incremental_id("vertex10", "vertex8")

    occupancy_map.add_edge_with_incremental_id("vertex8", "vertex11")
    occupancy_map.add_edge_with_incremental_id("vertex11", "vertex8")

    occupancy_map.add_edge_with_incremental_id("vertex9", "vertex10")
    occupancy_map.add_edge_with_incremental_id("vertex10", "vertex9")

    occupancy_map.add_edge_with_incremental_id("vertex9", "vertex11")
    occupancy_map.add_edge_with_incremental_id("vertex11", "vertex9")

    # fifth room

    occupancy_map.add_edge_with_incremental_id("vertex10", "vertex11")
    occupancy_map.add_edge_with_incremental_id("vertex11", "vertex10")

    occupancy_map.add_edge_with_incremental_id("vertex10", "vertex16")
    occupancy_map.add_edge_with_incremental_id("vertex16", "vertex10")

    occupancy_map.add_edge_with_incremental_id("vertex11", "vertex16")
    occupancy_map.add_edge_with_incremental_id("vertex16", "vertex11")


def create_madama_topological_map_sequential_21(occupancy_map):
    occupancy_map.add_vertex_with_id("vertex1", 53.91, 26.05)
    occupancy_map.add_vertex_with_id("vertex2", 50.17, 32.65)
    occupancy_map.add_vertex_with_id("vertex3", 54.12, 32.65)
    occupancy_map.add_vertex_with_id("vertex4", 48.51, 43.02)
    occupancy_map.add_vertex_with_id("vertex5", 50.28, 50.69)
    occupancy_map.add_vertex_with_id("vertex6", 34.24, 41.64)
    occupancy_map.add_vertex_with_id("vertex7", 34.65, 50.53)
    occupancy_map.add_vertex_with_id("vertex8", 18.38, 45.31)
    occupancy_map.add_vertex_with_id("vertex9", 21.84, 41.71)
    occupancy_map.add_vertex_with_id("vertex10", 20.50, 28.87)
    occupancy_map.add_vertex_with_id("vertex11", 24.80, 29.86)
    occupancy_map.add_vertex_with_id("vertex12", 42.92, 51.01)
    occupancy_map.add_vertex_with_id("vertex13", 41.92, 43.24)
    occupancy_map.add_vertex_with_id("vertex14", 27.66, 40.50)
    occupancy_map.add_vertex_with_id("vertex15", 26.6, 48.84)
    occupancy_map.add_vertex_with_id("vertex16", 23.6, 25.9)
    occupancy_map.add_vertex_with_id("vertex17", 49.20, 37.17) 
    occupancy_map.add_vertex_with_id("vertex18", 54.82, 37.35)
    occupancy_map.add_vertex_with_id("vertex19", 53.98, 42.86)
    occupancy_map.add_vertex_with_id("vertex20", 23.34,35.5)
    occupancy_map.add_vertex_with_id("vertex21", 19.12, 35.2)


    occupancy_map.set_name('madama_sequential_21')

    # first room

    occupancy_map.add_edge_with_incremental_id("vertex1", "vertex2")
    occupancy_map.add_edge_with_incremental_id("vertex2", "vertex1")

    occupancy_map.add_edge_with_incremental_id("vertex1", "vertex3")
    occupancy_map.add_edge_with_incremental_id("vertex3", "vertex1")

    occupancy_map.add_edge_with_incremental_id("vertex2", "vertex3")
    occupancy_map.add_edge_with_incremental_id("vertex3", "vertex2")

    occupancy_map.add_edge_with_incremental_id("vertex2", "vertex17")
    occupancy_map.add_edge_with_incremental_id("vertex17", "vertex2")

    occupancy_map.add_edge_with_incremental_id("vertex3", "vertex17")
    occupancy_map.add_edge_with_incremental_id("vertex17", "vertex3")

    occupancy_map.add_edge_with_incremental_id("vertex2", "vertex18")
    occupancy_map.add_edge_with_incremental_id("vertex18", "vertex2")

    occupancy_map.add_edge_with_incremental_id("vertex3", "vertex18")
    occupancy_map.add_edge_with_incremental_id("vertex18", "vertex3")

    occupancy_map.add_edge_with_incremental_id("vertex17", "vertex18")
    occupancy_map.add_edge_with_incremental_id("vertex18", "vertex17")

    # connections first and second room

    occupancy_map.add_edge_with_incremental_id("vertex17", "vertex4")
    occupancy_map.add_edge_with_incremental_id("vertex4", "vertex17")

    occupancy_map.add_edge_with_incremental_id("vertex17", "vertex19")
    occupancy_map.add_edge_with_incremental_id("vertex19", "vertex17")

    occupancy_map.add_edge_with_incremental_id("vertex18", "vertex4")
    occupancy_map.add_edge_with_incremental_id("vertex4", "vertex18")

    occupancy_map.add_edge_with_incremental_id("vertex18", "vertex19")
    occupancy_map.add_edge_with_incremental_id("vertex19", "vertex18")

    # second room

    occupancy_map.add_edge_with_incremental_id("vertex4", "vertex5")
    occupancy_map.add_edge_with_incremental_id("vertex5", "vertex4")

    occupancy_map.add_edge_with_incremental_id("vertex4", "vertex19")
    occupancy_map.add_edge_with_incremental_id("vertex19", "vertex4")

    occupancy_map.add_edge_with_incremental_id("vertex5", "vertex19")
    occupancy_map.add_edge_with_incremental_id("vertex19", "vertex5")

    # connections second and third room

    occupancy_map.add_edge_with_incremental_id("vertex4", "vertex12")
    occupancy_map.add_edge_with_incremental_id("vertex12", "vertex4")

    occupancy_map.add_edge_with_incremental_id("vertex5", "vertex12")
    occupancy_map.add_edge_with_incremental_id("vertex12", "vertex5")

    occupancy_map.add_edge_with_incremental_id("vertex4", "vertex13")
    occupancy_map.add_edge_with_incremental_id("vertex13", "vertex4")

    occupancy_map.add_edge_with_incremental_id("vertex5", "vertex13")
    occupancy_map.add_edge_with_incremental_id("vertex13", "vertex5")

    # third room

    occupancy_map.add_edge_with_incremental_id("vertex12", "vertex13")
    occupancy_map.add_edge_with_incremental_id("vertex13", "vertex12")

    occupancy_map.add_edge_with_incremental_id("vertex12", "vertex6")
    occupancy_map.add_edge_with_incremental_id("vertex6", "vertex12")

    occupancy_map.add_edge_with_incremental_id("vertex13", "vertex6")
    occupancy_map.add_edge_with_incremental_id("vertex6", "vertex13")

    occupancy_map.add_edge_with_incremental_id("vertex12", "vertex7")
    occupancy_map.add_edge_with_incremental_id("vertex7", "vertex12")

    occupancy_map.add_edge_with_incremental_id("vertex13", "vertex7")
    occupancy_map.add_edge_with_incremental_id("vertex7", "vertex13")

    occupancy_map.add_edge_with_incremental_id("vertex6", "vertex7")
    occupancy_map.add_edge_with_incremental_id("vertex7", "vertex6")

    occupancy_map.add_edge_with_incremental_id("vertex6", "vertex14")
    occupancy_map.add_edge_with_incremental_id("vertex14", "vertex6")

    occupancy_map.add_edge_with_incremental_id("vertex7", "vertex14")
    occupancy_map.add_edge_with_incremental_id("vertex14", "vertex7")

    occupancy_map.add_edge_with_incremental_id("vertex6", "vertex15")
    occupancy_map.add_edge_with_incremental_id("vertex15", "vertex6")

    occupancy_map.add_edge_with_incremental_id("vertex7", "vertex15")
    occupancy_map.add_edge_with_incremental_id("vertex15", "vertex7")

    occupancy_map.add_edge_with_incremental_id("vertex14", "vertex15")
    occupancy_map.add_edge_with_incremental_id("vertex15", "vertex14")

    # connections third and fourth room

    occupancy_map.add_edge_with_incremental_id("vertex14", "vertex8")
    occupancy_map.add_edge_with_incremental_id("vertex8", "vertex14")

    occupancy_map.add_edge_with_incremental_id("vertex14", "vertex9")
    occupancy_map.add_edge_with_incremental_id("vertex9", "vertex14")

    occupancy_map.add_edge_with_incremental_id("vertex15", "vertex8")
    occupancy_map.add_edge_with_incremental_id("vertex8", "vertex15")

    occupancy_map.add_edge_with_incremental_id("vertex15", "vertex9")
    occupancy_map.add_edge_with_incremental_id("vertex9", "vertex15")

    # fourth room

    occupancy_map.add_edge_with_incremental_id("vertex8", "vertex9")
    occupancy_map.add_edge_with_incremental_id("vertex9", "vertex8")

    # connections fourth and fifth room

    occupancy_map.add_edge_with_incremental_id("vertex8", "vertex20")
    occupancy_map.add_edge_with_incremental_id("vertex20", "vertex8")

    occupancy_map.add_edge_with_incremental_id("vertex8", "vertex21")
    occupancy_map.add_edge_with_incremental_id("vertex21", "vertex8")

    occupancy_map.add_edge_with_incremental_id("vertex9", "vertex20")
    occupancy_map.add_edge_with_incremental_id("vertex20", "vertex9")

    occupancy_map.add_edge_with_incremental_id("vertex9", "vertex21")
    occupancy_map.add_edge_with_incremental_id("vertex21", "vertex9")

    # fifth room

    occupancy_map.add_edge_with_incremental_id("vertex20", "vertex21")
    occupancy_map.add_edge_with_incremental_id("vertex21", "vertex20")

    occupancy_map.add_edge_with_incremental_id("vertex20", "vertex10")
    occupancy_map.add_edge_with_incremental_id("vertex10", "vertex20")

    occupancy_map.add_edge_with_incremental_id("vertex21", "vertex10")
    occupancy_map.add_edge_with_incremental_id("vertex10", "vertex21")

    occupancy_map.add_edge_with_incremental_id("vertex20", "vertex11")
    occupancy_map.add_edge_with_incremental_id("vertex11", "vertex20")

    occupancy_map.add_edge_with_incremental_id("vertex21", "vertex11")
    occupancy_map.add_edge_with_incremental_id("vertex11", "vertex21")

    occupancy_map.add_edge_with_incremental_id("vertex10", "vertex11")
    occupancy_map.add_edge_with_incremental_id("vertex11", "vertex10")

    occupancy_map.add_edge_with_incremental_id("vertex10", "vertex16")
    occupancy_map.add_edge_with_incremental_id("vertex16", "vertex10")

    occupancy_map.add_edge_with_incremental_id("vertex11", "vertex16")
    occupancy_map.add_edge_with_incremental_id("vertex16", "vertex11")


def create_madama_topological_map_sequential_26(occupancy_map):

    occupancy_map.add_vertex_with_id("vertex1", 53.91, 26.05)
    occupancy_map.add_vertex_with_id("vertex2", 50.17, 32.65)
    occupancy_map.add_vertex_with_id("vertex3", 54.12, 32.65)
    occupancy_map.add_vertex_with_id("vertex4", 48.51, 43.02)
    occupancy_map.add_vertex_with_id("vertex5", 50.28, 50.69)
    occupancy_map.add_vertex_with_id("vertex6", 34.24, 41.64)
    occupancy_map.add_vertex_with_id("vertex7", 34.65, 50.53)
    occupancy_map.add_vertex_with_id("vertex8", 18.38, 45.31)
    occupancy_map.add_vertex_with_id("vertex9", 21.84, 41.71)
    occupancy_map.add_vertex_with_id("vertex10", 20.50, 28.87)
    occupancy_map.add_vertex_with_id("vertex11", 24.80, 29.86)
    occupancy_map.add_vertex_with_id("vertex12", 42.92, 51.01)
    occupancy_map.add_vertex_with_id("vertex13", 41.92, 43.24)
    occupancy_map.add_vertex_with_id("vertex14", 27.66, 40.50)
    occupancy_map.add_vertex_with_id("vertex15", 26.6, 48.84)
    occupancy_map.add_vertex_with_id("vertex16", 23.6, 25.9)
    occupancy_map.add_vertex_with_id("vertex17", 49.20, 37.17) 
    occupancy_map.add_vertex_with_id("vertex18", 54.82, 37.35)
    occupancy_map.add_vertex_with_id("vertex19", 53.98, 42.86)
    occupancy_map.add_vertex_with_id("vertex20", 23.34,35.5)
    occupancy_map.add_vertex_with_id("vertex21", 19.12, 35.2)
    occupancy_map.add_vertex_with_id("vertex22", 54.35, 49.00)
    occupancy_map.add_vertex_with_id("vertex23", 34.25, 45.92)
    occupancy_map.add_vertex_with_id("vertex24", 20.9, 48.0)
    occupancy_map.add_vertex_with_id("vertex25", 22.07, 32.4)
    occupancy_map.add_vertex_with_id("vertex26", 52.0, 34.1)
    occupancy_map.set_name('madama_sequential_26')

    # first room

    occupancy_map.add_edge_with_incremental_id("vertex1", "vertex2")
    occupancy_map.add_edge_with_incremental_id("vertex2", "vertex1")

    occupancy_map.add_edge_with_incremental_id("vertex1", "vertex3")
    occupancy_map.add_edge_with_incremental_id("vertex3", "vertex1")

    occupancy_map.add_edge_with_incremental_id("vertex2", "vertex3")
    occupancy_map.add_edge_with_incremental_id("vertex3", "vertex2")

    occupancy_map.add_edge_with_incremental_id("vertex1", "vertex26")
    occupancy_map.add_edge_with_incremental_id("vertex26", "vertex1")

    occupancy_map.add_edge_with_incremental_id("vertex2", "vertex26")
    occupancy_map.add_edge_with_incremental_id("vertex26", "vertex2")

    occupancy_map.add_edge_with_incremental_id("vertex3", "vertex26")
    occupancy_map.add_edge_with_incremental_id("vertex26", "vertex3")

    occupancy_map.add_edge_with_incremental_id("vertex2", "vertex17")
    occupancy_map.add_edge_with_incremental_id("vertex17", "vertex2")

    # occupancy_map.add_edge_with_incremental_id("vertex3", "vertex17")
    # occupancy_map.add_edge_with_incremental_id("vertex17", "vertex3")

    # occupancy_map.add_edge_with_incremental_id("vertex2", "vertex18")
    # occupancy_map.add_edge_with_incremental_id("vertex18", "vertex2")

    occupancy_map.add_edge_with_incremental_id("vertex3", "vertex18")
    occupancy_map.add_edge_with_incremental_id("vertex18", "vertex3")

    occupancy_map.add_edge_with_incremental_id("vertex17", "vertex18")
    occupancy_map.add_edge_with_incremental_id("vertex18", "vertex17")

    occupancy_map.add_edge_with_incremental_id("vertex17", "vertex26")
    occupancy_map.add_edge_with_incremental_id("vertex26", "vertex17")

    occupancy_map.add_edge_with_incremental_id("vertex18", "vertex26")
    occupancy_map.add_edge_with_incremental_id("vertex26", "vertex18")

    # connections first and second room

    occupancy_map.add_edge_with_incremental_id("vertex17", "vertex4")
    occupancy_map.add_edge_with_incremental_id("vertex4", "vertex17")

    occupancy_map.add_edge_with_incremental_id("vertex17", "vertex19")
    occupancy_map.add_edge_with_incremental_id("vertex19", "vertex17")

    occupancy_map.add_edge_with_incremental_id("vertex18", "vertex4")
    occupancy_map.add_edge_with_incremental_id("vertex4", "vertex18")

    occupancy_map.add_edge_with_incremental_id("vertex18", "vertex19")
    occupancy_map.add_edge_with_incremental_id("vertex19", "vertex18")

    occupancy_map.add_edge_with_incremental_id("vertex26", "vertex4")
    occupancy_map.add_edge_with_incremental_id("vertex4", "vertex26")

    occupancy_map.add_edge_with_incremental_id("vertex26", "vertex19")
    occupancy_map.add_edge_with_incremental_id("vertex19", "vertex26")

    # second room

    occupancy_map.add_edge_with_incremental_id("vertex4", "vertex5")
    occupancy_map.add_edge_with_incremental_id("vertex5", "vertex4")

    occupancy_map.add_edge_with_incremental_id("vertex4", "vertex19")
    occupancy_map.add_edge_with_incremental_id("vertex19", "vertex4")

    occupancy_map.add_edge_with_incremental_id("vertex5", "vertex19")
    occupancy_map.add_edge_with_incremental_id("vertex19", "vertex5")

    occupancy_map.add_edge_with_incremental_id("vertex4", "vertex22")
    occupancy_map.add_edge_with_incremental_id("vertex22", "vertex4")

    occupancy_map.add_edge_with_incremental_id("vertex5", "vertex22")
    occupancy_map.add_edge_with_incremental_id("vertex22", "vertex5")

    occupancy_map.add_edge_with_incremental_id("vertex19", "vertex22")
    occupancy_map.add_edge_with_incremental_id("vertex22", "vertex19")

    # connections second and third room

    occupancy_map.add_edge_with_incremental_id("vertex4", "vertex12")
    occupancy_map.add_edge_with_incremental_id("vertex12", "vertex4")

    occupancy_map.add_edge_with_incremental_id("vertex5", "vertex12")
    occupancy_map.add_edge_with_incremental_id("vertex12", "vertex5")

    occupancy_map.add_edge_with_incremental_id("vertex4", "vertex13")
    occupancy_map.add_edge_with_incremental_id("vertex13", "vertex4")

    occupancy_map.add_edge_with_incremental_id("vertex5", "vertex13")
    occupancy_map.add_edge_with_incremental_id("vertex13", "vertex5")

    # third room

    occupancy_map.add_edge_with_incremental_id("vertex12", "vertex13")
    occupancy_map.add_edge_with_incremental_id("vertex13", "vertex12")

    occupancy_map.add_edge_with_incremental_id("vertex12", "vertex6")
    occupancy_map.add_edge_with_incremental_id("vertex6", "vertex12")

    occupancy_map.add_edge_with_incremental_id("vertex13", "vertex6")
    occupancy_map.add_edge_with_incremental_id("vertex6", "vertex13")

    occupancy_map.add_edge_with_incremental_id("vertex12", "vertex7")
    occupancy_map.add_edge_with_incremental_id("vertex7", "vertex12")

    occupancy_map.add_edge_with_incremental_id("vertex13", "vertex7")
    occupancy_map.add_edge_with_incremental_id("vertex7", "vertex13")

    occupancy_map.add_edge_with_incremental_id("vertex12", "vertex23")
    occupancy_map.add_edge_with_incremental_id("vertex23", "vertex12")

    occupancy_map.add_edge_with_incremental_id("vertex13", "vertex23")
    occupancy_map.add_edge_with_incremental_id("vertex23", "vertex13")

    occupancy_map.add_edge_with_incremental_id("vertex6", "vertex23")
    occupancy_map.add_edge_with_incremental_id("vertex23", "vertex6")

    occupancy_map.add_edge_with_incremental_id("vertex7", "vertex23")
    occupancy_map.add_edge_with_incremental_id("vertex23", "vertex7")

    occupancy_map.add_edge_with_incremental_id("vertex6", "vertex14")
    occupancy_map.add_edge_with_incremental_id("vertex14", "vertex6")

    occupancy_map.add_edge_with_incremental_id("vertex7", "vertex14")
    occupancy_map.add_edge_with_incremental_id("vertex14", "vertex7")

    occupancy_map.add_edge_with_incremental_id("vertex6", "vertex15")
    occupancy_map.add_edge_with_incremental_id("vertex15", "vertex6")

    occupancy_map.add_edge_with_incremental_id("vertex7", "vertex15")
    occupancy_map.add_edge_with_incremental_id("vertex15", "vertex7")

    occupancy_map.add_edge_with_incremental_id("vertex14", "vertex23")
    occupancy_map.add_edge_with_incremental_id("vertex23", "vertex14")

    occupancy_map.add_edge_with_incremental_id("vertex15", "vertex23")
    occupancy_map.add_edge_with_incremental_id("vertex23", "vertex15")

    occupancy_map.add_edge_with_incremental_id("vertex14", "vertex15")
    occupancy_map.add_edge_with_incremental_id("vertex15", "vertex14")

    # connections third and fourth room

    occupancy_map.add_edge_with_incremental_id("vertex14", "vertex24")
    occupancy_map.add_edge_with_incremental_id("vertex24", "vertex14")

    occupancy_map.add_edge_with_incremental_id("vertex14", "vertex9")
    occupancy_map.add_edge_with_incremental_id("vertex9", "vertex14")

    occupancy_map.add_edge_with_incremental_id("vertex15", "vertex24")
    occupancy_map.add_edge_with_incremental_id("vertex24", "vertex15")

    occupancy_map.add_edge_with_incremental_id("vertex15", "vertex9")
    occupancy_map.add_edge_with_incremental_id("vertex9", "vertex15")

    # fourth room

    occupancy_map.add_edge_with_incremental_id("vertex8", "vertex24")
    occupancy_map.add_edge_with_incremental_id("vertex24", "vertex8")

    occupancy_map.add_edge_with_incremental_id("vertex9", "vertex24")
    occupancy_map.add_edge_with_incremental_id("vertex24", "vertex9")

    occupancy_map.add_edge_with_incremental_id("vertex8", "vertex9")
    occupancy_map.add_edge_with_incremental_id("vertex9", "vertex8")

    # connections fourth and fifth room

    occupancy_map.add_edge_with_incremental_id("vertex8", "vertex20")
    occupancy_map.add_edge_with_incremental_id("vertex20", "vertex8")

    occupancy_map.add_edge_with_incremental_id("vertex8", "vertex21")
    occupancy_map.add_edge_with_incremental_id("vertex21", "vertex8")

    occupancy_map.add_edge_with_incremental_id("vertex9", "vertex20")
    occupancy_map.add_edge_with_incremental_id("vertex20", "vertex9")

    occupancy_map.add_edge_with_incremental_id("vertex9", "vertex21")
    occupancy_map.add_edge_with_incremental_id("vertex21", "vertex9")

    # fifth room

    occupancy_map.add_edge_with_incremental_id("vertex20", "vertex21")
    occupancy_map.add_edge_with_incremental_id("vertex21", "vertex20")

    occupancy_map.add_edge_with_incremental_id("vertex20", "vertex25")
    occupancy_map.add_edge_with_incremental_id("vertex25", "vertex20")

    occupancy_map.add_edge_with_incremental_id("vertex20", "vertex11")
    occupancy_map.add_edge_with_incremental_id("vertex11", "vertex20")


    occupancy_map.add_edge_with_incremental_id("vertex21", "vertex10")
    occupancy_map.add_edge_with_incremental_id("vertex10", "vertex21")

    occupancy_map.add_edge_with_incremental_id("vertex21", "vertex25")
    occupancy_map.add_edge_with_incremental_id("vertex25", "vertex21")

    occupancy_map.add_edge_with_incremental_id("vertex10", "vertex11")
    occupancy_map.add_edge_with_incremental_id("vertex11", "vertex10")

    occupancy_map.add_edge_with_incremental_id("vertex10", "vertex25")
    occupancy_map.add_edge_with_incremental_id("vertex25", "vertex10")

    occupancy_map.add_edge_with_incremental_id("vertex11", "vertex25")
    occupancy_map.add_edge_with_incremental_id("vertex25", "vertex11")

    occupancy_map.add_edge_with_incremental_id("vertex10", "vertex16")
    occupancy_map.add_edge_with_incremental_id("vertex16", "vertex10")

    occupancy_map.add_edge_with_incremental_id("vertex11", "vertex16")
    occupancy_map.add_edge_with_incremental_id("vertex16", "vertex11")

    occupancy_map.add_edge_with_incremental_id("vertex25", "vertex16")
    occupancy_map.add_edge_with_incremental_id("vertex16", "vertex25")



def get_times_madama():
    # read the file times_higher_7_madama.csv and put into a list
    filename = 'times_higher_7_madama.csv'
    time_list = []
    with open(filename) as f:
        for line in f:
            time_list.append(float(line.strip()))
    return time_list


def create_occupancy_map(occupancy_map, level, topological_map_creator_function, num_iterations=3000):
    topological_map_creator_function(occupancy_map)
    edges = occupancy_map.get_edges()
    for edge_key in edges:
        occupancy_map.add_edge_limit(edges[edge_key].get_id(), level)
    occupancy_map.calculate_average_edge_traverse_times(num_iterations)
    folder = 'data/occupancy_maps_' + occupancy_map.get_name()
    utils.create_folder(folder)

    filename = folder + '/occupancy_map_' + occupancy_map.get_name() + "_" + str(len(level))+'_levels.yaml'
    occupancy_map.save_occupancy_map(filename)



# def create_occupancy_map_madama(occupancy_map, level, topological_map_creator_function, num_iterations=1000):
#     topological_map_creator_function(occupancy_map)
#     edges = occupancy_map.get_edges()
#     for edge_key in edges:
#         occupancy_map.add_edge_limit(edges[edge_key].get_id(), level)
#     occupancy_map.calculate_average_edge_traverse_times(num_iterations)
#     folder = 'data/occupancy_maps_' + occupancy_map.get_name()
#     utils.create_folder(folder)

#     filename = folder + '/occupancy_map_' + occupancy_map.get_name() + "_" + str(len(level))+'_levels.yaml'
#     occupancy_map.save_occupancy_map(filename)


if __name__ == "__main__":
    # print(matrix)
    warnings.filterwarnings("ignore")
    predictor = create_atc_cliff_predictor()
    predictor_madama = create_madama_cliff_predictor()
    # topological_map_creator_function = [create_large_topological_map_atc_corridor, create_medium_large_topological_map_atc_corridor]
    topological_map_creator_function = [create_topological_map_atc_corridor_21, create_topological_map_atc_corridor_16, create_topological_map_atc_corridor_11]
    # topological_map_creator_function = [create_large_topological_map_atc_corridor, create_medium_topological_map_atc_corridor, create_small_topological_map_atc_corridor,
    #                                      create_large_topological_map_atc_square, create_medium_topological_map_atc_square]
    # topological_map_creator_function_madama = [create_madama_topological_map_26, create_madama_topological_map_21, create_madama_topological_map_16, create_madama_topological_map_11]
    topological_map_creator_function_madama_doors = [ create_madama_topological_map_doors_26, create_madama_topological_map_doors_21, create_madama_topological_map_doors_16]
    topological_map_creator_function_madama = [ create_madama_topological_map_26, create_madama_topological_map_21, create_madama_topological_map_16, create_madama_topological_map_11]
    topological_map_creator_function_madama_sequential = [create_madama_topological_map_sequential_26, create_madama_topological_map_sequential_21, create_madama_topological_map_sequential_16, create_madama_topological_map_sequential_11]
    # two levels
    occupancy_levels = [(["zero", "one"], {"zero": [0,1], "one": [1,9999999]}),
                        (["zero", "one", "two"], {"zero": [0,1], "one": [1,3], "two": [3,9999999]}),
                        (["zero", "one", "two", "three"], {"zero": [0,1], "one": [1,3], "two": [3,6], "three": [6,9999999]}),
                        (["zero", "one", "two", "three", "four"], {"zero": [0,1], "one": [1,3], "two": [3,5], "three": [5,7], "four": [7,9999999]}),
                        (["zero", "one", "two", "three", "four", "five"], {"zero": [0,1], "one": [1,3], "two": [3,5], "three": [5,7], "four": [7,9], "five": [9,9999999]}),
                        (["zero", "one", "two", "three", "four", "five", "six"], {"zero": [0,1], "one": [1,3], "two": [3,5], "three": [5,7], "four": [7,9], "five": [9,12], "six": [12,9999999]}),
                        (["zero", "one", "two", "three", "four", "five", "six", "seven"], {"zero": [0,1], "one": [1,2], "two": [2,3], "three": [3,4], "four": [4,5], "five": [5,6], "six": [6,7], "seven": [7,9999999]})
                        ]



    for function_name in topological_map_creator_function_madama_sequential:
        for levels in occupancy_levels:
            occupancy_map = OccupancyMap(predictor_madama, levels[0])
            create_occupancy_map(occupancy_map, levels[1], function_name, 3000)
            # occupancy_map.plot_topological_map(predictor_madama.map_file, predictor_madama.fig_size, occupancy_map.get_name(), show_vertex_names=True)
            # occupancy_map.display_topological_map()

    # for levels in  occupancy_levels:  # just two levels
    #     for vertex_number in [26]:
    #         occupancy_map = OccupancyMap(predictor, levels[0])
    #         function_name_map = globals()[f'create_topological_map_atc_corridor_{vertex_number}']
    #         create_occupancy_map_atc(occupancy_map, levels[1], function_name_map)
            # occupancy_map.plot_topological_map(predictor.map_file, predictor.fig_size, occupancy_map.get_name())
