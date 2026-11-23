# Individual Diary

Name: Liu Chi Kwan Eric

Student number: 26222131

Branch: `c_liu_26222131`

Copy this file as
`individual_diary_c_liu_26222131.md` in `diaries/`.

## Week 4 — Preparation and Familiarisation

### My Contributions

Attended the group's first coursework meeting on 20/10/2026, where we went through the eight core tasks, the marking scheme and the list of permitted packages (matplotlib, numpy, pandas, pyproj, shapely, geopandas, rasterio, Rtree, NetworkX).\
Agreed my responsibilities with the group: Task 6: Highest Point Identification and Task 8 — Shortest path using Naismith's rule (15 marks in total).\
Helped map out the dependencies between tasks.
- Task 6 needs the validated user location from Task 1. Its output, the highest point, is used by Task 7 (the nearest ITN node to the highest point) and by Task 5 (plotting the highest point marker).
- Task 8 needs the two ITN nodes found in Task 7 and the elevation raster. Its output, the route, is used by Task 5 (plotting the route line).

Proposed simple interfaces so we can develop in parallel. Proposed simple interfaces so we can develop in parallel and integrate later:
- Task 6 takes the user's (easting, northing) and returns the highest point as (easting, northing, elevation).
- Task 8 takes the start and end ITN node IDs and returns an ordered list of node IDs, a shapely LineString of the route and the estimated walking time.

Created my individual branch c_liu_26222131 in the group repository and added this diary file to the diaries/ folder.\
Read the template code (main.py, point.py, convex_hull.py, plotter.py) to understand the expected structure, and looked through the provided data (the ITN JSON file and the elevation raster) to see their format and coordinate system.\
Practised the Git workflow in a separate test repository: creating branches, committing, pushing, opening a pull request, merging, and resolving a small merge conflict that I created on purpose.


### Challenges and Learning

I had little previous experience of working with Git in a team. At first, switching branches and keeping my branch up to date with main was confusing. Practising in a test repository helped. I learned to run git pull origin main before starting work and to commit small, clearly described changes.\
My two tasks sit at different points in the workflow, and Task 8 cannot run for real until Task 7 is finished. We decided that each member will start with mock inputs: for Task 8, I will use fixed start and end nodes taken by hand from the ITN data, and switch to the real Task 7 output during integration.\
For Task 6, I learned that reading the whole elevation raster may cause memory problems. Using a rasterio window to read only the area around the user, and then masking the cells outside a 5 km circular buffer, should solve this. I still need to work out how to convert the row and column of the maximum cell back into British National Grid coordinates.\
For Task 8, I reviewed Naismith's rule (walking at 5 km/h, plus 1 minute for every 10 m of ascent, with no extra time for descent). The main difficulty will be that ascent depends on the direction of travel, so a road link needs a different weight in each direction. I think a directed graph in NetworkX can handle this.


### Relevant Commits

Add individual diary for Week 4\
Compile the group diary and upload to github\
No code commits this week, as agreed for the preparation week.


### Plans for Next Week

Task 6: read the elevation raster with a rasterio window around a test point, apply a 5 km circular mask and return the coordinates and elevation of the highest cell. Check the result visually by plotting it.\
Task 8: build a NetworkX graph from the ITN road links and first calculate a simple shortest path by distance. Then add Naismith's rule weights by sampling elevation along each link, using (439619, 85800) as the test starting point.\
Agree with the Task 7 member on the exact node ID format, and with the Task 5 member on how the route will be passed to the map.\
Commit my progress to my branch and update this diary before the next deadline.


## Week 5 — Coursework Development
 
*Date: [7 Nov 2026]*
 
### My Contributions
 
- Started implementing **Task 6 — Highest Point Identification**, following the
  plan from last week. As we agreed, I focused on Task 6 first because Task 7
  (Winnie and Serena) needs the highest point as an input, so finishing it early
  unblocks their work.
- Inspected the elevation raster from Material.zip with rasterio. I printed its
  coordinate system (`src.crs`), cell size (`src.res`) and extent
  (`src.bounds`) and confirmed that it uses British National Grid (EPSG:27700)
  with [CELL SIZE] m cells, which matches the user coordinates from Task 1.
- Created a `HighestPointFinder` class in `[highest_point.py]` with a `find(x, y)`
  method that returns `(easting, northing, elevation)`, matching the interface
  the group agreed in Week 4. The method:
  1. converts the corners of a 10 km × 10 km square around the user into row and
     column indices with `src.index()`, and reads only that part of the raster
     using a rasterio `Window` (to avoid loading the whole raster into memory);
  2. calculates the coordinates of every cell centre from the window transform
     and masks all cells more than 5 km from the user, so the search area is a
     circle rather than a square;
  3. finds the highest remaining cell with `argmax()` and converts its row and
     column back into British National Grid coordinates.
- Tested the method with the suggested test point (439619, 85800), which gave a
  highest point at [EASTING, NORTHING] with an elevation of [ELEVATION] m. I also
  plotted the masked elevation array with matplotlib to check that the search
  area is a circle and that the result sits on the highest area inside it.
- Added docstrings and comments to the class and checked the code against PEP8.

### Challenges and Learning
 
- **Coordinates vs. array positions**: at first I mixed up `(row, col)` with
  `(x, y)`. I learned that rows increase southwards, so the transform's `e` value
  (cell height) is negative and the top of the window is `y + 5000`, not
  `y − 5000`. Getting this wrong placed the window in the wrong area.
- **Square vs. circle**: reading a window gives a square, but the brief asks for
  a 5 km radius. Masking cells by their distance from the user (using
  `np.hypot`) solved this without needing a loop over every cell.
- **No-data cells**: some cells (for example, over the sea) contain a no-data
  value. Reading the raster with `masked=True` makes numpy ignore these cells, so
  they are never chosen as the highest point.
- **Ties**: if several cells share the same maximum value, `argmax()` returns the
  first one. I decided this is acceptable and documented it in the docstring.
- I learned how a rasterio window and its transform work together, and how numpy
  masked arrays can replace loops for this kind of analysis.
### Relevant Commits
 
- [`<hash>`](https://github.com/serliventals-create/CEGE0096_-Falcon-/tree/c_liu_26222131<hash>)
  — Add HighestPointFinder class to read elevation within a window (Task 6)
- [`<hash>`](https://github.com/serliventals-create/CEGE0096_-Falcon-/tree/c_liu_26222131<hash>)
  — Mask cells outside 5 km radius and return highest point (Task 6)
- [`<hash>`](https://github.com/serliventals-create/CEGE0096_-Falcon-/blob/c_liu_26222131/diaries/individual_diary_c_liu_26222131.md)
  — Add Week 5 individual diary entry
### Plans for Next Week
 
- Test Task 6 with more user locations, including points near the edge of the
  allowed box and near the coast, and fix any problems.
- Share the Task 6 output with Winnie and Serena so they can use the real
  highest point for Task 7, and with Winnie for plotting the marker in Task 5.
- Open a pull request to merge Task 6 into `main` after a group member has
  reviewed it.
- Start Task 8: read the ITN JSON file, understand its structure (nodes, road
  links and their coordinates) and build a first NetworkX graph. I plan to get a
  simple shortest-distance route working first, then add Naismith's rule weights.
- Continue committing weekly and update this diary, including during Reading Week.


## Week 6 — Reading Week

*Date: [14 Nov 2026]*

### My Contributions

- Completed a **first full draft of Task 6 — Highest Point Identification**.
  The `HighestPointFinder` class now runs from start to finish: it takes the
  user's `(easting, northing)`, reads only the area around the user, masks cells
  outside the 5 km radius and returns the highest point as
  `(easting, northing, elevation)`.
- Tested the draft with several user locations, not just the suggested test
  point (439619, 85800):
  - points in the middle of the island;
  - points close to the edge of the allowed box from Task 1;
  - points near the coast, where part of the 5 km circle falls over the sea.

  In each case I plotted the masked elevation and the result to check that the
  highest point lies inside the circle and on the highest ground.
- Made the class easier to reuse and test: the raster path and radius are set
  when the object is created (default radius 5000 m), and the elevation data is
  kept as a private attribute in line with the group's OOP guidelines.
- Added error handling for cases where no valid elevation cells are found inside
  the circle, so the program gives a clear message instead of crashing.
- Improved the docstrings and comments and checked the code against PEP8.
- Shared the output format and a sample result with Winnie and Serena so they
  can test Task 7 with a real highest point instead of mock data.

### Challenges and Learning

- **Coastal locations**: near the coast, many cells in the circle are no-data
  (sea). I checked that the masked array ignores these cells, so the highest
  point is always on land. This confirmed that reading the raster with
  `masked=True` was the right decision.
- **Edge of the raster**: for points close to the edge of the allowed box, I
  checked that the 10 km window still fits inside the raster. Because Task 1
  only accepts points at least 5 km from the raster edge, the window never goes
  outside the data, which shows why Task 1 uses that box.
- **Checking correctness**: it is hard to tell whether the highest point is
  correct just from the numbers. Plotting the elevation with the circle and the
  result on top made it much easier to check and to find mistakes.
- Reading Week gave me time to review my Week 5 code. I simplified some steps
  and learned that writing small test cases makes it easier to change code
  without breaking it.

### Relevant Commits

- [`<hash>`](https://github.com/[OWNER]/CEGE0096_[GROUPNAME]/commit/<hash>)
  — Complete first draft of HighestPointFinder (Task 6)
- [`<hash>`](https://github.com/[OWNER]/CEGE0096_[GROUPNAME]/commit/<hash>)
  — Add error handling when no valid elevation cells are found (Task 6)
- [`<hash>`](https://github.com/[OWNER]/CEGE0096_[GROUPNAME]/commit/<hash>)
  — Improve docstrings and PEP8 formatting for Task 6
- [`<hash>`](https://github.com/serliventals-create/CEGE0096_-Falcon-/blob/c_liu_26222131/diaries/individual_diary_c_liu_26222131.md)
  — Add Week 6 individual diary entry

### Plans for Next Week

- Ask a group member (most probably Winnie or Tim) to review the Task 6 code, then open a pull request to
  merge it into `main`.
- Work with Tim to connect Task 1 (user input) to Task 6, so the highest point
  is found from the real user location in `main.py`.
- Start Task 8: read the ITN JSON file, understand its structure (nodes, road
  links and their coordinates) and build a first NetworkX graph.
- Get a simple shortest-distance route working first, using mock start and end
  nodes until Task 7 is ready, then begin adding Naismith's rule weights.
- Continue committing weekly and update this diary.


## Week 7 — Coursework Development

*Date: [21 Nov 2026]*

### My Contributions

- **Completed Task 6 — Highest Point Identification.**
  - Finalised `highest_point.py`. The `HighestPointFinder` class has two public
    methods:
    - `find_highest_point(x, y)` returns `(easting, northing, elevation)` in
      the format agreed with the group;
    - `get_elevation_in_radius(x, y)` returns the masked elevation inside the
      5 km circle and its extent, so Winnie can plot the elevation inside the
      buffer for Task 5.
  - Added a check for invalid search radii, and clipped the reading window to
    the raster so the code also works for points close to the raster edge.
  - Ran the final version on the real elevation raster with the test point
    (439619, 85800). The highest point is at [EASTING, NORTHING] with an
    elevation of [ELEVATION] m, which matches the highest area in my plot.
  - [A group member] reviewed the code, and I merged it into `main` through a
    pull request.
  - As required by the brief, I added a GenAI declaration at the top of the
    file, because I used GenAI (Claude) to help develop the structure of the
    module. I then tested and adapted the code myself.
- **Started Task 8 — Shortest Path using Naismith's rule.**
  - Opened the ITN JSON file and studied its structure: `roadnodes` store each
    node's coordinates, and `roadlinks` store each road's start node, end
    node, length and the list of vertices along the road.
  - Started `shortest_path.py` with a `NaismithCalculator` class that
    calculates walking time: distance at 5 km/h, plus 1 minute for every 10 m
    of ascent (downhill adds no time).
  - Began building the network as a NetworkX directed graph (`DiGraph`), with
    one edge in each direction for every road link.
  - Got a first shortest-distance route working between two hand-picked test
    nodes, as a fallback version before adding the Naismith weights.

### Challenges and Learning

- **Finishing Task 6**: testing with the real raster showed that a point close
  to the raster edge could make the reading window extend past the data.
  Task 1 should stop this from happening, but I clipped the window to the
  raster as well, so Task 6 does not depend completely on another task being
  correct.
- **Why Task 8 needs a directed graph**: Naismith's rule only adds time for
  going uphill. A road that climbs from A to B is slower in that direction
  than from B to A, so one weight per road is not enough. I learned that a
  directed graph solves this by storing a separate edge, and a separate
  walking time, for each direction.
- **Understanding the ITN data**: at first I did not know how the nodes and
  links were connected. Printing a few entries from the JSON file helped me
  see that each link refers to its start and end nodes by id, which is
  exactly what NetworkX needs to build the graph.
- **Working without Task 7**: Task 8 needs the nearest nodes from Task 7,
  which is not finished yet. I picked start and end nodes by hand for
  testing, so I can develop Task 8 now and connect it to Task 7 later.

### Relevant Commits

- [`<hash>`](https://github.com/[OWNER]/CEGE0096_[GROUPNAME]/commit/<hash>)
  — Finalise HighestPointFinder and add get_elevation_in_radius (Task 6)
- [`<hash>`](https://github.com/[OWNER]/CEGE0096_[GROUPNAME]/commit/<hash>)
  — Merge Task 6 into main (pull request #[N])
- [`<hash>`](https://github.com/[OWNER]/CEGE0096_[GROUPNAME]/commit/<hash>)
  — Add NaismithCalculator class (Task 8)
- [`<hash>`](https://github.com/[OWNER]/CEGE0096_[GROUPNAME]/commit/<hash>)
  — Build directed ITN graph and first shortest-distance route (Task 8)
- [`<hash>`](https://github.com/serliventals-create/CEGE0096_-Falcon-/blob/c_liu_26222131/diaries/individual_diary_c_liu_26222131.md)
  — Add Week 7 individual diary entry

### Plans for Next Week

- Task 8: sample the elevation at every vertex of each road link and use it
  to calculate the climb and Naismith walking time in each direction.
- Use NetworkX's Dijkstra algorithm with the walking time as the weight, and
  compare the result with the shortest-distance route.
- Join the road vertices along the route into a shapely `LineString`, so
  Winnie can draw the route on the map for Task 5.
- Test Task 8 with small, hand-made networks where the correct answer is
  known (for example, a short road over a hill and a longer flat detour).
- Agree the node id format with Winnie and Serena, and replace my test nodes
  with their Task 7 output once it is ready.
- Continue committing weekly and update this diary.
