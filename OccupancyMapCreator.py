from OccupancyMap import OccupancyMap
import utils
import matplotlib.pyplot as plt
import csv
from cliff_predictor import CliffPredictor
from PredictorCreator import create_atc_cliff_predictor,  create_madama_cliff_predictor
import warnings

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


def create_topological_map_atc_corridor_19(occupancy_map):
    occupancy_map.set_name('large_atc_corridor_19')
    occupancy_map.add_vertex_with_id("vertex1", 50.55, -26.44)
    occupancy_map.add_vertex_with_id("vertex2", 40.03, -18.72)
    occupancy_map.add_vertex_with_id("vertex3", 34.15, -17.47)
    occupancy_map.add_vertex_with_id("vertex4", 21.91, -16.2)
    occupancy_map.add_vertex_with_id("vertex5", 27.88, -18.22)
    occupancy_map.add_vertex_with_id("vertex6", 35.64, -21.17)
    occupancy_map.add_vertex_with_id("vertex7", 27.0, -15.14)
    occupancy_map.add_vertex_with_id("vertex8", 19.79, -13.51)
    occupancy_map.add_vertex_with_id("vertex9", 41.46, -21.41)
    occupancy_map.add_vertex_with_id("vertex10", 31.7, -18.0)
    occupancy_map.add_vertex_with_id("vertex11", 24.71, -16.0)
    occupancy_map.add_vertex_with_id("vertex12", 42.88, -24.13)
    occupancy_map.add_vertex_with_id("vertex13", 52.28, -23.13)
    occupancy_map.add_vertex_with_id("vertex14", 47.14, -20.26)
    occupancy_map.add_vertex_with_id("vertex17", 20.6, -9.38)
    occupancy_map.add_vertex_with_id("vertex18", 16.59, -9.92)
    occupancy_map.add_vertex_with_id("vertex19", 11.28, -8.67)




    occupancy_map.add_edge_with_incremental_id("vertex1", "vertex12")
    occupancy_map.add_edge_with_incremental_id("vertex1", "vertex13")
    occupancy_map.add_edge_with_incremental_id("vertex1", "vertex14")

    occupancy_map.add_edge_with_incremental_id("vertex12", "vertex1")
    occupancy_map.add_edge_with_incremental_id("vertex13", "vertex1")
    occupancy_map.add_edge_with_incremental_id("vertex14", "vertex1")

# ----------------------------

    occupancy_map.add_edge_with_incremental_id("vertex2", "vertex3")
    occupancy_map.add_edge_with_incremental_id("vertex2", "vertex6")
    occupancy_map.add_edge_with_incremental_id("vertex2", "vertex9")
    occupancy_map.add_edge_with_incremental_id("vertex2", "vertex12")
    occupancy_map.add_edge_with_incremental_id("vertex2", "vertex14")

    occupancy_map.add_edge_with_incremental_id("vertex3", "vertex2")
    occupancy_map.add_edge_with_incremental_id("vertex6", "vertex2")
    occupancy_map.add_edge_with_incremental_id("vertex9", "vertex2")
    occupancy_map.add_edge_with_incremental_id("vertex12", "vertex2")
    occupancy_map.add_edge_with_incremental_id("vertex14", "vertex2")

# ----------------------------

    occupancy_map.add_edge_with_incremental_id("vertex3", "vertex6")
    occupancy_map.add_edge_with_incremental_id("vertex3", "vertex7")
    occupancy_map.add_edge_with_incremental_id("vertex3", "vertex9")
    occupancy_map.add_edge_with_incremental_id("vertex3", "vertex10")

    occupancy_map.add_edge_with_incremental_id("vertex6", "vertex3")
    occupancy_map.add_edge_with_incremental_id("vertex7", "vertex3")
    occupancy_map.add_edge_with_incremental_id("vertex9", "vertex3")
    occupancy_map.add_edge_with_incremental_id("vertex10", "vertex3")

# ----------------------------

    occupancy_map.add_edge_with_incremental_id("vertex4", "vertex5")
    occupancy_map.add_edge_with_incremental_id("vertex4", "vertex8")
    occupancy_map.add_edge_with_incremental_id("vertex4", "vertex11")
    occupancy_map.add_edge_with_incremental_id("vertex4", "vertex15")

    occupancy_map.add_edge_with_incremental_id("vertex5", "vertex4")
    occupancy_map.add_edge_with_incremental_id("vertex8", "vertex4")
    occupancy_map.add_edge_with_incremental_id("vertex11", "vertex4")
    occupancy_map.add_edge_with_incremental_id("vertex15", "vertex4")

# ----------------------------

    occupancy_map.add_edge_with_incremental_id("vertex5", "vertex6")
    occupancy_map.add_edge_with_incremental_id("vertex5", "vertex7")
    occupancy_map.add_edge_with_incremental_id("vertex5", "vertex10")
    occupancy_map.add_edge_with_incremental_id("vertex5", "vertex11")

    occupancy_map.add_edge_with_incremental_id("vertex6", "vertex5")
    occupancy_map.add_edge_with_incremental_id("vertex7", "vertex5")
    occupancy_map.add_edge_with_incremental_id("vertex10", "vertex5")
    occupancy_map.add_edge_with_incremental_id("vertex11", "vertex5")

# ----------------------------

    occupancy_map.add_edge_with_incremental_id("vertex6", "vertex9")
    occupancy_map.add_edge_with_incremental_id("vertex6", "vertex10")
    occupancy_map.add_edge_with_incremental_id("vertex6", "vertex12")

    occupancy_map.add_edge_with_incremental_id("vertex9", "vertex6")
    occupancy_map.add_edge_with_incremental_id("vertex10", "vertex6")
    occupancy_map.add_edge_with_incremental_id("vertex12", "vertex6")

# ----------------------------

    occupancy_map.add_edge_with_incremental_id("vertex7", "vertex8")
    occupancy_map.add_edge_with_incremental_id("vertex7", "vertex10")
    occupancy_map.add_edge_with_incremental_id("vertex7", "vertex11")
    occupancy_map.add_edge_with_incremental_id("vertex7", "vertex16")

    occupancy_map.add_edge_with_incremental_id("vertex8", "vertex7")
    occupancy_map.add_edge_with_incremental_id("vertex10", "vertex7")
    occupancy_map.add_edge_with_incremental_id("vertex11", "vertex7")
    occupancy_map.add_edge_with_incremental_id("vertex16", "vertex7")

# ----------------------------

    occupancy_map.add_edge_with_incremental_id("vertex8", "vertex11")
    occupancy_map.add_edge_with_incremental_id("vertex8", "vertex15")
    occupancy_map.add_edge_with_incremental_id("vertex8", "vertex16")
    occupancy_map.add_edge_with_incremental_id("vertex8", "vertex17")
    occupancy_map.add_edge_with_incremental_id("vertex8", "vertex18")

    occupancy_map.add_edge_with_incremental_id("vertex11", "vertex8")
    occupancy_map.add_edge_with_incremental_id("vertex15", "vertex8")
    occupancy_map.add_edge_with_incremental_id("vertex16", "vertex8")
    occupancy_map.add_edge_with_incremental_id("vertex17", "vertex8")
    occupancy_map.add_edge_with_incremental_id("vertex18", "vertex8")

# ----------------------------

    occupancy_map.add_edge_with_incremental_id("vertex9", "vertex12")
    occupancy_map.add_edge_with_incremental_id("vertex9", "vertex14")

    occupancy_map.add_edge_with_incremental_id("vertex12", "vertex9")
    occupancy_map.add_edge_with_incremental_id("vertex14", "vertex9")

# ----------------------------

    occupancy_map.add_edge_with_incremental_id("vertex12", "vertex13")
    occupancy_map.add_edge_with_incremental_id("vertex12", "vertex14")

    occupancy_map.add_edge_with_incremental_id("vertex13", "vertex12")
    occupancy_map.add_edge_with_incremental_id("vertex14", "vertex12")

# ----------------------------

    occupancy_map.add_edge_with_incremental_id("vertex13", "vertex14")

    occupancy_map.add_edge_with_incremental_id("vertex14", "vertex13")

# ----------------------------

    occupancy_map.add_edge_with_incremental_id("vertex15", "vertex18")
    occupancy_map.add_edge_with_incremental_id("vertex15", "vertex19")

    occupancy_map.add_edge_with_incremental_id("vertex18", "vertex15")
    occupancy_map.add_edge_with_incremental_id("vertex19", "vertex15")

# ----------------------------

    occupancy_map.add_edge_with_incremental_id("vertex16", "vertex17")
    occupancy_map.add_edge_with_incremental_id("vertex16", "vertex18")

    occupancy_map.add_edge_with_incremental_id("vertex17", "vertex16")
    occupancy_map.add_edge_with_incremental_id("vertex18", "vertex16")

# ----------------------------

    occupancy_map.add_edge_with_incremental_id("vertex17", "vertex18")

    occupancy_map.add_edge_with_incremental_id("vertex18", "vertex17")

# ----------------------------

    occupancy_map.add_edge_with_incremental_id("vertex18", "vertex19")

    occupancy_map.add_edge_with_incremental_id("vertex19", "vertex18")


def create_topological_map_atc_corridor_20(occupancy_map):
    create_topological_map_atc_corridor_19(occupancy_map)
    occupancy_map.add_vertex_with_id("vertex20", 17.08, -5.88)

    occupancy_map.add_edge_with_incremental_id("vertex17", "vertex20")
    occupancy_map.add_edge_with_incremental_id("vertex20", "vertex17")
    occupancy_map.add_edge_with_incremental_id("vertex18", "vertex20")
    occupancy_map.add_edge_with_incremental_id("vertex20", "vertex18")
    occupancy_map.add_edge_with_incremental_id("vertex19", "vertex20")
    occupancy_map.add_edge_with_incremental_id("vertex20", "vertex19")

    occupancy_map.set_name('large_atc_corridor_20')



def create_topological_map_atc_corridor_21_old(occupancy_map):
    create_topological_map_atc_corridor_20(occupancy_map)
    occupancy_map.add_vertex_with_id("vertex21", 11.5, -5.21)

    occupancy_map.add_edge_with_incremental_id("vertex18", "vertex21")
    occupancy_map.add_edge_with_incremental_id("vertex21", "vertex18")

    occupancy_map.add_edge_with_incremental_id("vertex19", "vertex21")
    occupancy_map.add_edge_with_incremental_id("vertex21", "vertex19")

    occupancy_map.add_edge_with_incremental_id("vertex20", "vertex21")
    occupancy_map.add_edge_with_incremental_id("vertex21", "vertex20")

    occupancy_map.set_name('large_atc_corridor_21')


def create_topological_map_atc_corridor_22(occupancy_map):
    create_topological_map_atc_corridor_21(occupancy_map)
    occupancy_map.add_vertex_with_id("vertex22", 7.11, -6.31)
    
    occupancy_map.add_edge_with_incremental_id("vertex19", "vertex22")
    occupancy_map.add_edge_with_incremental_id("vertex22", "vertex19")

    occupancy_map.add_edge_with_incremental_id("vertex21", "vertex22")
    occupancy_map.add_edge_with_incremental_id("vertex22", "vertex21")


    occupancy_map.set_name('large_atc_corridor_22')


def create_topological_map_atc_corridor_23(occupancy_map):
    create_topological_map_atc_corridor_22(occupancy_map)
    occupancy_map.add_vertex_with_id("vertex23", 11.10, -0.89)

    occupancy_map.add_edge_with_incremental_id("vertex20", "vertex23")
    occupancy_map.add_edge_with_incremental_id("vertex23", "vertex20")

    occupancy_map.add_edge_with_incremental_id("vertex21", "vertex23")
    occupancy_map.add_edge_with_incremental_id("vertex23", "vertex21")

    occupancy_map.set_name('large_atc_corridor_23')

def create_topological_map_atc_corridor_24(occupancy_map):
    create_topological_map_atc_corridor_23(occupancy_map)
    occupancy_map.add_vertex_with_id("vertex24", 7.00, -3.07)

    occupancy_map.add_edge_with_incremental_id("vertex21", "vertex24")
    occupancy_map.add_edge_with_incremental_id("vertex24", "vertex21")

    occupancy_map.add_edge_with_incremental_id("vertex22", "vertex24")
    occupancy_map.add_edge_with_incremental_id("vertex24", "vertex22")

    occupancy_map.add_edge_with_incremental_id("vertex23", "vertex24")
    occupancy_map.add_edge_with_incremental_id("vertex24", "vertex23")

    occupancy_map.set_name('large_atc_corridor_24')



def create_topological_map_atc_corridor_25(occupancy_map):
    create_topological_map_atc_corridor_24(occupancy_map)
    occupancy_map.add_vertex_with_id("vertex25", 6.80, 0.42)

    occupancy_map.add_edge_with_incremental_id("vertex23", "vertex25")
    occupancy_map.add_edge_with_incremental_id("vertex25", "vertex23")

    occupancy_map.add_edge_with_incremental_id("vertex24", "vertex25")
    occupancy_map.add_edge_with_incremental_id("vertex25", "vertex24")

    occupancy_map.set_name('large_atc_corridor_25')


def create_topological_map_atc_corridor_26_old(occupancy_map):
    create_topological_map_atc_corridor_25(occupancy_map)
    occupancy_map.set_name('large_atc_corridor_26')
    occupancy_map.add_vertex_with_id("vertex26", -0.09, -5.91)

    occupancy_map.add_edge_with_incremental_id("vertex22", "vertex26")
    occupancy_map.add_edge_with_incremental_id("vertex26", "vertex22")

    occupancy_map.add_edge_with_incremental_id("vertex24", "vertex26")
    occupancy_map.add_edge_with_incremental_id("vertex26", "vertex24")

    occupancy_map.add_edge_with_incremental_id("vertex25", "vertex26")

    occupancy_map.add_edge_with_incremental_id("vertex26", "vertex25")

def create_topological_map_atc_corridor_27(occupancy_map):
    create_topological_map_atc_corridor_26(occupancy_map)
    occupancy_map.set_name('large_atc_corridor_27')

    occupancy_map.add_vertex_with_id("vertex27", 2.31, -0.15)

    occupancy_map.add_edge_with_incremental_id("vertex24", "vertex27")
    occupancy_map.add_edge_with_incremental_id("vertex27", "vertex24")

    occupancy_map.add_edge_with_incremental_id("vertex25", "vertex27")
    occupancy_map.add_edge_with_incremental_id("vertex27", "vertex25")

    occupancy_map.add_edge_with_incremental_id("vertex26", "vertex27")
    occupancy_map.add_edge_with_incremental_id("vertex27", "vertex26")


def create_topological_map_atc_corridor_28(occupancy_map):
    create_topological_map_atc_corridor_27(occupancy_map)
    occupancy_map.set_name('large_atc_corridor_28')

    occupancy_map.add_vertex_with_id("vertex28", -0.26, 4.19)

    occupancy_map.add_edge_with_incremental_id("vertex27", "vertex28")
    occupancy_map.add_edge_with_incremental_id("vertex28", "vertex27")

    occupancy_map.add_edge_with_incremental_id("vertex25", "vertex28")
    occupancy_map.add_edge_with_incremental_id("vertex28", "vertex25")

    occupancy_map.add_edge_with_incremental_id("vertex26", "vertex28")
    occupancy_map.add_edge_with_incremental_id("vertex28", "vertex26")


def create_topological_map_atc_corridor_29(occupancy_map):
    create_topological_map_atc_corridor_28(occupancy_map)
    occupancy_map.set_name('large_atc_corridor_29')
    occupancy_map.add_vertex_with_id("vertex29", -4.15, 0.40)

    occupancy_map.add_edge_with_incremental_id("vertex28", "vertex29")
    occupancy_map.add_edge_with_incremental_id("vertex29", "vertex28")

    occupancy_map.add_edge_with_incremental_id("vertex27", "vertex29")
    occupancy_map.add_edge_with_incremental_id("vertex29", "vertex27")

    occupancy_map.add_edge_with_incremental_id("vertex26", "vertex29")
    occupancy_map.add_edge_with_incremental_id("vertex29", "vertex26")

def create_large_topological_map_atc_corridor(occupancy_map):
    occupancy_map.set_name('large_atc_corridor')
    occupancy_map.add_vertex_with_id("vertex1", 50.55, -26.44)
    occupancy_map.add_vertex_with_id("vertex2", 40.03, -18.72)
    occupancy_map.add_vertex_with_id("vertex3", 34.15, -17.47)
    occupancy_map.add_vertex_with_id("vertex4", 21.91, -16.2)
    occupancy_map.add_vertex_with_id("vertex5", 27.88, -18.22)
    occupancy_map.add_vertex_with_id("vertex6", 35.64, -21.17)
    occupancy_map.add_vertex_with_id("vertex7", 27.0, -15.14)
    occupancy_map.add_vertex_with_id("vertex8", 19.79, -13.51)
    occupancy_map.add_vertex_with_id("vertex9", 41.46, -21.41)
    occupancy_map.add_vertex_with_id("vertex10", 31.7, -18.0)
    occupancy_map.add_vertex_with_id("vertex11", 24.71, -16.0)
    occupancy_map.add_vertex_with_id("vertex12", 42.88, -24.13)
    occupancy_map.add_vertex_with_id("vertex13", 52.28, -23.13)
    occupancy_map.add_vertex_with_id("vertex14", 47.14, -20.26)
    occupancy_map.add_vertex_with_id("vertex15", 17.02, -14.14)
    occupancy_map.add_vertex_with_id("vertex16", 22.6, -11.38)
    occupancy_map.add_vertex_with_id("vertex17", 20.6, -9.38)
    occupancy_map.add_vertex_with_id("vertex18", 16.59, -9.92)
    occupancy_map.add_vertex_with_id("vertex19", 11.28, -8.67)
    occupancy_map.add_vertex_with_id("vertex22", 11.5, -5.21)
    occupancy_map.add_vertex_with_id("vertex21", 7.11, -6.31)
    occupancy_map.add_vertex_with_id("vertex20", 17.08, -5.88)
    occupancy_map.add_vertex_with_id("vertex23", 11.10, -0.89)
    occupancy_map.add_vertex_with_id("vertex27", 2.31, -0.15)
    occupancy_map.add_vertex_with_id("vertex25", 6.80, 0.42)
    occupancy_map.add_vertex_with_id("vertex26", -0.09, -5.91)
    occupancy_map.add_vertex_with_id("vertex24", 7, -3.07)
    occupancy_map.add_vertex_with_id("vertex28", -0.26, 4.19)
    occupancy_map.add_vertex_with_id("vertex29", -4.15, 0.40)




    occupancy_map.add_edge_with_incremental_id("vertex1", "vertex12")
    occupancy_map.add_edge_with_incremental_id("vertex1", "vertex13")
    occupancy_map.add_edge_with_incremental_id("vertex1", "vertex14")

    occupancy_map.add_edge_with_incremental_id("vertex12", "vertex1")
    occupancy_map.add_edge_with_incremental_id("vertex13", "vertex1")
    occupancy_map.add_edge_with_incremental_id("vertex14", "vertex1")

# ----------------------------

    occupancy_map.add_edge_with_incremental_id("vertex2", "vertex3")
    occupancy_map.add_edge_with_incremental_id("vertex2", "vertex6")
    occupancy_map.add_edge_with_incremental_id("vertex2", "vertex9")
    occupancy_map.add_edge_with_incremental_id("vertex2", "vertex12")
    occupancy_map.add_edge_with_incremental_id("vertex2", "vertex14")

    occupancy_map.add_edge_with_incremental_id("vertex3", "vertex2")
    occupancy_map.add_edge_with_incremental_id("vertex6", "vertex2")
    occupancy_map.add_edge_with_incremental_id("vertex9", "vertex2")
    occupancy_map.add_edge_with_incremental_id("vertex12", "vertex2")
    occupancy_map.add_edge_with_incremental_id("vertex14", "vertex2")

# ----------------------------

    occupancy_map.add_edge_with_incremental_id("vertex3", "vertex6")
    occupancy_map.add_edge_with_incremental_id("vertex3", "vertex7")
    occupancy_map.add_edge_with_incremental_id("vertex3", "vertex9")
    occupancy_map.add_edge_with_incremental_id("vertex3", "vertex10")

    occupancy_map.add_edge_with_incremental_id("vertex6", "vertex3")
    occupancy_map.add_edge_with_incremental_id("vertex7", "vertex3")
    occupancy_map.add_edge_with_incremental_id("vertex9", "vertex3")
    occupancy_map.add_edge_with_incremental_id("vertex10", "vertex3")

# ----------------------------

    occupancy_map.add_edge_with_incremental_id("vertex4", "vertex5")
    occupancy_map.add_edge_with_incremental_id("vertex4", "vertex8")
    occupancy_map.add_edge_with_incremental_id("vertex4", "vertex11")
    occupancy_map.add_edge_with_incremental_id("vertex4", "vertex15")

    occupancy_map.add_edge_with_incremental_id("vertex5", "vertex4")
    occupancy_map.add_edge_with_incremental_id("vertex8", "vertex4")
    occupancy_map.add_edge_with_incremental_id("vertex11", "vertex4")
    occupancy_map.add_edge_with_incremental_id("vertex15", "vertex4")

# ----------------------------

    occupancy_map.add_edge_with_incremental_id("vertex5", "vertex6")
    occupancy_map.add_edge_with_incremental_id("vertex5", "vertex7")
    occupancy_map.add_edge_with_incremental_id("vertex5", "vertex10")
    occupancy_map.add_edge_with_incremental_id("vertex5", "vertex11")

    occupancy_map.add_edge_with_incremental_id("vertex6", "vertex5")
    occupancy_map.add_edge_with_incremental_id("vertex7", "vertex5")
    occupancy_map.add_edge_with_incremental_id("vertex10", "vertex5")
    occupancy_map.add_edge_with_incremental_id("vertex11", "vertex5")

# ----------------------------

    occupancy_map.add_edge_with_incremental_id("vertex6", "vertex9")
    occupancy_map.add_edge_with_incremental_id("vertex6", "vertex10")
    occupancy_map.add_edge_with_incremental_id("vertex6", "vertex12")

    occupancy_map.add_edge_with_incremental_id("vertex9", "vertex6")
    occupancy_map.add_edge_with_incremental_id("vertex10", "vertex6")
    occupancy_map.add_edge_with_incremental_id("vertex12", "vertex6")

# ----------------------------

    occupancy_map.add_edge_with_incremental_id("vertex7", "vertex8")
    occupancy_map.add_edge_with_incremental_id("vertex7", "vertex10")
    occupancy_map.add_edge_with_incremental_id("vertex7", "vertex11")
    occupancy_map.add_edge_with_incremental_id("vertex7", "vertex16")

    occupancy_map.add_edge_with_incremental_id("vertex8", "vertex7")
    occupancy_map.add_edge_with_incremental_id("vertex10", "vertex7")
    occupancy_map.add_edge_with_incremental_id("vertex11", "vertex7")
    occupancy_map.add_edge_with_incremental_id("vertex16", "vertex7")

# ----------------------------

    occupancy_map.add_edge_with_incremental_id("vertex8", "vertex11")
    occupancy_map.add_edge_with_incremental_id("vertex8", "vertex15")
    occupancy_map.add_edge_with_incremental_id("vertex8", "vertex16")
    occupancy_map.add_edge_with_incremental_id("vertex8", "vertex17")
    occupancy_map.add_edge_with_incremental_id("vertex8", "vertex18")

    occupancy_map.add_edge_with_incremental_id("vertex11", "vertex8")
    occupancy_map.add_edge_with_incremental_id("vertex15", "vertex8")
    occupancy_map.add_edge_with_incremental_id("vertex16", "vertex8")
    occupancy_map.add_edge_with_incremental_id("vertex17", "vertex8")
    occupancy_map.add_edge_with_incremental_id("vertex18", "vertex8")

# ----------------------------

    occupancy_map.add_edge_with_incremental_id("vertex9", "vertex12")
    occupancy_map.add_edge_with_incremental_id("vertex9", "vertex14")

    occupancy_map.add_edge_with_incremental_id("vertex12", "vertex9")
    occupancy_map.add_edge_with_incremental_id("vertex14", "vertex9")

# ----------------------------

    occupancy_map.add_edge_with_incremental_id("vertex12", "vertex13")
    occupancy_map.add_edge_with_incremental_id("vertex12", "vertex14")

    occupancy_map.add_edge_with_incremental_id("vertex13", "vertex12")
    occupancy_map.add_edge_with_incremental_id("vertex14", "vertex12")

# ----------------------------

    occupancy_map.add_edge_with_incremental_id("vertex13", "vertex14")

    occupancy_map.add_edge_with_incremental_id("vertex14", "vertex13")

# ----------------------------

    occupancy_map.add_edge_with_incremental_id("vertex15", "vertex18")
    occupancy_map.add_edge_with_incremental_id("vertex15", "vertex19")

    occupancy_map.add_edge_with_incremental_id("vertex18", "vertex15")
    occupancy_map.add_edge_with_incremental_id("vertex19", "vertex15")

# ----------------------------

    occupancy_map.add_edge_with_incremental_id("vertex16", "vertex17")
    occupancy_map.add_edge_with_incremental_id("vertex16", "vertex18")

    occupancy_map.add_edge_with_incremental_id("vertex17", "vertex16")
    occupancy_map.add_edge_with_incremental_id("vertex18", "vertex16")

# ----------------------------

    occupancy_map.add_edge_with_incremental_id("vertex17", "vertex18")
    occupancy_map.add_edge_with_incremental_id("vertex17", "vertex20")

    occupancy_map.add_edge_with_incremental_id("vertex18", "vertex17")
    occupancy_map.add_edge_with_incremental_id("vertex20", "vertex17")

# ----------------------------

    occupancy_map.add_edge_with_incremental_id("vertex18", "vertex19")
    occupancy_map.add_edge_with_incremental_id("vertex18", "vertex20")

    occupancy_map.add_edge_with_incremental_id("vertex19", "vertex18")
    occupancy_map.add_edge_with_incremental_id("vertex20", "vertex18")

# ----------------------------

    occupancy_map.add_edge_with_incremental_id("vertex19", "vertex22")
    occupancy_map.add_edge_with_incremental_id("vertex19", "vertex21")
    occupancy_map.add_edge_with_incremental_id("vertex19", "vertex20")

    occupancy_map.add_edge_with_incremental_id("vertex22", "vertex19")
    occupancy_map.add_edge_with_incremental_id("vertex21", "vertex19")
    occupancy_map.add_edge_with_incremental_id("vertex20", "vertex19")

# ----------------------------

    occupancy_map.add_edge_with_incremental_id("vertex22", "vertex21")
    occupancy_map.add_edge_with_incremental_id("vertex22", "vertex20")
    occupancy_map.add_edge_with_incremental_id("vertex22", "vertex23")
    occupancy_map.add_edge_with_incremental_id("vertex22", "vertex27")

    occupancy_map.add_edge_with_incremental_id("vertex21", "vertex22")
    occupancy_map.add_edge_with_incremental_id("vertex20", "vertex22")
    occupancy_map.add_edge_with_incremental_id("vertex23", "vertex22")
    occupancy_map.add_edge_with_incremental_id("vertex27", "vertex22")

# ----------------------------

    occupancy_map.add_edge_with_incremental_id("vertex21", "vertex26")
    occupancy_map.add_edge_with_incremental_id("vertex21", "vertex27")

    occupancy_map.add_edge_with_incremental_id("vertex26", "vertex21")
    occupancy_map.add_edge_with_incremental_id("vertex27", "vertex21")

# ----------------------------

    occupancy_map.add_edge_with_incremental_id("vertex20", "vertex23")

    occupancy_map.add_edge_with_incremental_id("vertex23", "vertex20")

# ----------------------------

    occupancy_map.add_edge_with_incremental_id("vertex23", "vertex25")
    occupancy_map.add_edge_with_incremental_id("vertex23", "vertex27")

    occupancy_map.add_edge_with_incremental_id("vertex25", "vertex23")
    occupancy_map.add_edge_with_incremental_id("vertex27", "vertex23")

# ----------------------------

    occupancy_map.add_edge_with_incremental_id("vertex24", "vertex25")
    occupancy_map.add_edge_with_incremental_id("vertex24", "vertex26")
    occupancy_map.add_edge_with_incremental_id("vertex24", "vertex27")
    occupancy_map.add_edge_with_incremental_id("vertex24", "vertex28")
    occupancy_map.add_edge_with_incremental_id("vertex24", "vertex29")

    occupancy_map.add_edge_with_incremental_id("vertex25", "vertex24")
    occupancy_map.add_edge_with_incremental_id("vertex26", "vertex24")
    occupancy_map.add_edge_with_incremental_id("vertex27", "vertex24")
    occupancy_map.add_edge_with_incremental_id("vertex28", "vertex24")
    occupancy_map.add_edge_with_incremental_id("vertex29", "vertex24")

# ----------------------------

    occupancy_map.add_edge_with_incremental_id("vertex25", "vertex27")
    occupancy_map.add_edge_with_incremental_id("vertex25", "vertex28")

    occupancy_map.add_edge_with_incremental_id("vertex27", "vertex25")
    occupancy_map.add_edge_with_incremental_id("vertex28", "vertex25")

# ----------------------------

    occupancy_map.add_edge_with_incremental_id("vertex26", "vertex27")
    occupancy_map.add_edge_with_incremental_id("vertex26", "vertex28")
    occupancy_map.add_edge_with_incremental_id("vertex26", "vertex29")

    occupancy_map.add_edge_with_incremental_id("vertex27", "vertex26")
    occupancy_map.add_edge_with_incremental_id("vertex28", "vertex26")
    occupancy_map.add_edge_with_incremental_id("vertex29", "vertex26")

# ----------------------------

    occupancy_map.add_edge_with_incremental_id("vertex28", "vertex29")

    occupancy_map.add_edge_with_incremental_id("vertex29", "vertex28") 

# ----------------------------

def create_small_topological_map_atc_corridor(occupancy_map):
    occupancy_map.set_name('small_atc_corridor')
    occupancy_map.add_vertex_with_id("vertex1", 43.89, -22.09)
    occupancy_map.add_vertex_with_id("vertex2", 40.03, -18.72)
    occupancy_map.add_vertex_with_id("vertex3", 34.15, -17.47)
    occupancy_map.add_vertex_with_id("vertex4", 35.52, -20.16)
    
    occupancy_map.add_edge_with_id("edge1", "vertex1", "vertex2")
    occupancy_map.add_edge_with_id("edge2", "vertex1", "vertex3")
    occupancy_map.add_edge_with_id("edge3", "vertex1", "vertex4")
    occupancy_map.add_edge_with_id("edge4", "vertex2", "vertex3")
    occupancy_map.add_edge_with_id("edge5", "vertex2", "vertex4")
    occupancy_map.add_edge_with_id("edge6", "vertex3", "vertex4")

    # add also the opposite edges
    occupancy_map.add_edge_with_id("edge7", "vertex2", "vertex1")
    occupancy_map.add_edge_with_id("edge8", "vertex3", "vertex1")
    occupancy_map.add_edge_with_id("edge9", "vertex4", "vertex1")
    occupancy_map.add_edge_with_id("edge10", "vertex3", "vertex2")
    occupancy_map.add_edge_with_id("edge11", "vertex4", "vertex2")
    occupancy_map.add_edge_with_id("edge12", "vertex4", "vertex3")

def create_medium_topological_map_atc_square(occupancy_map):
    occupancy_map.set_name('medium_atc_square')
    occupancy_map.add_vertex_with_id("vertex1", -4.5, -2.2)
    occupancy_map.add_vertex_with_id("vertex2", -6.3, -4.8)
    occupancy_map.add_vertex_with_id("vertex3", -11.1, 2.5)
    occupancy_map.add_vertex_with_id("vertex4", -16.5, 0)
    occupancy_map.add_vertex_with_id("vertex5", -11.1, 0)
    occupancy_map.add_vertex_with_id("vertex6", -6.3, 2.5)
    

    occupancy_map.add_edge_with_id("edge1", "vertex1", "vertex2")
    occupancy_map.add_edge_with_id("edge2", "vertex1", "vertex3")
    occupancy_map.add_edge_with_id("edge3", "vertex1", "vertex5")
    occupancy_map.add_edge_with_id("edge4", "vertex1", "vertex6")
    occupancy_map.add_edge_with_id("edge5", "vertex2", "vertex4")
    occupancy_map.add_edge_with_id("edge6", "vertex2", "vertex5")
    occupancy_map.add_edge_with_id("edge7", "vertex2", "vertex6")
    occupancy_map.add_edge_with_id("edge8", "vertex3", "vertex4")
    occupancy_map.add_edge_with_id("edge9", "vertex3", "vertex5")
    occupancy_map.add_edge_with_id("edge10", "vertex3", "vertex6")
    occupancy_map.add_edge_with_id("edge11", "vertex4", "vertex5")
    occupancy_map.add_edge_with_id("edge12", "vertex5", "vertex6")


    occupancy_map.add_edge_with_id("edge13", "vertex2", "vertex1")
    occupancy_map.add_edge_with_id("edge14", "vertex3", "vertex1")
    occupancy_map.add_edge_with_id("edge15", "vertex5", "vertex1")
    occupancy_map.add_edge_with_id("edge16", "vertex6", "vertex1")
    occupancy_map.add_edge_with_id("edge17", "vertex4", "vertex2")
    occupancy_map.add_edge_with_id("edge18", "vertex5", "vertex2")
    occupancy_map.add_edge_with_id("edge19", "vertex6", "vertex2")
    occupancy_map.add_edge_with_id("edge20", "vertex4", "vertex3")
    occupancy_map.add_edge_with_id("edge21", "vertex5", "vertex3")
    occupancy_map.add_edge_with_id("edge22", "vertex6", "vertex3")
    occupancy_map.add_edge_with_id("edge23", "vertex5", "vertex4")
    occupancy_map.add_edge_with_id("edge24", "vertex6", "vertex5")

def create_large_topological_map_atc_square(occupancy_map):
    occupancy_map.set_name('large_atc_square')
    occupancy_map.add_vertex_with_id("vertex1", -4.5, -2.2)
    occupancy_map.add_vertex_with_id("vertex2", -6.3, -4.8)
    occupancy_map.add_vertex_with_id("vertex3", -11.1, 2.5)
    occupancy_map.add_vertex_with_id("vertex4", -16.5, 0)
    occupancy_map.add_vertex_with_id("vertex5", -11.1, 0)
    occupancy_map.add_vertex_with_id("vertex6", -6.3, 2.5)
    occupancy_map.add_vertex_with_id("vertex7", -11.87, -4.97)
    occupancy_map.add_vertex_with_id("vertex8", -4.95, 5.48)
    occupancy_map.add_vertex_with_id("vertex9", 0, 2)
    occupancy_map.add_vertex_with_id("vertex10", -2.4, -3.31)
    occupancy_map.add_vertex_with_id("vertex11", -7.91, -1.63)
    occupancy_map.add_vertex_with_id("vertex12", -3.78, 0.63)

    occupancy_map.add_edge_with_incremental_id("vertex1", "vertex2")
    occupancy_map.add_edge_with_incremental_id( "vertex1", "vertex9")
    occupancy_map.add_edge_with_incremental_id("vertex1", "vertex10")
    occupancy_map.add_edge_with_incremental_id("vertex1", "vertex11")
    occupancy_map.add_edge_with_incremental_id("vertex1", "vertex12")
    occupancy_map.add_edge_with_incremental_id("vertex2", "vertex4")
    occupancy_map.add_edge_with_incremental_id("vertex2", "vertex5")
    occupancy_map.add_edge_with_incremental_id("vertex2", "vertex7")
    occupancy_map.add_edge_with_incremental_id("vertex2", "vertex10")
    occupancy_map.add_edge_with_incremental_id("vertex2", "vertex11")
    occupancy_map.add_edge_with_incremental_id("vertex3", "vertex4")
    occupancy_map.add_edge_with_incremental_id("vertex3", "vertex5")
    occupancy_map.add_edge_with_incremental_id("vertex3", "vertex6")
    occupancy_map.add_edge_with_incremental_id("vertex3", "vertex8")
    occupancy_map.add_edge_with_incremental_id("vertex4", "vertex5")
    occupancy_map.add_edge_with_incremental_id("vertex4", "vertex7")
    occupancy_map.add_edge_with_incremental_id("vertex5", "vertex6")
    occupancy_map.add_edge_with_incremental_id("vertex5", "vertex7")
    occupancy_map.add_edge_with_incremental_id("vertex5", "vertex11")
    occupancy_map.add_edge_with_incremental_id("vertex6", "vertex8")
    occupancy_map.add_edge_with_incremental_id("vertex6", "vertex9")
    occupancy_map.add_edge_with_incremental_id("vertex6", "vertex12")
    occupancy_map.add_edge_with_incremental_id("vertex8", "vertex9")
    occupancy_map.add_edge_with_incremental_id("vertex8", "vertex12")
    occupancy_map.add_edge_with_incremental_id("vertex9", "vertex10")
    occupancy_map.add_edge_with_incremental_id("vertex9", "vertex12")
    occupancy_map.add_edge_with_incremental_id("vertex10", "vertex12")

    # add also the opposite edges

    occupancy_map.add_edge_with_incremental_id("vertex2", "vertex1")
    occupancy_map.add_edge_with_incremental_id("vertex9", "vertex1")
    occupancy_map.add_edge_with_incremental_id("vertex10", "vertex1")
    occupancy_map.add_edge_with_incremental_id("vertex11", "vertex1")
    occupancy_map.add_edge_with_incremental_id("vertex12", "vertex1")
    occupancy_map.add_edge_with_incremental_id("vertex4", "vertex2")
    occupancy_map.add_edge_with_incremental_id("vertex5", "vertex2")
    occupancy_map.add_edge_with_incremental_id("vertex7", "vertex2")
    occupancy_map.add_edge_with_incremental_id("vertex10", "vertex2")
    occupancy_map.add_edge_with_incremental_id("vertex11", "vertex2")
    occupancy_map.add_edge_with_incremental_id("vertex4", "vertex3")
    occupancy_map.add_edge_with_incremental_id("vertex5", "vertex3")
    occupancy_map.add_edge_with_incremental_id("vertex6", "vertex3")
    occupancy_map.add_edge_with_incremental_id("vertex8", "vertex3")
    occupancy_map.add_edge_with_incremental_id("vertex5", "vertex4")
    occupancy_map.add_edge_with_incremental_id("vertex7", "vertex4")
    occupancy_map.add_edge_with_incremental_id("vertex6", "vertex5")
    occupancy_map.add_edge_with_incremental_id("vertex7", "vertex5")
    occupancy_map.add_edge_with_incremental_id("vertex11", "vertex5")
    occupancy_map.add_edge_with_incremental_id("vertex8", "vertex6")
    occupancy_map.add_edge_with_incremental_id("vertex9", "vertex6")
    occupancy_map.add_edge_with_incremental_id("vertex12", "vertex6")
    occupancy_map.add_edge_with_incremental_id("vertex9", "vertex8")
    occupancy_map.add_edge_with_incremental_id("vertex12", "vertex8")
    occupancy_map.add_edge_with_incremental_id("vertex10", "vertex9")
    occupancy_map.add_edge_with_incremental_id("vertex12", "vertex9")
    occupancy_map.add_edge_with_incremental_id("vertex12", "vertex10")

def create_medium_topological_map_iit(occupancy_map):
    occupancy_map.set_name('medium_iit')
    
    # add the vertices
    assert occupancy_map.add_vertex_with_id("vertex1", 0, -12)
    assert occupancy_map.add_vertex_with_id("vertex2", 1, -2)
    assert occupancy_map.add_vertex_with_id("vertex3", 3, -6)
    assert occupancy_map.add_vertex_with_id("vertex4", 8, -10)
    assert occupancy_map.add_vertex_with_id("vertex5", 6, -3)

    # add the edges
    assert occupancy_map.add_edge_with_id("edge1", "vertex1", "vertex2")
    assert occupancy_map.add_edge_with_id("edge9", "vertex2", "vertex1")
    assert occupancy_map.add_edge_with_id("edge2", "vertex1", "vertex3")
    assert occupancy_map.add_edge_with_id("edge10", "vertex3", "vertex1")
    assert occupancy_map.add_edge_with_id("edge3", "vertex1", "vertex4")
    assert occupancy_map.add_edge_with_id("edge11", "vertex4", "vertex1")
    assert occupancy_map.add_edge_with_id("edge4", "vertex2", "vertex3")
    assert occupancy_map.add_edge_with_id("edge12", "vertex3", "vertex2")
    assert occupancy_map.add_edge_with_id("edge5", "vertex3", "vertex4")
    assert occupancy_map.add_edge_with_id("edge13", "vertex4", "vertex3")
    assert occupancy_map.add_edge_with_id("edge6", "vertex2", "vertex5")
    assert occupancy_map.add_edge_with_id("edge14", "vertex5", "vertex2")
    assert occupancy_map.add_edge_with_id("edge7", "vertex3", "vertex5")
    assert occupancy_map.add_edge_with_id("edge15", "vertex5", "vertex3")
    assert occupancy_map.add_edge_with_id("edge8", "vertex4", "vertex5")
    assert occupancy_map.add_edge_with_id("edge16", "vertex5", "vertex4")

def create_small_topological_map_iit(occupancy_map):
    occupancy_map.set_name('small_iit')
    
    # add the vertices
    assert occupancy_map.add_vertex_with_id("vertex1", 0, 0)
    assert occupancy_map.add_vertex_with_id("vertex2", 1, 6)
    assert occupancy_map.add_vertex_with_id("vertex3", 5, 5)
    assert occupancy_map.add_vertex_with_id("vertex4", 7, 0)

    # add the edges
    assert occupancy_map.add_edge_with_id("edge1", "vertex1", "vertex2")
    assert occupancy_map.add_edge_with_id("edge9", "vertex2", "vertex1")
    assert occupancy_map.add_edge_with_id("edge2", "vertex1", "vertex3")
    assert occupancy_map.add_edge_with_id("edge10", "vertex3", "vertex1")
    assert occupancy_map.add_edge_with_id("edge3", "vertex1", "vertex4")
    assert occupancy_map.add_edge_with_id("edge11", "vertex4", "vertex1")
    assert occupancy_map.add_edge_with_id("edge4", "vertex2", "vertex3")
    assert occupancy_map.add_edge_with_id("edge12", "vertex3", "vertex2")
    assert occupancy_map.add_edge_with_id("edge5", "vertex3", "vertex4")
    assert occupancy_map.add_edge_with_id("edge13", "vertex4", "vertex3")

def get_times_atc():
    num_iterations = 2000
    # read the file times_higher_20.csv and put into a list
    filename = 'times_higher_17_atc_reduced'
    time_list = []
    with open(filename + '.csv', 'r') as f:
        reader = csv.reader(f)
        time_list = list(reader)[0]
    times = []
    with open('dataset/atc/atc_reduced.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            times.append(row[0])
    for time_index in range(0, len(times), int(len(times)/num_iterations)):
        time_list.append(times[time_index])
    return time_list

def create_occupancy_map_atc(occupancy_map, level, topological_map_creator_function, num_iterations=3000):
    topological_map_creator_function(occupancy_map)
    edges = occupancy_map.get_edges()
    for edge_key in edges:
        occupancy_map.add_edge_limit(edges[edge_key].get_id(), level)
    occupancy_map.calculate_average_edge_traverse_times(num_iterations)
    folder = 'data/occupancy_maps_' + occupancy_map.get_name()
    utils.create_folder(folder)

    filename = folder + '/occupancy_map_' + occupancy_map.get_name() + "_" + str(len(level))+'_levels.yaml'
    occupancy_map.save_occupancy_map(filename)

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


def get_times_madama():
    # read the file times_higher_7_madama.csv and put into a list
    filename = 'times_higher_7_madama.csv'
    time_list = []
    with open(filename) as f:
        for line in f:
            time_list.append(float(line.strip()))
    return time_list

def create_occupancy_map_madama(occupancy_map, level, topological_map_creator_function, num_iterations=1000):
    topological_map_creator_function(occupancy_map)
    edges = occupancy_map.get_edges()
    for edge_key in edges:
        occupancy_map.add_edge_limit(edges[edge_key].get_id(), level)
    occupancy_map.calculate_average_edge_traverse_times_with_time_list(get_times_madama())
    folder = 'data/occupancy_maps_' + occupancy_map.get_name()
    utils.create_folder(folder)

    filename = folder + '/occupancy_map_' + occupancy_map.get_name() + "_" + str(len(level))+'_levels.yaml'
    occupancy_map.save_occupancy_map(filename)


if __name__ == "__main__":
    # print(matrix)
    warnings.filterwarnings("ignore")
    predictor = create_atc_cliff_predictor()
    predictor_madama = create_madama_cliff_predictor()
    # topological_map_creator_function = [create_large_topological_map_atc_corridor, create_medium_large_topological_map_atc_corridor]
    topological_map_creator_function = [create_topological_map_atc_corridor_21, create_topological_map_atc_corridor_16, create_topological_map_atc_corridor_11]
    # topological_map_creator_function = [create_large_topological_map_atc_corridor, create_medium_topological_map_atc_corridor, create_small_topological_map_atc_corridor,
    #                                      create_large_topological_map_atc_square, create_medium_topological_map_atc_square]
    topological_map_creator_function_madama = [create_madama_topological_map_11]
    # two levels
    occupancy_levels = [(["zero", "one"], {"zero": [0,1], "one": [1,9999999]}),
                        (["zero", "one", "two"], {"zero": [0,1], "one": [1,3], "two": [3,9999999]}),
                        (["zero", "one", "two", "three"], {"zero": [0,1], "one": [1,3], "two": [3,6], "three": [6,9999999]}),
                        (["zero", "one", "two", "three", "four"], {"zero": [0,1], "one": [1,3], "two": [3,5], "three": [5,7], "four": [7,9999999]}),
                        (["zero", "one", "two", "three", "four", "five"], {"zero": [0,1], "one": [1,3], "two": [3,5], "three": [5,7], "four": [7,9], "five": [9,9999999]}),
                        (["zero", "one", "two", "three", "four", "five", "six"], {"zero": [0,1], "one": [1,3], "two": [3,5], "three": [5,7], "four": [7,9], "five": [9,12], "six": [12,9999999]}),
                        (["zero", "one", "two", "three", "four", "five", "six", "seven"], {"zero": [0,1], "one": [1,2], "two": [2,3], "three": [3,4], "four": [4,5], "five": [5,6], "six": [6,7], "seven": [7,9999999]})
                        ]



    for function_name in topological_map_creator_function_madama:
        for levels in [occupancy_levels[0]]:
            occupancy_map = OccupancyMap(predictor_madama, levels[0])
            create_occupancy_map_madama(occupancy_map, levels[1], function_name, 30000)
    #         occupancy_map.plot_topological_map(predictor_madama.map_file, predictor_madama.fig_size, occupancy_map.get_name())

    for levels in  occupancy_levels:  # just two levels
        for vertex_number in [26, 21,16,11, 6]:
            occupancy_map = OccupancyMap(predictor, levels[0])
            function_name_map = globals()[f'create_topological_map_atc_corridor_{vertex_number}']
            create_occupancy_map_atc(occupancy_map, levels[1], function_name_map)
            # occupancy_map.plot_topological_map(predictor.map_file, predictor.fig_size, occupancy_map.get_name())
