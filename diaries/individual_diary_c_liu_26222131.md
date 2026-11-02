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
- Task 6 needs the validated user location from Task 1. Its output, the highest point, is used by Task 7 (the nearest ITN node to the highest point) and by Task 5 (plotting the highest point marker).\
- Task 8 needs the two ITN nodes found in Task 7 and the elevation raster. Its output, the route, is used by Task 5 (plotting the route line).\

Proposed simple interfaces so we can develop in parallel. Proposed simple interfaces so we can develop in parallel and integrate later:
- Task 6 takes the user's (easting, northing) and returns the highest point as (easting, northing, elevation).\
- Task 8 takes the start and end ITN node IDs and returns an ordered list of node IDs, a shapely LineString of the route and the estimated walking time.\

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
