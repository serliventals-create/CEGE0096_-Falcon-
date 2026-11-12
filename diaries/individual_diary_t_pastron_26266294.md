Name: Tim Pastron

Student number: 26266294

Branch: `t_pastron_26266294`


## Week 4 — Preparation and Familiarisation

### My Contributions

- Reviewed coursework requirements, familiarised myself with the project template
- Implemented Task 1 in main.py, which collects the user's easting and northing coordinates and checks whether they fall within the permitted geographical area
 - Began preparing for Task 4 by reading about convex hull and gift wrapping algorithm
 - Set up individual branch on Git and understood how to manage contributions to the project
 

### Challenges and Learning

- Understood relationship between local and cloud versions of Git and how to use commits
- Began to look into convex hull task to gain better understanding

### Relevant Commits

- Task 1 commit in main.py - completed Task 1

### Plans for Next Week

- Continue developing understanding, begin to develop code for convex hull
- Wait for task 2 completion, otherwise use dummy data to set up task 4 beforehand and then complete with real data



## Week 5 

### My Contribution

- Continued work on Task 4 - convex hull. In line with the description, the first step is to identify the outmost points which make up the convex hull. I did this by creating a set of example points to simplify the process, rather than instantly getting convex_hull.py to read the input.csv values.
- The gift wrapping algorithm (Jarvis March) used input from test_orientation.py and orientation.py which provided the function determining whether points are clockwise, anti-clockwise or collinear.
- I developed a while loop which repeatedly selects the next hull point, until the algorithm reads that it has returned to its initial starting point, at which point the loop is stopped (break is called).
- As mentioned, this gift wrapping setup was tested with dummy example points for simplicity. These points also ensured that the wrapping was calculated properly, since one of the points [2,2] was inside the boundary, and therefore should be excluded from the final convex hull.

### Challenges and Learning

- Initally, the algorithm only found the first edge rather than the complete convex hull, because the code was not enclosed within a while loop. Fixing this ensured that all the edges were calculated, before breaking the loop.
- While debugging, I included extra lines of print code so that I could check what was going wrong. This resulted in a rather messy terminal, which I then had to clean up. The final convex hull print was useful to keep, as it confirms that the loop has successfully worked. Once the algorithm is told to read the input.csv file, and instead have an output of a plotter, there may not be any need for this print output, but I will keep it for now. 

### Relevant Commits

- Committed initial copy of my Task 4 - Convex Hull contribution, with following commits building on this work.

### Next Steps

- Next, I will incorporate both input and output files, so that the points for the convex hull can be read from input.csv, and resulting hull can be written to output.csv