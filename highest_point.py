"""Task 6: Highest point identification.

Find the highest point of land within a given radius (5 km by default) of the
user's location, using the elevation raster provided with the coursework.

The search works in four steps:

1. Read only the square window of the raster that contains the search circle,
   instead of the whole raster, to save memory.
2. Work out the British National Grid coordinates of every cell centre in that
   window and mask the cells that lie further than the radius from the user.
3. Find the cell with the highest remaining elevation value.
4. Convert that cell's position (row, column) back into coordinates.

Output format agreed with the group:
    (easting, northing, elevation)

Permitted packages used: numpy, rasterio.

"""

import numpy as np
import rasterio
from rasterio.windows import Window


class HighestPointFinder:
    """Find the highest elevation cell within a radius of a location.

    Attributes are kept private and are read through properties, so the
    raster path and search radius cannot be changed by accident after the
    object has been created.

    Example:
        >>> finder = HighestPointFinder("Material/elevation/SZ.asc")
        >>> finder.find_highest_point(439619, 85800)
        (442502.5, 84997.5, 214.0)
    """

    def __init__(self, raster_path, radius=5000):
        """Create a finder for one elevation raster.

        Args:
            raster_path (str): Path to the elevation raster file.
            radius (float): Search radius in metres. Defaults to 5000 (5 km).

        Raises:
            ValueError: If the radius is not a positive number.
        """
        if radius <= 0:
            raise ValueError("The search radius must be a positive number.")
        self.__raster_path = raster_path
        self.__radius = radius

    @property
    def raster_path(self):
        """str: Path to the elevation raster file."""
        return self.__raster_path

    @property
    def radius(self):
        """float: Search radius in metres."""
        return self.__radius

    def get_elevation_in_radius(self, x, y):
        """Return the elevation cells within the radius of a location.

        Cells outside the search circle, and cells with no data (for example
        over the sea), are masked. This method is also useful for Task 5,
        to plot the elevation inside the 5 km buffer.

        Args:
            x (float): Easting of the user's location (British National Grid).
            y (float): Northing of the user's location (British National Grid).

        Returns:
            tuple: (elevation, xs, ys, extent) where
                elevation (numpy.ma.MaskedArray): elevation values, with cells
                    outside the circle or without data masked;
                xs, ys (numpy.ndarray): easting and northing of each cell
                    centre, with the same shape as ``elevation``;
                extent (tuple): (left, right, bottom, top) of the window,
                    ready to pass to ``matplotlib.pyplot.imshow``.

        Raises:
            ValueError: If the search area lies completely outside the raster.
        """
        r = self.__radius

        with rasterio.open(self.__raster_path) as src:
            # Step 1: find the rows and columns of the square around the
            # circle. The top-left corner is (x - r, y + r) because northing
            # gets smaller as the row number gets bigger.
            row_top, col_left = src.index(x - r, y + r)
            row_bottom, col_right = src.index(x + r, y - r)

            # Keep the window inside the raster, in case the point is close
            # to an edge (Task 1 should already prevent this).
            row_start, row_stop = max(row_top, 0), min(row_bottom + 1,
                                                       src.height)
            col_start, col_stop = max(col_left, 0), min(col_right + 1,
                                                        src.width)
            if row_start >= row_stop or col_start >= col_stop:
                raise ValueError("The search area is outside the elevation "
                                 "raster.")

            window = Window.from_slices((row_start, row_stop),
                                        (col_start, col_stop))

            # masked=True hides the raster's no-data cells automatically.
            elevation = src.read(1, window=window, masked=True)
            transform = src.window_transform(window)

        # Step 2: coordinates of every cell centre in the window.
        # transform.a = cell width, transform.e = cell height (negative),
        # transform.c / transform.f = x / y of the window's top-left corner.
        rows, cols = np.indices(elevation.shape)
        xs = transform.c + (cols + 0.5) * transform.a
        ys = transform.f + (rows + 0.5) * transform.e

        # Mask every cell whose centre is further than r from the user.
        distance = np.hypot(xs - x, ys - y)
        elevation = np.ma.masked_where(distance > r, elevation)

        height, width = elevation.shape
        extent = (transform.c,
                  transform.c + width * transform.a,
                  transform.f + height * transform.e,
                  transform.f)

        return elevation, xs, ys, extent

    def find_highest_point(self, x, y):
        """Find the highest point within the radius of a location.

        If several cells share the highest value, the first one found
        (scanning from the north-west, row by row) is returned.

        Args:
            x (float): Easting of the user's location (British National Grid).
            y (float): Northing of the user's location (British National Grid).

        Returns:
            tuple: (easting, northing, elevation) of the centre of the highest
            cell, as floats.

        Raises:
            ValueError: If there are no valid elevation cells in the circle.
        """
        elevation, xs, ys, _ = self.get_elevation_in_radius(x, y)

        if elevation.count() == 0:
            raise ValueError("No valid elevation data was found within "
                             f"{self.__radius} m of ({x}, {y}).")

        # Step 3: argmax ignores masked cells and returns a flat index,
        # which unravel_index turns back into (row, column).
        row, col = np.unravel_index(elevation.argmax(), elevation.shape)

        # Step 4: convert the cell position back into coordinates.
        return (float(xs[row, col]),
                float(ys[row, col]),
                float(elevation[row, col]))


if __name__ == "__main__":
    # Quick manual test. Change RASTER_PATH to the elevation file from
    # Material.zip on your computer.
    RASTER_PATH = "Material/elevation/SZ.asc"
    TEST_POINT = (439619, 85800)  # test point suggested in the brief

    finder = HighestPointFinder(RASTER_PATH)
    easting, northing, height = finder.find_highest_point(*TEST_POINT)
    print(f"User location: {TEST_POINT}")
    print(f"Highest point within {finder.radius / 1000:g} km: "
          f"({easting:.1f}, {northing:.1f}), elevation {height:.1f} m")
