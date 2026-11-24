
from nearest_itn import NearestITNNode
import math 

network = NearestITNNode()

# Sample coordinates
user_location = (439619, 85800)
highest_point = (440850, 86900)

#testing find route nodes
#sample data
start_node, end_node = network.find_route_nodes(user_location, highest_point)

print('Start node:', start_node)
print('End node:', end_node)

assert len(start_node) == 3
assert len(end_node) == 3 

assert start_node == network.find_nearest(user_location)
assert end_node == network.find_nearest(highest_point)

print('Test 1 passed')



# testing nearest network node
for point, result in [(user_location, start_node), (highest_point, end_node)]:
    node_id, coordinates, distance = result

all_distances = []

for node_data in network.nodes.values():
    x, y = node_data['coords']

    d = math.sqrt((x - point[0])** 2 + (y - point[1])**2)

    all_distances.append(d)

minimum_distance = min(all_distances)


print("Input point:", point)
print("R-tree node:", node_id)
print("R-tree distance:", distance)
print("Minimum calculated distance:", minimum_distance)

assert math.isclose(distance, minimum_distance, abs_tol= 0.000001)
print('Test 2 passed')


