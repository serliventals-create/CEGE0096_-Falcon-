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



## Week 6

### My Contribution

- The next step in my convex hull task was to finish off the input.csv and output.csv reading and writing capability, which would allow the program to run with a foreign set of points, given that they were formatted correctly, inside input.csv
- I completed the code, and subsequently was able to remove the example points within the script. On running the code, I could see that the algorithm was correctly reading the input.csv file, as well as providing the hull points in output.csv. I also made a print output, letting the user know that the hull points had been saved to output.csv.
- Importantly, I wanted to test the algorithm on its ability to cope with example datasets. To do this, I generated foreign random data and imported it into the project folder as a .csv file. I then told the program to read this file temporarily, rather than input.csv. After a successful run, I also made sure to repeat the same, with a dataset including duplicate coordinates and multiple collinear points, which can expose edge cases in convex hull implementation. The algorithm also managed to provide the correct outputs for this test, and therefore I was happy that the testing was successful, and the gift wrapping algorithm to calculate the convex hull was working as desired. 

### Challenges and Learning

- Testing the algorithm with example data is a crucial step in the process of writing code, therefore I felt that it was essential to do so. In the process, there are several important steps to make sure that testing happens sucessfully. 
1. The read command had to be modified to the name of the example csv
2. These changes had to be saved
3. The program had to be re-run, and output tested against expected output from the test datasets.
4. Most important - the read input file had to be reverted back to input.csv after testing was complete, so that the program would continue to run in its expected way. 

- The key learning point in this process was understanding the importance of going beyond simply checking whether the algorithm produced a convex hull. I tested whether the algorithm remained reliable when the input data contained duplicates, collinear points, and interior coordinates. 

### Relevant Commits

- Convex hull commit with working input and output csv

### Next Steps

- Now with Task 4 - Convex Hull functioning as desired, I am intereseted at looking into how I can visually represent the hull points, using the plotter.py code, and this is what I will work on next.