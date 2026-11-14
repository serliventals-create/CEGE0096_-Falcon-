"""Task 4: implement the Gift Wrapping algorithm in this file.

Read input.csv, use the Task 2 orientation calculation, and write output.csv
in the supplied id,x,y format. Choose your own classes, functions, and APIs.
The point.py and plotter.py helpers are optional and may be adapted.
"""

# TODO: read the input points, preserving their identifiers.
# TODO: implement Gift Wrapping and use your orientation calculation.
# TODO: write the hull vertices to output.csv.
# TODO: optionally visualise your result with the supplied plotting helper.

import pandas as pd
from orientation import OrientationCheck
from plotter import Plotter

df = pd.read_csv("input.csv")

points = []

for _,point in df.iterrows():
    points.append((point['x'], point['y']))

leftmost = min(points, key=lambda p: p[0])

hull = []

point_on_hull = leftmost

while True:

    hull.append(point_on_hull)

    endpoint = points[0]

    for candidate in points:

        if endpoint == point_on_hull:
            endpoint = candidate

        elif OrientationCheck.orientation(
            point_on_hull,
            endpoint,
            candidate) == -1:

            endpoint = candidate

    point_on_hull = endpoint

    if endpoint == leftmost:
        break

output_rows = []

for point in hull:

    match = df[(df['x'] == point[0]) & (df['y'] == point[1])]

    output_rows.append({
        "id" : int(match.iloc[0]["id"]),
        "x" : point[0],
        "y" : point[1]
    })

# Save the hull points to output.csv
output_df = pd.DataFrame(output_rows)
output_df.to_csv("output.csv", index=False)

print("Convex hull points have been saved to output.csv")

# Visualisation of the hull points using the Plotter class from plotter.py
plotter = Plotter(points, hull)
plotter.plot()