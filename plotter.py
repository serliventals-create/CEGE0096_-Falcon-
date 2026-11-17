"""Optional hull visualisation helper; students may adapt or replace it."""

import matplotlib.pyplot as plt


class Plotter:
    """Plot lists of point-like objects exposing x and y attributes."""

    def __init__(self, points, hull, title="Convex Hull Visualization"):
        self.points = points
        self.hull = hull
        self.title = title

    def plot(self):
        x_points = [p[0] for p in self.points]
        y_points = [p[1] for p in self.points]

        # Close the hull for display, without changing the original list.
        hull_points = self.hull + [self.hull[0]] if self.hull else []
        x_hull = [p[0] for p in hull_points]
        y_hull = [p[1] for p in hull_points]

        plt.figure(figsize=(8, 8))
        plt.scatter(x_points, y_points, label="Points", color="blue")
        plt.plot(x_hull, y_hull, "r-", label="Convex Hull", lw=2)

        for point in self.points:
            plt.annotate(
                f"({int(point[0])},{int(point[1])})",
                point,
                textcoords="offset points",
                xytext=(0, 5),
                ha="center",
            )

        plt.title(self.title)
        plt.xlabel("X")
        plt.ylabel("Y")
        plt.legend()
        plt.grid(True)
        plt.show()
