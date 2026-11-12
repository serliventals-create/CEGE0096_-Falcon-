"""Task 4: implement the Gift Wrapping algorithm in this file.

Read input.csv, use the Task 2 orientation calculation, and write output.csv
in the supplied id,x,y format. Choose your own classes, functions, and APIs.
The point.py and plotter.py helpers are optional and may be adapted.
"""

# TODO: read the input points, preserving their identifiers.
# TODO: implement Gift Wrapping and use your orientation calculation.
# TODO: write the hull vertices to output.csv.
# TODO: optionally visualise your result with the supplied plotting helper.


from orientation import OrientationCheck

points = [
    (10, 0),
    (4, 4),
    (0, 4),
    (4, 0),
    (2, 2)
]

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

print("Convex hull:")
for point in hull:
    print(point)
