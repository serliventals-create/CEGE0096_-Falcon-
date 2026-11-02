#Task 2

class OrientationCheck():

    '''Returns: 
        0: Collinear
        1: Clockwise
        2: Counterclockwise'''
    
    @staticmethod
    def orientation(p, q, r):
        a = q[1] - p[1]
        b = r[0] - q[0]
        c = q[0] - p[0]
        d = r[1] - q[1]

        val = a*b - c*d

        if val == 0:
            return 0
        elif val > 0:
            return 1
        else: 
            return -1 