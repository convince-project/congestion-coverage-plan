import matplotlib
import shapely
import datetime
import OccupancyMapCreator
from PredictorCreator import create_atc_cliff_predictor, create_iit_cliff_predictor
import warnings
from OccupancyMap import OccupancyMap
from matplotlib import path
from tqdm import tqdm
# create 3 polygons

warnings.filterwarnings("ignore")
predictor = create_atc_cliff_predictor()
topological_map_creator_function = [OccupancyMapCreator.create_medium_topological_map_atc_corridor]
levels = [(["zero", "one"], {"zero": [0,1], "one": [1,9999999]})]
predictor = create_atc_cliff_predictor()
predictor_iit = create_iit_cliff_predictor()
occupancy_map = OccupancyMap(predictor, levels[0])
OccupancyMapCreator.create_medium_topological_map_atc_corridor(occupancy_map)

# create a list with 1000 random points
points = occupancy_map.get_random_points(100000)
time_start = datetime.datetime.now()
shapely_polygon = shapely.geometry.Polygon(occupancy_map.get_edges_list()[0].get_area())
for point in tqdm(points):
    shapely_polygon.contains(shapely.geometry.Point(point[0], point[1]))


time_end = datetime.datetime.now()
print("Time to check 100000 points shapely: ", time_end - time_start)

area = path.Path(occupancy_map.get_edges_list()[0].get_area())
time_start = datetime.datetime.now()
for point in tqdm(points):
    area.contains_point(point)
time_end = datetime.datetime.now()
print("Time to check 100000 points matplotlib: ", time_end - time_start)
