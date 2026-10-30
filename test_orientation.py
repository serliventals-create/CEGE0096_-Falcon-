from orientation import OrientationCheck

#collinear
assert OrientationCheck.orientation((0,0), (14,14), (7,7)) == 0 

#clockwise
assert OrientationCheck.orientation((0,0), (14,14), (28,7)) == 1

#counterclockwise 
assert OrientationCheck.orientation((0,0), (14,14), (7,28)) == -1

#horizontal line
assert OrientationCheck.orientation((0,0), (14,0), (28,0)) == 0

#vertical line 
assert OrientationCheck.orientation((0,0), (0,14), (0,28)) == 0
