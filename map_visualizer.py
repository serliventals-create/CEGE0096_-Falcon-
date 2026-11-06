
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import rasterio

from matplotlib.colors import ListedColormap
from rasterio.enums import Resampling
from rasterio.windows import from_bounds


class MapVisualizer:
    """
    CEGE0096 - Task 5: Map Plotting.

    Create an emergency evacuation map using British
    National Grid coordinates (EPSG:27700).

    AI assistance disclosure:
    Initial structure and plotting implementation were
    developed with ChatGPT assistance. The student should
    review, test and document all adopted code.
    """

    def __init__(
        self,
        background_path,
        elevation_path,
        map_size=20000
    ):
        """
        Initialise the map visualiser.

        Parameters
        ----------
        background_path : str or Path
            OS background raster file.
        elevation_path : str or Path
            Elevation raster file.
        map_size : float
            Width and height of map in metres.
        """
        self.background_path = Path(background_path)
        self.elevation_path = Path(elevation_path)
        self.map_size = float(map_size)
        self.max_pixels = 1200

        if self.map_size <= 0:
            raise ValueError("map_size must be positive.")

        if not self.background_path.is_file():
            raise FileNotFoundError(
                f"Background raster not found: {self.background_path}"
            )

        if not self.elevation_path.is_file():
            raise FileNotFoundError(
                f"Elevation raster not found: {self.elevation_path}"
            )

    def _read_raster(self, raster_path, bounds):
        """
        Read and downsample a raster window.

        bounds: (left, bottom, right, top)

        Returns
        -------
        data, extent, colour_map

        extent is:
        (left, right, bottom, top)
        """

        left, bottom, right, top = bounds

        with rasterio.open(raster_path) as src:
            read_left = max(left, src.bounds.left)
            read_bottom = max(bottom, src.bounds.bottom)
            read_right = min(right, src.bounds.right)
            read_top = min(top, src.bounds.top)

            if (
                read_left >= read_right
                or read_bottom >= read_top
            ):
                raise ValueError(
                    f"Requested map does not overlap {raster_path}"
                )

            window = from_bounds(
                read_left,
                read_bottom,
                read_right,
                read_top,
                transform=src.transform
            )

            width = max(1, int(round(window.width)))
            height = max(1, int(round(window.height)))

            factor = min(
                1.0,
                self.max_pixels / max(width, height)
            )

            output_width = max(1, int(round(width * factor)))
            output_height = max(1, int(round(height * factor)))

            data = src.read(
                1,
                window=window,
                out_shape=(output_height, output_width),
                masked=True,
                resampling=Resampling.nearest
            )

            # Raster window location in BNG metres.
            transform = src.window_transform(window)
            window_bounds = rasterio.windows.bounds(
                window,
                src.transform
            )

            extent = (
                window_bounds[0],
                window_bounds[2],
                window_bounds[1],
                window_bounds[3]
            )

            try:
                colour_map = src.colormap(1)
            except ValueError:
                colour_map = None

            return data, extent, colour_map

    def plot_background(self, ax, bounds):
        """Plot the OS background raster."""

        data, extent, colour_map = self._read_raster(
            self.background_path,
            bounds
        )

        if colour_map:
            max_index = max(colour_map.keys())

            colours = [
                tuple(
                    value / 255.0
                    for value in colour_map.get(
                        i, (0, 0, 0, 255)
                    )
                )
                for i in range(max_index + 1)
            ]

            cmap = ListedColormap(colours)

            ax.imshow(
                data,
                extent=extent,
                origin="upper",
                cmap=cmap,
                vmin=-0.5,
                vmax=max_index + 0.5,
                interpolation="nearest",
                zorder=1
            )

        else:
            ax.imshow(
                data,
                extent=extent,
                origin="upper",
                cmap="gray",
                interpolation="nearest",
                zorder=1
            )

    def plot_elevation(self, ax, bounds, fig):
        """Overlay elevation data and draw a colour bar."""

        data, extent, _ = self._read_raster(
            self.elevation_path,
            bounds
        )

        elevation = np.ma.masked_invalid(
            data.astype(float)
        )

        if elevation.count() == 0:
            raise ValueError(
                "No valid elevation values in the map area."
            )

        image = ax.imshow(
            elevation,
            extent=extent,
            origin="upper",
            cmap="terrain",
            alpha=0.45,
            interpolation="nearest",
            zorder=2
        )

        colour_bar = fig.colorbar(
            image,
            ax=ax,
            shrink=0.75,
            pad=0.02
        )

        colour_bar.set_label("Elevation (m)")

    def plot_points(self, ax, start, highest=None):
        """Plot the start and highest-point markers."""

        ax.scatter(
            start[0],
            start[1],
            color="blue",
            edgecolors="white",
            linewidths=1.5,
            marker="o",
            s=110,
            label="Starting Point",
            zorder=6
        )

        if highest is not None:
            ax.scatter(
                highest[0],
                highest[1],
                color="red",
                edgecolors="white",
                linewidths=1.5,
                marker="^",
                s=150,
                label="Highest Point",
                zorder=6
            )

    def plot_route(self, ax, route=None):
        """Plot an ordered sequence of route coordinates."""

        if route is None:
            return

        route = np.asarray(route, dtype=float)

        if (
            route.ndim != 2
            or route.shape[1] != 2
            or len(route) < 2
        ):
            raise ValueError(
                "route must contain at least two (x, y) points."
            )

        ax.plot(
            route[:, 0],
            route[:, 1],
            color="orange",
            linewidth=3,
            label="Evacuation Route",
            zorder=5
        )

    def add_north_arrow(self, ax):
        """Draw a north arrow in the upper-right corner."""

        ax.annotate(
            "N",
            xy=(0.93, 0.96),
            xytext=(0.93, 0.84),
            xycoords="axes fraction",
            textcoords="axes fraction",
            ha="center",
            va="center",
            fontsize=14,
            fontweight="bold",
            arrowprops=dict(
                arrowstyle="-|>",
                color="black",
                lw=2
            ),
            zorder=10
        )

    def add_scale_bar(self, ax):
        """Draw a 2 km scale bar using BNG metre units."""

        x_min, x_max = ax.get_xlim()
        y_min, y_max = ax.get_ylim()

        width = x_max - x_min
        height = y_max - y_min

        length = 2000.0

        x_start = x_min + 0.08 * width
        y_start = y_min + 0.08 * height

        # White outline for visibility.
        ax.plot(
            [x_start, x_start + length],
            [y_start, y_start],
            color="white",
            linewidth=8,
            zorder=9
        )

        ax.plot(
            [x_start, x_start + length],
            [y_start, y_start],
            color="black",
            linewidth=4,
            zorder=10
        )

        ax.text(
            x_start + length / 2,
            y_start + 0.02 * height,
            "2 km",
            ha="center",
            va="bottom",
            fontsize=11,
            fontweight="bold",
            bbox=dict(
                facecolor="white",
                edgecolor="none",
                alpha=0.8
            ),
            zorder=10
        )

    def add_map_elements(self, ax):
        """Add map labels, north arrow, scale bar and legend."""

        self.add_north_arrow(ax)
        self.add_scale_bar(ax)

        ax.set_xlabel(
            "Easting (m) - British National Grid"
        )
        ax.set_ylabel(
            "Northing (m) - British National Grid"
        )
        ax.set_title(
            "Emergency Evacuation Map - Isle of Wight",
            fontsize=14,
            fontweight="bold"
        )

        ax.legend(
            loc="upper left",
            fontsize=9,
            framealpha=0.9
        )

    def plot_map(
        self,
        start,
        highest=None,
        route=None
    ):
        """
        Generate the complete evacuation map.

        start: (easting, northing)
        highest: optional (easting, northing)
        route: optional ordered list of (easting, northing)

        Returns
        -------
        fig, ax
        """

        x, y = map(float, start)

        half_size = self.map_size / 2.0

        bounds = (
            x - half_size,
            y - half_size,
            x + half_size,
            y + half_size
        )

        fig, ax = plt.subplots(figsize=(11, 9))

        # 1. OS background.
        self.plot_background(ax, bounds)

        # 2. Transparent elevation overlay.
        self.plot_elevation(ax, bounds, fig)

        # 3. Start and highest point.
        self.plot_points(ax, start, highest)

        # 4. Evacuation route.
        self.plot_route(ax, route)

        # 5. Enforce exact 20 km x 20 km geographic extent.
        ax.set_xlim(bounds[0], bounds[2])
        ax.set_ylim(bounds[1], bounds[3])
        ax.set_aspect("equal", adjustable="box")

        # 6. Decorations.
        self.add_map_elements(ax)

        fig.tight_layout()

        return fig, ax
