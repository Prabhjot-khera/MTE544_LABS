

import numpy as np



# TODO Part 3: Comment the code explaining each part
class kalman_filter:
    
    # TODO Part 3: Initialize the covariances and the states    
    def __init__(self, P,Q,R, x, dt):
        
        self.P= P #np.array(P).reshape(-1, 1)
        self.Q= Q
        self.R= R
        self.x= x # state vector [x, y, th, w, v, vdot]
        self.dt = dt
        
    # TODO Part 3: Replace the matrices with Jacobians where needed        
    def predict(self):

        self.A = self.jacobian_A()
        self.C = self.jacobian_H() #consider moving self.C after self.motion_model maybe if we get issues
        
        self.motion_model()
        
        self.P= np.dot( np.dot(self.A, self.P), self.A.T) + self.Q

    # TODO Part 3: Calculate the Kalman gain and correct your estimates
    def update(self, z):
        
        kalman_gain= self.P @ self.C.T @ np.linalg.inv(self.C @ self.P @ self.C.T + self.R)
        
        self.x= self.x + kalman_gain @ (z - self.measurement_model())
        
        self.P= (np.eye(self.P.shape[1]) - kalman_gain @ self.C) @ self.P # uses number of states for i matrix (second dim of C)
        
    
    # TODO Part 3: Implement here the measurement model
    def measurement_model(self):
        x, y, th, w, v, vdot = self.x
        return np.array([
            v,# v
            w,# w
            vdot, # ax
            v*w, # ay
        ])
        
    # TODO Part 3: Impelment the motion model (state-transition matrice)
    def motion_model(self):
        
        x, y, th, w, v, vdot = self.x
        dt = self.dt
        
        self.x = np.array([
            x + v * np.cos(th) * dt, #x
            y + v * np.sin(th) * dt, #y
            th + w * dt, #th
            w, #th dot
            v  + vdot*dt,#v
            vdot,#accel
        ])
        


    
    def jacobian_A(self):
        x, y, th, w, v, vdot = self.x
        dt = self.dt
        
        return np.array([
            # Columns: current x, y, th, w, v, vdot; rows: next state.
            # x  y                  th   w               v  vdot
            [1, 0, -v*np.sin(th)*dt,  0,  np.cos(th)*dt,    0],  # x
            [0, 1,  v*np.cos(th)*dt,  0,  np.sin(th)*dt,    0],  # y
            [0, 0,                   1, dt,              0,    0],  # th
            [0, 0,                   0,  1,              0,    0],  # w
            [0, 0,                   0,  0,              1,   dt],  # v
            [0, 0,                   0,  0,              0,    1],  # vdot
        ])
    
    
    # TODO Part 3: Implement here the jacobian of the H matrix (measurements)    
    def jacobian_H(self):
        x, y, th, w, v, vdot=self.x
        return np.array([
            #x, y,th, w, v,vdot
            [0,0,0  , 0, 1, 0], # v
            [0,0,0  , 1, 0, 0], # w
            [0,0,0  , 0, 0, 1], # ax
            [0,0,0  , v, w, 0], # ay  # ay = v*w
        ])
        
    # TODO Part 3: return the states here    
    def get_states(self):
        return self.x
