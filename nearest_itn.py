
import json
import math
from rtree import index
from pathlib import Path 


class NearestITNNode:

    def __init__(self):
        file_path = (Path(__file__).resolve().parent/'itn'/'solent_itn.json')

        with open(file_path, "r") as file:
            data = json.load(file)

        self.nodes = data["roadnodes"]

        #R-tree spatial index
        self.spatial_index = index.Index()

        self.node_ids = []

        # Entering road node into the R-tree
        for i, (node_id, node_data) in enumerate(
            self.nodes.items()):
            x, y = node_data["coords"]

            self.spatial_index.insert(
                i, (x, y, x, y)
            )

            self.node_ids.append(node_id)

    def find_nearest(self, point):

        x, y = point

        nearest_index = next(
            self.spatial_index.nearest(
                (x, y, x, y), 1
            )
        )

        # Convert index number to ITN node ID
        node_id = self.node_ids[nearest_index]

        #Node coordinates
        node_x, node_y = self.nodes[node_id]["coords"]

        distance = math.sqrt(
            (node_x - x) ** 2 + (node_y - y) ** 2
        )

        return node_id, (node_x, node_y), distance

    def find_route_nodes(self, user_location, highest_point):
        highest_coords = highest_point[:2]
            
        start_node = self.find_nearest(user_location)
        end_node = self.find_nearest(highest_coords)

        return start_node, end_node
    
'''
add this to main (user location from task 1 and highest point from task 6):

from nearest_itn import NearestITNNode

network = NearestITNNode()

start_node, end_node = network.find_route_nodes(
    user_location, 
    highest_point)

print('Start node:', start_node)
print('end_node:', end_node)
'''
