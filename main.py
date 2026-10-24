"""Implement the coursework application here.

Your group chooses the classes, interfaces, modules, and user interaction.
You may create additional files and packages as your design requires.
"""

# TODO: implement and integrate the coursework tasks using your own design.

#Task 1: User Input/System Output
import sys

def get_user_location():
    easting = float(input("Enter your easting: "))
    northing = float(input("Enter your northing: "))

    if 430000 <= easting <= 465000 and 80000 <= northing <= 95000:
        print("Location is inside the permitted area.")
    else:
        print("This location is outside the permitted area. Please try again.")
        sys.exit()
    return easting, northing

easting, northing = get_user_location()