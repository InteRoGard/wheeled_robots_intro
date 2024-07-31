from math import *
import numpy as np
from time import sleep

class Odometry:

    def __init__(self, x = 0, y = 0, angle = 0, velocity = 0, 
                 breadth = 0, wheel_rad = 0):
        # Odometry:
        self.x = x
        self.y = y
        self.angle = angle
        self.position = np.array([self.x, self.y, self.angle])
        self.next_pos= np.array([self.x, self.y, self.angle])
        self.dir_matrix = [0, 0, 0]
        self.chord = 0
        self.delta_angle = 0
        # Differential wheeled:
        self.ang_vel = 0
        self.radius = 0
        self.velocity = velocity
        self.breadth = breadth
        self.wheel_rad = wheel_rad
        self.wheel_vel_left = 0
        self.wheel_vel_right = 0

    def set_waypoint(self, next_x, next_y):
        self.next_pos = np.array([next_x, next_y, 0])
        self.chord = sqrt((next_x - self.x)**2 + (next_y - self.y)**2)
        
        self.radius, self.next_pos[2] = arc_radius(self.x, self.y, self.next_pos[0], self.next_pos[1], self.angle)
        self.ang_vel = self.velocity / self.radius

        self.delta_angle = self.next_pos[2] - self.angle
        self.dir_matrix[0] = self.chord * cos(self.angle + self.delta_angle/2)
        self.dir_matrix[1] = self.chord * sin(self.angle + self.delta_angle/2)
        self.dir_matrix[2] = self.next_pos[2]
        
        self.next_pos = self.position + self.dir_matrix

        if self.radius == 0:
            self.wheel_vel_left = self.velocity
            self.wheel_vel_right = self.velocity
        else:
            self.ang_vel = self.velocity / self.radius
            self.wheel_vel_left = self.velocity * (self.radius + self.breadth/2) / self.radius
            self.wheel_vel_right = self.velocity * (self.radius - self.breadth/2) / self.radius

        # return self.wheel_vel_right, self.wheel_vel_left

    def update_position(self, dt = 0.1):
        # dt = 0.1
        self.x += self.velocity * cos(self.angle) * dt
        self.y += self.velocity * sin(self.angle) * dt
        self.angle += self.ang_vel * dt
        # self.x = self.next_pos[0]
        # self.y = self.next_pos[1]
        # self.angle = self.next_pos[2]
        # self.position = self.next_pos

    def distance_to_point(self, next_x, next_y):
        return sqrt((next_x - self.x)**2 + (next_y - self.y)**2)

    # def set_wheel_speeds(self, left_speed, right_speed):
    #     # Assuming the actuators for the wheels are named 'left_wheel_motor' and 'right_wheel_motor'
    #     left_wheel_actuator_id = self.model.actuator('left_wheel_motor').id
    #     right_wheel_actuator_id = self.model.actuator('right_wheel_motor').id
    #     self.data.ctrl[left_wheel_actuator_id] = left_speed
    #     self.data.ctrl[right_wheel_actuator_id] = right_speed
    
    def update_position(self, left_speed, right_speed, dt, wheel_base=0.5):
        v = (left_speed + right_speed) / 2.0
        omega = (right_speed - left_speed) / wheel_base

        self.x += v * cos(self.delta_angle) * dt
        self.y += v * sin(self.delta_angle) * dt
        self.delta_angle += omega * dt

def arc_radius(x1, y1, x2, y2, tangent_angle):
    centre_x = (x1 + x2) / 2
    centre_y = (y1 + y2) / 2
    chord_length = sqrt((x2 - x1)**2 + (y2 - y1)**2)
    chord_angle = atan2(y2 - y1, x2 - x1)
    radius = chord_length / (2 * sin(pi - tangent_angle - abs(chord_angle)))
    return radius, chord_angle*2


def control_robot_to_point(robot, next_x, next_y, treshold=0.1):
    while robot.distance_to_point(next_x, next_y) > treshold:
        robot.update_position()

# print(arc_radius(0, 0, 2, 1, 0))

# robot = Odometry(velocity=1, breadth=0.5, wheel_rad=0.1)
# control_robot_to_point(robot, 2, 1)

