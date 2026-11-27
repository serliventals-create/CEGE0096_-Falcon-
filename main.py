"""Implement the coursework application here.

Your group chooses the classes, interfaces, modules, and user interaction.
You may create additional files and packages as your design requires.
"""

# TODO: implement and integrate the coursework tasks using your own design.


'''Main application for the emergency evacuation route planner.'''

import sys
from pathlib import Path

from highest_point import HighestPointFinder
from nearest_itn import NearestITNNode


# TASK 1: User input (tim)
def get_user_location():

    easting = float(input("Enter your easting: "))
    northing = float(input("Enter your northing: "))

    if 430000 <= easting <= 465000 and 80000 <= northing <= 95000:
        print("Location is inside the permitted area.")
    else:
        print("This location is outside the permitted area.")
        sys.exit()

    return easting, northing


def main():

    user_location = get_user_location()

    print("User location:", user_location)

    # TASK 6: Find highest point within 5 km (eric)
    project_folder = Path(__file__).resolve().parent

    raster_path = (
        project_folder / "Material" / "elevation" / "SZ.asc"
    )

    finder = HighestPointFinder(raster_path)

    highest_point = finder.find_highest_point(
        *user_location
    )

    print("Highest point:", highest_point)
    print("Elevation:", highest_point[2], "metres")

    # TASK 7: Find nearest ITN nodes (ser)
    network = NearestITNNode()

    start_node, end_node = network.find_route_nodes(
        user_location,
        highest_point
    )

    print("Start node:", start_node)
    print("End node:", end_node)

    # Extract node IDs for Task 8 (eric)
    start_id = start_node[0]
    end_id = end_node[0]

    print("Start node ID:", start_id)
    print("End node ID:", end_id)


if __name__ == "__main__":
    main()
