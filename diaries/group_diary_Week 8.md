# Group Diary

## Week 8 —  (written by Eric)

### Progress Overview

| Task | Description | Responsible | Status |
|---|---|---|---|
| 1 | User Input / System Output | Tim | Completed |
| 2 | Triplet Orientation | Serena | Completed |
| 3 | Object-Oriented Programming | Everyone | Completed |
| 4 | Convex Hull (Gift Wrapping) | Tim | Completed |
| 5 | Map Plotting | Winnie | Completed |
| 6 | Highest Point Identification | Eric | Completed |
| 7 | Nearest Integrated Transport Network | Winnie, Serena | Completed (revising after review) |
| 8 | Shortest Path (Naismith's rule) | Eric | In progress (Parts 1–4 done) |

### Contributions by Member

- **Tim** — Tasks 1 and 4 complete.
  - Reviewed the Task 7 code written by Winnie and Serena and gave feedback.
- **Serena** — Tasks 2 and 7:
  - Task 2 complete.
  - Completed Task 7 with Winnie: finding the ITN node nearest the user and
    the node nearest the highest point.
- **Winnie** — Tasks 5 and 7:
  - Task 5 complete.
  - Completed Task 7 with Serena.
- **Eric** — Tasks 6 and 8:
  - Task 6 complete.
  - Completed Parts 1–4 of Task 8 (`shortest_path.py`):
    - **Part 1**: constants for Naismith's rule (5 km/h, and 1 minute per
      10 m of ascent);
    - **Part 2**: `NaismithCalculator`, which calculates the climb (uphill
      only) and the walking time;
    - **Part 3**: `ITNNetwork`, which samples the elevation along every road
      link and builds a directed graph with a separate walking time for each
      direction;
    - **Part 4**: `RoutePlanner`, which finds the quickest route with
      Dijkstra's algorithm and returns the node list, a shapely `LineString`
      and the walking time.
  - Tested Parts 1–4 on small hand-made networks with known answers (for
    example, the Naismith route avoids a steep hill by taking a longer flat
    detour, while the shortest-distance route goes over the hill).
  - Added explanatory comments before each part of the code.
  - Started Part 5: a manual test that runs the whole chain for the test point
    (439619, 85800).

### Collaboration and Integration

- All tasks are now complete except Task 8, so almost every part of the
  application is ready to be connected in `main.py`.
- **Code review of Task 7**: Tim reviewed the Task 7 code. Serena will update
  it based on his feedback.
- **Connecting Task 7 and Task 8**: Task 7 returns the start and end ITN
  nodes, which are the inputs of Task 8. Eric will replace the temporary
  nearest-node helper in his Part 5 test with the group's Task 7 code, and
  check that the node id format matches.
- **Connecting Task 8 and Task 5**: once Task 8 is finished, its route
  `LineString` will be passed to Winnie's Task 5 map.

### Challenges and Decisions

- **Task 8 is the last core task**: it depends on Task 7 and is needed by
  Task 5, so it is the final step before the full program can run. We decided
  that Eric will continue focusing on Task 8, while the rest of the group
  reviews code and prepares for integration.
- **Reviewing before merging**: the review of Task 7 showed that a second pair
  of eyes is useful. We agreed to keep reviewing each other's code before
  merging into `main`.
- **Creativity component**: with the core tasks nearly finished, we decided to
  hold a group meeting next week to discuss ideas for the creativity part.

### Relevant Commits

- [`<hash>`](https://github.com/serliventals-create/CEGE0096_-Falcon-/blob/s_liventals_26253036/nearest_itn.py)
  — Serena / Winnie: [complete task 7]
- [`<hash>`](https://github.com/serliventals-create/CEGE0096_-Falcon-/blob/s_liventals_26253036/nearest_itn.py)
  — Tim: [review comments on Task 7]
- [`<hash>`](https://github.com/[OWNER]/CEGE0096_[GROUPNAME]/commit/<hash>)
  — Eric: Sample elevation along road links and add Naismith weights (Task 8)
- [`<hash>`](https://github.com/[OWNER]/CEGE0096_[GROUPNAME]/commit/<hash>)
  — Eric: Add RoutePlanner with Dijkstra route and LineString output (Task 8)
- [`<hash>`](https://github.com/[OWNER]/CEGE0096_[GROUPNAME]/commit/<hash>)
  — Eric: Add explanatory comments and docstrings to Task 8
- [`<hash>`](https://github.com/serliventals-create/CEGE0096_-Falcon-/blob/main/diaries/group_diary_Week%208.md)
  — Eric: Group diary (week 8)

### Plans for Next Week

- **Eric**: continue Task 8. Finish Part 5, run the full chain on the real ITN
  and elevation data, connect it to the Task 7 code, and pass the route to
  Winnie for the Task 5 map.
- **Serena**: update the Task 7 code based on Tim's review.
- **Everyone**: hold a group meeting to discuss the creativity component
  (decide whether to attempt it, choose a feature and who will lead the
  presentation, which must be booked by 8 January), and continue weekly
  commits and diary updates.

