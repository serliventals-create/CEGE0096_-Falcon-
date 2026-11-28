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


# ===========================================================================
# PART 3: ITNNetwork
# ---------------------------------------------------------------------------
# This class turns the ITN JSON file into a graph that networkx can search.
#
# What is in the ITN data?
#   * Road nodes: junctions and road ends, each with an (x, y) position.
#   * Road links: the roads between two nodes. Each link has a start node,
#     an end node, a length and a list of vertices ("coords") that trace
#     the shape of the road.
#
# Why a DIRECTED graph?
#   Naismith's rule only adds time for going UP. If a road climbs 50 m from
#   A to B, walking A -> B costs 5 extra minutes, but walking B -> A is
#   downhill and costs nothing extra. An ordinary (undirected) graph can
#   store only one weight per road, so we use nx.DiGraph and add two edges
#   per road: A -> B and B -> A, each with its own walking time.
#
# How the graph is built (three steps):
#   Step 1  __sample_elevations: look up the height of every vertex of every
#           road in the elevation raster.
#   Step 2  __build_graph: for each road, calculate the climb and walking
#           time in both directions.
#   Step 3  add both edges to the graph, storing the time as the weight that
#           the route search will minimise.
# ===========================================================================

class ITNNetwork:
    """Build a directed walking network from the ITN JSON file.

    Each road link becomes two edges (one per direction). Every edge stores:
        * ``length``: horizontal length in metres;
        * ``ascent``: climb in metres in that direction;
        * ``time``: Naismith walking time in minutes;
        * ``coords``: the link's vertices, ordered in that direction;
        * ``fid``: the original road link id.
    """

    # -----------------------------------------------------------------------
    # Set-up: read the JSON file and build the graph straight away, so a new
    # ITNNetwork object is ready to use as soon as it is created.
    # -----------------------------------------------------------------------
    def __init__(self, itn_json_path, elevation_path,
                 calculator=None):
        """Load the ITN data and build the graph.

        Args:
            itn_json_path (str): Path to the ITN JSON file.
            elevation_path (str): Path to the elevation raster file.
            calculator (NaismithCalculator): Optional calculator, mainly for
                testing. A default one is created if not given.
        """
        self.__calculator = calculator or NaismithCalculator()
        with open(itn_json_path, "r") as file:
            itn = json.load(file)
        self.__nodes = itn["roadnodes"]
        self.__links = itn["roadlinks"]
        self.__graph = self.__build_graph(elevation_path)

    # -----------------------------------------------------------------------
    # Read-only access: the attributes above are private (double
    # underscore), so other classes read them through these properties and
    # cannot change them by accident (encapsulation).
    # -----------------------------------------------------------------------
    @property
    def graph(self):
        """networkx.DiGraph: The directed walking network."""
        return self.__graph

    @property
    def nodes(self):
        """dict: ITN node id -> {"coords": [x, y]}."""
        return self.__nodes

    # -----------------------------------------------------------------------
    # Step 1: find the height of every road vertex.
    # Instead of opening the raster once per road (slow), we collect ALL
    # vertices of ALL roads into one long list, ask rasterio for their
    # heights in one go, and then cut the long list of heights back into
    # one piece per road. "counts" remembers how many vertices each road
    # has, so we know where to cut.
    # -----------------------------------------------------------------------
    def __sample_elevations(self, elevation_path):
        """Sample the elevation at every vertex of every road link.

        All vertices are sampled in one pass with ``rasterio.sample``, which
        is much faster than opening the raster once per link and avoids
        loading the whole raster into memory.

        Returns:
            dict: link id -> numpy array of elevations (NaN for no data).
        """
        # Put every vertex of every road into one list.
        link_ids = list(self.__links)
        all_coords = []
        counts = []
        for fid in link_ids:
            coords = self.__links[fid]["coords"]
            all_coords.extend((c[0], c[1]) for c in coords)
            counts.append(len(coords))

        # Look up all the heights at once. sample() returns one value per
        # band for each point; the elevation raster has one band, so v[0].
        with rasterio.open(elevation_path) as src:
            nodata = src.nodata
            values = np.array([v[0] for v in src.sample(all_coords)],
                              dtype=float)
        # Mark "no data" cells as NaN so ascent() can skip them.
        if nodata is not None:
            values[values == nodata] = np.nan

        # Cut the long list of heights back into one array per road.
        elevations = {}
        start = 0
        for fid, count in zip(link_ids, counts):
            elevations[fid] = values[start:start + count]
            start += count
        return elevations

    # -----------------------------------------------------------------------
    # Backup length calculation: if a road has no "length" value in the
    # JSON, add up the straight-line distances between its vertices.
    # -----------------------------------------------------------------------
    @staticmethod
    def __line_length(coords):
        """Return the length of a polyline in metres."""
        return sum(math.dist(coords[i], coords[i + 1])
                   for i in range(len(coords) - 1))

    # -----------------------------------------------------------------------
    # Steps 2 and 3: build the graph.
    # For every road we create two edges:
    #   * forward  (start -> end): vertices and heights in the stored order;
    #   * backward (end -> start): the same vertices and heights REVERSED.
    # Reversing the heights turns uphill into downhill and vice versa, so
    # ascent() automatically gives a different climb for each direction.
    # The walking time is saved as the edge attribute "time", which the
    # route search in Part 4 will minimise.
    # -----------------------------------------------------------------------
    def __build_graph(self, elevation_path):
        """Create the directed graph with Naismith weights on each edge."""
        elevations = self.__sample_elevations(elevation_path)
        graph = nx.DiGraph()

        # Add every road node, remembering its position.
        for node_id, node in self.__nodes.items():
            graph.add_node(node_id, coords=tuple(node["coords"]))

        # Add two edges (one per direction) for every road link.
        for fid, link in self.__links.items():
            coords = [tuple(c) for c in link["coords"]]
            length = link.get("length") or self.__line_length(coords)
            heights = elevations[fid]

            # Forward direction: start -> end, vertices in stored order.
            # Backward direction: end -> start, vertices reversed.
            directions = (
                (link["start"], link["end"], coords, heights),
                (link["end"], link["start"], coords[::-1], heights[::-1]),
            )
            for u, v, edge_coords, edge_heights in directions:
                ascent = self.__calculator.ascent(edge_heights)
                time = self.__calculator.walking_time(length, ascent)
                # If two links join the same pair of nodes, keep the
                # quicker one, as that is the one a walker would use.
                if graph.has_edge(u, v) and graph[u][v]["time"] <= time:
                    continue
                graph.add_edge(u, v, fid=fid, length=length, ascent=ascent,
                               time=time, coords=edge_coords)
        return graph


# ===========================================================================
# PART 4: RoutePlanner
# ---------------------------------------------------------------------------
# This class searches the graph built in Part 3 for the best route.
#
# How is the "best" route found?
#   networkx.dijkstra_path() uses Dijkstra's algorithm: starting from the
#   start node, it keeps extending the cheapest route found so far until it
#   reaches the end node. "Cheapest" means the smallest total of the edge
#   attribute we choose:
#     * weight="time"   -> quickest route by Naismith's rule (default);
#     * weight="length" -> shortest distance, ignoring hills (the simpler
#                          fallback mentioned in the brief, and useful for
#                          comparison).
#
# What does it return?
#   1. the list of node ids along the route;
#   2. the route as a shapely LineString, made by joining the vertices of
#      each road on the route, so Task 5 can draw it on the map;
#   3. the total walking time in minutes.
# ===========================================================================

class RoutePlanner:
    """Find the quickest route between two ITN nodes."""

    def __init__(self, network):
        """Create a planner for an ``ITNNetwork``."""
        self.__network = network

    # -----------------------------------------------------------------------
    # Main method: check the two nodes exist, run Dijkstra's algorithm, then
    # build the route line and add up the walking time.
    # -----------------------------------------------------------------------
    def shortest_path(self, start_node, end_node, weight="time"):
        """Find the best route between two ITN nodes.

        Args:
            start_node (str): ITN node id nearest the user (from Task 7).
            end_node (str): ITN node id nearest the highest point (Task 7).
            weight (str): ``"time"`` for Naismith's rule (default), or
                ``"length"`` for the shortest distance only.

        Returns:
            tuple: (path, route, total_time) where
                path (list): ordered ITN node ids along the route;
                route (shapely.geometry.LineString): the route geometry;
                total_time (float): Naismith walking time in minutes.

        Raises:
            ValueError: If a node is not in the network, or no route exists.
        """
        # Give a clear message if Task 7 passes a node that does not exist.
        graph = self.__network.graph
        for node in (start_node, end_node):
            if node not in graph:
                raise ValueError(f"Node {node} is not in the ITN network.")

        # Find the route with the smallest total weight.
        try:
            path = nx.dijkstra_path(graph, start_node, end_node,
                                    weight=weight)
        except nx.NetworkXNoPath:
            raise ValueError(f"No route found from {start_node} to "
                             f"{end_node}.") from None

        # Turn the list of nodes into a line, and add up the edge times.
        route = self.__build_route_line(path)
        total_time = sum(graph[u][v]["time"]
                         for u, v in zip(path[:-1], path[1:]))
        return path, route, total_time

    # -----------------------------------------------------------------------
    # Build the route line: the node list only gives the junctions, but the
    # roads between them can bend. So we take each edge's own vertices
    # (already stored in the right direction in Part 3) and join them end
    # to end. The first vertex of each edge after the first is skipped,
    # because it is the same point as the last vertex of the previous edge.
    # -----------------------------------------------------------------------
    def __build_route_line(self, path):
        """Join the coordinates of each edge along the path into one line."""
        graph = self.__network.graph
        # Special case: start and end are the same node, so there is no
        # road to walk. A LineString needs two points, so repeat the node.
        if len(path) == 1:
            point = graph.nodes[path[0]]["coords"]
            return LineString([point, point])

        coords = []
        for u, v in zip(path[:-1], path[1:]):
            edge_coords = graph[u][v]["coords"]
            # Skip the first vertex after the first edge, because it is the
            # same as the last vertex of the previous edge.
            coords.extend(edge_coords if not coords else edge_coords[1:])
        return LineString(coords)

    # -----------------------------------------------------------------------
    # Summary for printing or the map legend: total distance, total climb
    # and total time of a route.
    # -----------------------------------------------------------------------
    def route_summary(self, path):
        """Return total length (m), total ascent (m) and time (min)."""
        graph = self.__network.graph
        edges = [graph[u][v] for u, v in zip(path[:-1], path[1:])]
        return (sum(e["length"] for e in edges),
                sum(e["ascent"] for e in edges),
                sum(e["time"] for e in edges))
