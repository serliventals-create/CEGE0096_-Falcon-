"""Task 8: Shortest path using Naismith's rule.

Find the quickest walking route along the Integrated Transport Network (ITN)
from the node nearest the user to the node nearest the highest point.

Naismith's rule:
    * a reasonably fit person walks at 5 km/h;
    * one extra minute is added for every 10 m of climb (ascent only,
      descent adds no time).

Because climbing only counts uphill, walking a road from A to B can take a
different time from walking it from B to A. The network is therefore built as
a directed graph (networkx.DiGraph) with one edge in each direction, and each
edge has its own Naismith weight.

The climb on each road link is worked out from the elevation at every vertex
along the link (not only at its two end nodes), so ups and downs in the
middle of a link are counted.

Expected ITN JSON structure (as in the coursework data):
    {
      "roadnodes": {"<node id>": {"coords": [x, y]}, ...},
      "roadlinks": {"<link id>": {"start": "<node id>",
                                  "end": "<node id>",
                                  "length": <metres>,
                                  "coords": [[x, y], [x, y], ...]}, ...}
    }

Output format agreed with the group:
    (list of node ids, shapely LineString of the route, walking time in min)

How the module is organised:
    1. Constants        - the two numbers in Naismith's rule.
    2. NaismithCalculator - turns distance and climb into walking time.
    3. ITNNetwork       - reads the ITN data and builds the directed graph.
    4. RoutePlanner     - finds the quickest route on that graph.
    5. Testing helper and manual test (run this file directly).

Permitted packages used: json, math, numpy, rasterio, shapely, networkx.

"""

import json
import math

import networkx as nx
import numpy as np
import rasterio
from shapely.geometry import LineString


# ===========================================================================
# PART 1: Constants for Naismith's rule
# ---------------------------------------------------------------------------
# Naismith's rule has two parts, so we store two numbers:
#   * Walking speed: 5 km/h = 5000 m / 60 min, i.e. about 83.3 m per minute.
#     Dividing a distance in metres by this gives the walking time in minutes.
#   * Climbing penalty: 1 minute per 10 m of ascent = 0.1 minute per metre.
# Keeping them as named constants (instead of typing 83.3 or 0.1 inside the
# code) makes the code easier to read and to change.
# ===========================================================================

WALKING_SPEED_M_PER_MIN = 5000 / 60   # 5 km/h in metres per minute
MINUTES_PER_METRE_CLIMB = 1 / 10      # 1 minute for every 10 m of ascent


# ===========================================================================
# PART 2: NaismithCalculator
# ---------------------------------------------------------------------------
# This part does the arithmetic of Naismith's rule and nothing else.
# It answers two questions:
#   1. "How much did I climb?"  -> ascent()
#      Given the heights along a road in walking order, add up only the
#      rises. For example, heights 10 -> 15 -> 12 -> 20 m give rises of
#      +5, -3 and +8. The -3 is downhill, so it is ignored:
#      total climb = 5 + 8 = 13 m.
#   2. "How long will it take?" -> walking_time()
#      time = distance / speed + climb x 0.1
#      e.g. 1000 m with 20 m of climb = 12 min + 2 min = 14 min.
# Keeping this in its own class means the rule can be tested on its own,
# and the speed or penalty could be changed without touching the graph code.
# ===========================================================================

class NaismithCalculator:
    """Calculate walking time with Naismith's rule."""

    def __init__(self, speed_m_per_min=WALKING_SPEED_M_PER_MIN,
                 minutes_per_metre_climb=MINUTES_PER_METRE_CLIMB):
        """Create a calculator.

        Args:
            speed_m_per_min (float): Walking speed on flat ground, in metres
                per minute. Defaults to 5 km/h.
            minutes_per_metre_climb (float): Extra minutes per metre of
                ascent. Defaults to 1 minute per 10 m.
        """
        self.__speed = speed_m_per_min
        self.__climb_rate = minutes_per_metre_climb

    @staticmethod
    def ascent(elevations):
        """Return the total climb (metres) along a sequence of elevations.

        Only the uphill parts are added; downhill parts count as zero.
        Missing values (NaN, e.g. no data) are ignored.

        Example:
            >>> NaismithCalculator.ascent([10, 15, 12, 20])
            13.0
        """
        # Remove missing heights (NaN) so they do not break the calculation.
        values = np.asarray(elevations, dtype=float)
        values = values[~np.isnan(values)]
        if values.size < 2:
            return 0.0
        # np.diff gives the change in height between each pair of
        # neighbouring points; keep only the positive changes (uphill).
        rises = np.diff(values)
        return float(rises[rises > 0].sum())

    def walking_time(self, length, ascent):
        """Return the walking time in minutes.

        Args:
            length (float): Horizontal distance in metres.
            ascent (float): Total climb in metres.
        """
        # Flat walking time + extra time for climbing.
        return length / self.__speed + ascent * self.__climb_rate
