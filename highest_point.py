"""Task 6: Highest point identification.

Find the highest point of land within a given radius (5 km by default) of the
user's location, using the elevation raster provided with the coursework.

The search divids into four steps:

1. Read only the square window of the raster that contains the search circle,
   instead of the whole raster, to save memory.
2. Work out the British National Grid coordinates of every cell centre in that
   window and mask the cells that lie further than the radius from the user.
3. Find the cell with the highest remaining elevation value.
4. Convert that cell's position (row, column) back into coordinates.

Output format agreed with the group:
    (easting, northing, elevation)

How the module is organised:
    1. Background     - what a raster is and how cells relate to coordinates.
    2. Set-up         - creating a HighestPointFinder and its properties.
    3. get_elevation_in_radius() - steps 1 and 2 above.
    4. find_highest_point()      - steps 3 and 4 above.
    5. Manual test (run this file directly).

Permitted packages used: numpy, rasterio.

"""

import numpy as np
import rasterio
from rasterio.windows import Window


# ===========================================================================
# PART 1: Background - rasters and coordinates
# ---------------------------------------------------------------------------
# The elevation raster is a large grid (a 2D array). Each cell stores one
# height value in metres and covers a small square of ground (e.g. 5 m x 5 m).
#
#            col 0   col 1   col 2   ...
#   row 0  [ 12.3,   14.1,   15.0, ...]   <- northern edge of the raster
#   row 1  [ 13.0,   16.2,   18.4, ...]
#   ...
#
# There are two ways to describe a position:
#   * array position (row, col) - which row and column of the grid;
#   * map coordinates (x, y)    - easting and northing in metres
#                                 (British National Grid, EPSG:27700).
#
# rasterio links the two with a "transform". The values used here are:
#   transform.c - x (easting) of the top-left corner;
#   transform.f - y (northing) of the top-left corner;
#   transform.a - width of one cell (e.g. 5);
#   transform.e - height of one cell, which is NEGATIVE (e.g. -5), because
#                 the row number goes UP as we move SOUTH (northing goes down).
#
# So the centre of cell (row, col) is at:
#   x = c + (col + 0.5) * a
#   y = f + (row + 0.5) * e
# The "+ 0.5" moves from the cell's corner to its centre.
# ===========================================================================


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

    # =======================================================================
    # PART 2: Set-up
    # -----------------------------------------------------------------------
    # A HighestPointFinder is created once for one elevation raster, and can
    # then be used for any number of user locations.
    #   * raster_path - where the elevation file is stored;
    #   * radius      - how far to search, in metres (5000 m = 5 km by
    #                   default, as required by the brief).
    # The radius is checked straight away: a zero or negative radius makes
    # no sense, so we stop with a clear error instead of failing later.
    #
    # Encapsulation: both values are stored in private attributes (double
    # underscore) and can only be READ through the properties below, so
    # other parts of the program cannot change them by accident.
    # =======================================================================
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

    # =======================================================================
    # PART 3: get_elevation_in_radius() - read and mask the search area
    # -----------------------------------------------------------------------
    # This method prepares the cells we are allowed to search.
    #
    # Step 1 - Read only what we need (a "window"):
    #   The whole raster is large, and reading all of it could use too much
    #   memory. The search circle (radius r) fits inside a square from
    #   (x - r, y - r) to (x + r, y + r), so we read only that square.
    #   src.index(x, y) converts map coordinates into (row, col). The
    #   square's TOP-left corner is (x - r, y + r), because the top of the
    #   raster is the north, where northing is larger.
    #
    #   +-----------------+   <- the square window we read
    #   |   ..ooooo..     |
    #   |  ooooooooooo    |   o = inside the 5 km circle (kept)
    #   |  oooooUoooooo   |   . = corners outside the circle (masked)
    #   |  ooooooooooo    |   U = user's location
    #   |   ..ooooo..     |
    #   +-----------------+
    #
    # Step 2 - Turn the square into a circle:
    #   The corners of the square are further than 5 km away (up to about
    #   7.07 km), so they must not be searched. We work out the coordinates
    #   of every cell centre (formula from Part 1), measure each cell's
    #   distance to the user with Pythagoras (np.hypot), and MASK (hide)
    #   every cell further than r.
    #
    # Masked arrays: a numpy masked array keeps all the values but marks some
    # of them as hidden. Calculations such as max() and argmax() simply skip
    # the hidden cells. Reading with masked=True also hides the raster's own
    # "no data" cells (for example over the sea) automatically.
    #
    # This method is kept separate from find_highest_point() so that Task 5
    # can reuse it to plot the elevation inside the 5 km circle.
    # =======================================================================
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
            # --- Step 1a: find the rows and columns of the square ---------
            # Top-left corner = (x - r, y + r); bottom-right = (x + r, y - r).
            row_top, col_left = src.index(x - r, y + r)
            row_bottom, col_right = src.index(x + r, y - r)

            # --- Step 1b: keep the window inside the raster ---------------
            # If the user is close to the edge, part of the square could lie
            # outside the raster. Task 1 should already prevent this, but we
            # clip the rows and columns to the raster size to be safe.
            row_start, row_stop = max(row_top, 0), min(row_bottom + 1,
                                                       src.height)
            col_start, col_stop = max(col_left, 0), min(col_right + 1,
                                                        src.width)
            if row_start >= row_stop or col_start >= col_stop:
                raise ValueError("The search area is outside the elevation "
                                 "raster.")

            # --- Step 1c: read only this window ---------------------------
            # masked=True hides the raster's no-data cells automatically.
            # window_transform() gives the transform of the window itself,
            # so its top-left corner is the corner of the square we read.
            window = Window.from_slices((row_start, row_stop),
                                        (col_start, col_stop))
            elevation = src.read(1, window=window, masked=True)
            transform = src.window_transform(window)

        # --- Step 2a: coordinates of every cell centre --------------------
        # np.indices gives the row and column number of every cell at once,
        # so we can apply the Part 1 formula to the whole window without a
        # loop. xs and ys have the same shape as the elevation array.
        rows, cols = np.indices(elevation.shape)
        xs = transform.c + (cols + 0.5) * transform.a
        ys = transform.f + (rows + 0.5) * transform.e

        # --- Step 2b: mask every cell further than r from the user --------
        # distance = sqrt((x_cell - x_user)^2 + (y_cell - y_user)^2)
        distance = np.hypot(xs - x, ys - y)
        elevation = np.ma.masked_where(distance > r, elevation)

        # --- Extra: the window's extent, for plotting in Task 5 -----------
        # matplotlib's imshow() needs (left, right, bottom, top) in map
        # coordinates to place the array correctly on the map.
        height, width = elevation.shape
        extent = (transform.c,
                  transform.c + width * transform.a,
                  transform.f + height * transform.e,
                  transform.f)

        return elevation, xs, ys, extent

    # =======================================================================
    # PART 4: find_highest_point() - pick the highest cell
    # -----------------------------------------------------------------------
    # This is the method main.py calls. It uses Part 3 to get the masked
    # cells, then:
    #
    # Check - make sure there is at least one valid cell. count() returns
    #   the number of cells that are NOT masked. If it is 0 (e.g. the whole
    #   circle is sea), we stop with a clear message.
    #
    # Step 3 - find the highest cell:
    #   argmax() returns the position of the largest value, skipping masked
    #   cells. It gives one "flat" number (as if the 2D grid were one long
    #   row), so np.unravel_index() turns it back into (row, col).
    #   Example: in a grid 4 columns wide, flat index 9 = row 2, col 1.
    #
    # Step 4 - convert back to map coordinates:
    #   xs and ys from Part 3 already hold the coordinates of every cell
    #   centre, so we simply look up the values at (row, col).
    #
    # Ties: if several cells share the highest value, argmax() returns the
    # first one it meets, scanning row by row from the north-west corner.
    # =======================================================================
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

        # Check: is there any valid (unmasked) cell left to search?
        if elevation.count() == 0:
            raise ValueError("No valid elevation data was found within "
                             f"{self.__radius} m of ({x}, {y}).")

        # Step 3: argmax ignores masked cells and returns a flat index,
        # which unravel_index turns back into (row, column).
        row, col = np.unravel_index(elevation.argmax(), elevation.shape)

        # Step 4: convert the cell position back into coordinates, and
        # return plain floats so other tasks do not receive numpy types.
        return (float(xs[row, col]),
                float(ys[row, col]),
                float(elevation[row, col]))


# ===========================================================================
# PART 5: Manual test
# ---------------------------------------------------------------------------
# This block only runs when the file is run directly
# (python highest_point.py), not when it is imported by main.py or other
# modules. It finds the highest point for the test location given in the
# brief and prints the result, so the module can be checked on its own.
# ===========================================================================

if __name__ == "__main__":
    # Change RASTER_PATH to the elevation file from Material.zip on your
    # computer.
    RASTER_PATH = "Material/elevation/SZ.asc"
    TEST_POINT = (439619, 85800)  # test point suggested in the brief

    finder = HighestPointFinder(RASTER_PATH)
    easting, northing, height = finder.find_highest_point(*TEST_POINT)
    print(f"User location: {TEST_POINT}")
    print(f"Highest point within {finder.radius / 1000:g} km: "
          f"({easting:.1f}, {northing:.1f}), elevation {height:.1f} m")
