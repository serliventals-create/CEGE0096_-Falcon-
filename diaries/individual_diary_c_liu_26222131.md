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
 
- [`<hash>`](https://github.com/[OWNER]/CEGE0096_[GROUPNAME]/commit/<hash>)
  — Add HighestPointFinder class to read elevation within a window (Task 6)
- [`<hash>`](https://github.com/[OWNER]/CEGE0096_[GROUPNAME]/commit/<hash>)
  — Mask cells outside 5 km radius and return highest point (Task 6)
- [`<hash>`](https://github.com/[OWNER]/CEGE0096_[GROUPNAME]/commit/<hash>)
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
