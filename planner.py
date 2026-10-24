# Type of planner
import math 

POINT_PLANNER=0; TRAJECTORY_PLANNER=1
PARABOLA = 0; SIGMOID = 1



class planner:
    def __init__(self, type_):

        self.type=type_

    
    def plan(self, goalPoint=[-1.0, -1.0]):
        
        if self.type==POINT_PLANNER:
            return self.point_planner(goalPoint)
        
        elif self.type==TRAJECTORY_PLANNER:
            return self.trajectory_planner()


    def point_planner(self, goalPoint):
        x = goalPoint[0]
        y = goalPoint[1]
        return x, y

    # TODO Part 6: Implement the trajectories here
    def trajectory_planner(self):
        path = SIGMOID
        trajectory = []
        if path == PARABOLA: 
            x = 0.0
            while x <= 1.5:
                y = x ** 2
                trajectory.append([x, y])
                x += 0.01  
        
        if (path == SIGMOID):
            x = 0.0
            while x <= 2.5:
                sigmoid = 2/(1+math.e**(-2*(x))) - 1
                trajectory.append([x,sigmoid]) 
                x+=0.01

        # the return should be a list of trajectory points: [ [x1,y1], ..., [xn,yn]]
        print(trajectory)
        return trajectory 

if __name__=="__main__":
    _planner = planner(1)
    _planner.plan()


