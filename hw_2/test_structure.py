import mujoco
# import mujoco_viewer
import numpy as np
import math
from IPython.display import display, Video
from pathlib import Path
import enum

class Resolution(enum.Enum):
            SD = (480, 640)
            HD = (720, 1280)
            UHD = (2160, 3840)

class StretchRobot:
    def __init__(self):
        model_dir = Path("mujoco_menagerie/hello_robot_stretch") # You could also use google_robot
        model_xml = model_dir / "scene.xml"
        # Load model.
        self.model = mujoco.MjModel.from_xml_path(str(model_xml))

        # self.model = mujoco.MjModel.from_xml_path(model_path)
        self.data = mujoco.MjData(self.model)
        # self.renderer = mujoco.Renderer(self.model)
        # self.viewer = mujoco_viewer.MujocoViewer(self.model, self.data)
        
        # Инициализация расчетных координат робота
        self.x = 0.0
        self.y = 0.0
        self.theta = 0.0

        self.vis = mujoco.MjvOption()
        self.vis.geomgroup[2] = True
        self.vis.geomgroup[3] = False

        self.camera = mujoco.MjvCamera()
        mujoco.mjv_defaultFreeCamera(self.model, self.camera)
        self.camera.distance = 4

        duration = 10
        fps = 30
        nsteps = int(np.ceil(duration / self.model.opt.timestep))

        # Set the desired control point.
        if self.model.nkey > 0:
            mujoco.mj_resetDataKeyframe(model, data, 0)
            ctrl0 = self.data.ctrl.copy()
        else:
            mujoco.mj_resetData(self.model, self.data)
            ctrl0 = np.mean(self.model.actuator_ctrlrange, axis=1)

        res = Resolution.SD
        h, w = res.value
        
        self.model.vis.global_.offheight = h
        self.model.vis.global_.offwidth = w

        self.renderer = mujoco.Renderer(self.model, height=h, width=w)

    def set_wheel_speeds(self, left_speed, right_speed):
        # Assuming the actuators for the wheels are named 'left_wheel_motor' and 'right_wheel_motor'
        # left_wheel_actuator_id = self.model.actuator('left_wheel_motor').id
        # right_wheel_actuator_id = self.model.actuator('right_wheel_motor').id
        # self.data.ctrl[left_wheel_actuator_id] = left_speed
        # self.data.ctrl[right_wheel_actuator_id] = right_speed
        self.data.joint('joint_right_wheel').qvel = np.array([right_speed])
        self.data.joint('joint_left_wheel').qvel = np.array([left_speed])
    
    def update_position(self, left_speed, right_speed, dt, wheel_base=0.5):
        v = (left_speed + right_speed) / 2.0
        omega = (right_speed - left_speed) / wheel_base

        self.x += v * math.cos(self.theta) * dt
        self.y += v * math.sin(self.theta) * dt
        self.theta += omega * dt

    def distance_to_point(self, x_goal, y_goal, x, y):
        return math.sqrt((x_goal - x) ** 2 + (y_goal - y) ** 2)
    
    def control_robot_to_point(self, x_goal, y_goal, v, omega, dt, threshold=0.1):
        x = self.x
        y = self.y
        while self.distance_to_point(x_goal, y_goal, x, y) > threshold:
            distance = self.distance_to_point(x_goal, y_goal, self.x, self.y)
            x = self.x
            y = self.y
            angle_to_goal = math.atan2(y_goal - y, x_goal - x)
            angle_diff = angle_to_goal - self.theta
            
            if angle_diff > math.pi:
                angle_diff -= 2 * math.pi
            elif angle_diff < -math.pi:
                angle_diff += 2 * math.pi
            
            v_left = v - omega * angle_diff
            v_right = v + omega * angle_diff
            
            self.set_wheel_speeds(v_left, v_right)
            self.update_position(v_left, v_right, dt)
            mujoco.mj_step(self.model, self.data)
            if len(frames) < self.data.time * 30:
                self.renderer.update_scene(self.data, self.camera, scene_option=self.vis)
                vispix = self.renderer.render().copy().astype(np.float32)
                frame = vispix.astype(np.uint8)
                frames.append(frame)
            # Render the frame
            # self.viewer.render()

        self.set_wheel_speeds(0, 0)
        print("Reached the goal and stopped.")

# Initialize the robot
robot = StretchRobot()
frames = []
# Set the target position (end of the chord)
x_goal, y_goal = 4, 3

# Define the speed parameters
v = 0.5  # Linear speed (m/s)
omega = 0.1  # Angular speed (rad/s)
dt = 0.1  # Time step (s)

# Control the robot to the target point
robot.control_robot_to_point(x_goal, y_goal, v, omega, dt)
