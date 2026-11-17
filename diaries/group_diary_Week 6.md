## Week 6 — Reading Week (written by Eric)

*Date: [14 Nov 2026]*

### Contributions by Member

- Tim — Task 4 (Convex Hull):
  - Completed reading from `input.csv` and writing the hull points to
    `output.csv`, so the program can now run on any correctly formatted set of
    points. Removed the hard-coded example points from the script and added a
    message telling the user that the hull points have been saved.
  - Tested the Gift Wrapping algorithm on his own randomly generated datasets,
    and on datasets containing duplicate coordinates, multiple collinear points
    and interior points. The algorithm produced the correct hull in all tests.
- Eric — Task 6 (Highest Point Identification):
  - Completed a first full draft of the `HighestPointFinder` class, which reads
    the elevation raster around the user with a rasterio window, masks cells
    outside the 5 km radius and returns the highest point as
    `(easting, northing, elevation)`.
  - Tested it with locations in the middle of the island, near the edge of the
    allowed box and near the coast, and checked the results visually. Added
    error handling for when no valid elevation cells are found.
  - Improved the class design in line with the group's OOP guidelines: the
    raster path and radius (default 5000 m) are set when the object is created,
    and the elevation data is kept as a private attribute. Improved docstrings
    and comments and checked the code against PEP8.
  - Shared the output format and a sample result with Winnie and Serena for
    Task 7.
- Serena — Task 2 (Triplet Orientation) / Task 7:
  - Completed Task 2, the function that determines whether three points are
    colinear, clockwise or counterclockwise.
  - Reviewed Winnie's Task 5 code.
  - Wrote and committed this week's group diary.
  - Started looking into how to complete Task 7 with Winnie.
- Winnie — Task 5 (Map Plotting) / Task 7:
  - Reviewed Serena's Task 2 code during the group meeting and found an error
    in the return values.
  - Started looking into how to complete Task 7 with Serena.

### Collaboration and Integration

- Task 4 is now independent of hard-coded data: it reads `input.csv` and writes
  `output.csv` in the format of `sample_output.csv`, which is how it will be
  assessed with unseen points.
- Task 6 now returns a real highest point in the agreed format, so Task 7 can
  start replacing mock inputs with real data. Task 6 still needs to be connected
  to the user input from Task 1 (Tim) in `main.py`.
- Task 4 uses the orientation function from Task 2 (Serena). [Confirm whether
  Tim's code now calls Serena's function, or still uses its own version.]

### Challenges and Decisions

- **Testing with different data**: Tim tested Task 4 by temporarily changing the
  input file name in the code and changing it back afterwards. This works but is
  easy to forget. We discussed passing the file name as a parameter (with
  `input.csv` as the default), so test files can be used without editing the
  code. [Keep this point only if the group actually discussed it.]
- **Edge cases**: both Tim and Eric found that testing only the "normal" case is
  not enough. Tim tested duplicates, collinear points and interior points for
  the convex hull, and Eric tested coastal and edge locations for the highest
  point. We agreed that every task should be tested with unusual inputs before
  it is merged.
- **Coastal and edge locations in Task 6**: near the coast, many cells inside
  the 5 km circle are sea with no elevation data. Eric confirmed that reading the
  raster as a masked array ignores these cells, so the highest point is always on
  land. He also confirmed that, because Task 1 only accepts points at least 5 km
  from the raster edge, the search area never goes outside the elevation data.
  This showed how Task 1 and Task 6 depend on each other.
- **Reading Week**: there was no lecture this week, but members continued
  working independently and updated their diaries as required.

### Relevant Commits

- [`<hash>`](https://github.com/[OWNER]/CEGE0096_[GROUPNAME]/commit/<hash>)
  — Tim: Convex hull with working input and output CSV
- [`<hash>`](https://github.com/[OWNER]/CEGE0096_[GROUPNAME]/commit/<hash>)
  — Eric: Complete first draft of HighestPointFinder (Task 6)
- [`<hash>`](https://github.com/[OWNER]/CEGE0096_[GROUPNAME]/commit/<hash>)
  — Eric: Add error handling when no valid elevation cells are found (Task 6)
- [`<hash>`](https://github.com/[OWNER]/CEGE0096_[GROUPNAME]/commit/<hash>)
  — Eric: Improve docstrings and PEP8 formatting for Task 6
- [`<hash>`](https://github.com/[OWNER]/CEGE0096_[GROUPNAME]/commit/<hash>)
  — Serena: [commit message]
- [`<hash>`](https://github.com/[OWNER]/CEGE0096_[GROUPNAME]/commit/<hash>)
  — Winnie: [commit message]

### Plans for Next Week

- **Tim**: plot the input points and the convex hull using `plotter.py` to check
  the results visually.
- **Eric**: get Task 6 reviewed and merged into `main`, connect it to Task 1 with
  Tim, and start Task 8 by reading the ITN JSON file into a NetworkX graph.
- **Serena**: begin working on her part of Task 7 and continue learning GitHub.
- **Winnie**: [next steps for Task 5], and begin her part of Task 7.
- **Everyone**: continue weekly commits and diary updates, and start planning how
  the tasks will be integrated in `main.py`.

<!-- Add a dated entry every week, including Reading Week. -->
