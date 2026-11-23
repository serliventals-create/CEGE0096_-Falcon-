# Group Diary

## Week 7 — Coursework Development

*Group meeting: [20 Nov 2026] ([on Teams])*

### Progress Overview

| Task | Description | Responsible | Status |
|---|---|---|---|
| 1 | User Input / System Output | Tim | Completed |
| 2 | Triplet Orientation | Serena | Completed |
| 3 | Object-Oriented Programming | Everyone | In progress |
| 4 | Convex Hull (Gift Wrapping) | Tim | Completed |
| 5 | Map Plotting | Winnie | Completed |
| 6 | Highest Point Identification | Eric | Completed |
| 7 | Nearest Integrated Transport Network | Winnie, Serena | Started |
| 8 | Shortest Path (Naismith's rule) | Eric | Started |

### Contributions by Member

- **Tim** — Task 1 and Task 4:
  - Completed both of his tasks. Task 1 asks the user for a location and checks
    that it lies inside the allowed box, and Task 4 reads `input.csv`,
    calculates the convex hull with the Gift Wrapping algorithm and writes the
    result to `sample_output.csv`.
  - [Add any other details, e.g. plotting the hull with `plotter.py`.]
- **Serena** — Task 2 and Task 7:
  - Task 2 (triplet orientation) is completed.
  - Started researching Task 7 with Winnie, looking at how to find the nearest
    ITN node using an R-tree spatial index.
- **Winnie** — Task 5 and Task 7:
  - Completed Task 5: the background map with a semi-transparent elevation
    overlay, a colour bar, north arrow, scale bar and legend, and markers for
    the user's location, the highest point and the route.
  - Started researching Task 7 with Serena.
- **Eric** — Task 6 and Task 8:
  - Completed Task 6. Finalised `HighestPointFinder`, which returns the highest
    point as `(easting, northing, elevation)`, and added
    `get_elevation_in_radius()` so the elevation inside the 5 km circle can be
    plotted in Task 5. Tested it on the real elevation raster with the test
    point (439619, 85800). After review, it was merged into `main`.
  - Started Task 8. Studied the structure of the ITN JSON file, wrote a
    `NaismithCalculator` class (5 km/h plus 1 minute per 10 m of ascent),
    began building the network as a directed NetworkX graph, and got a first
    shortest-distance route working between hand-picked test nodes.

### Collaboration and Integration

- Five of the eight tasks are now complete (Tasks 1, 2, 4, 5 and 6), so the
  group can start connecting them in `main.py`.
- Task 6 is ready to be connected to Task 1 (Tim): the validated user location
  from Task 1 is passed straight into `HighestPointFinder`.
- Task 7 (Winnie and Serena) is now the key link in the chain: it needs the
  highest point from Task 6, and Task 8 needs its nearest nodes. Eric shared
  the output format of Task 6 and agreed to use the same node id format as
  the ITN JSON file, so Task 7 and Task 8 can be connected easily.
- Task 5 (Winnie) can already show the user's location and highest point. The
  real route will be added once Task 8 returns a shapely `LineString`.


### Challenges and Decisions

- **Task 7 is on the critical path**: Task 8 cannot be tested end to end until
  Task 7 is finished. We decided that Eric will keep developing Task 8 with
  hand-picked test nodes, while Winnie and Serena focus on Task 7 now that
  their other tasks are complete.
- **Directed graph for Task 8**: Eric explained that Naismith's rule only adds
  time for going uphill, so a road can take longer in one direction than the
  other. The group agreed that Task 8 should use a directed graph with a
  separate walking time for each direction.
- **Robust code**: Eric clipped the Task 6 reading window to the raster, so it
  still works if a point is close to the edge. We agreed that each task
  should check its own inputs, rather than relying completely on earlier tasks.


### Relevant Commits

- [`<hash>`](https://github.com/serliventals-create/CEGE0096_-Falcon-/blob/t_pastron_26266294/main.py)
  — Tim: [commit message for Task 1]
- [`<hash>`](https://github.com/serliventals-create/CEGE0096_-Falcon-/blob/t_pastron_26266294/convex_hull.py)
  — Tim: [commit message for Task 4]
- [`<hash>`](https://github.com/serliventals-create/CEGE0096_-Falcon-/blob/s_liventals_26253036/orientation.py)
  — Serena: [commit message for Task 2]
- [`<hash>`](https://github.com/serliventals-create/CEGE0096_-Falcon-/blob/y_liu_26047534/test_map.py)
  — Winnie: [commit message for Task 5]
- [`<hash>`](https://github.com/serliventals-create/CEGE0096_-Falcon-/blob/c_liu_26222131/highest_point.py)
  — Eric: Finalise HighestPointFinder and add get_elevation_in_radius (Task 6)
- [`<hash>`](https://github.com/serliventals-create/CEGE0096_-Falcon-/blob/main/main.py)
  — Eric: Merge Task 6 into main
- [`<hash>`](https://github.com/serliventals-create/CEGE0096_-Falcon-/blob/c_liu_26222131/shortest_path_1-2.py)
  — Eric: Add NaismithCalculator class (Task 8)


### Plans for Next Week

- **Tim**: help integrate Tasks 1 and 4 into `main.py` and start on the creativity component.
- **Serena and Winnie**: implement Task 7, building an R-tree index of ITN
  nodes and finding the nearest nodes to the user and to the highest point.
- **Winnie**: add the real route from Task 8 to the map once it is ready.
- **Eric**: add elevation sampling along each road link and the Naismith
  weights to Task 8, find the quickest route with Dijkstra's algorithm, and
  return it as a shapely `LineString` for Task 5.
- **Everyone**: agree the final OOP structure for `main.py`, decide whether to
  attempt the creativity component (the presentation must be booked by
  8 January), and continue weekly commits and diary updates.


<!-- Add a dated entry every week, including Reading Week. -->
