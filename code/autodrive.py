#!/usr/bin/env python

import rospy
import time
from linedetector import LineDetector
from obstacledetector import ObstacleDetector
from motordriver import MotorDriver


class AutoDrive:

    def __init__(self):
        rospy.init_node('xycar_driver')
        self.line_detector = LineDetector('/usb_cam/image_raw')
        # self.obstacle_detector = ObstacleDetector('/ultrasonic')
        self.driver = MotorDriver('/xycar_motor_msg')

    def trace(self):
        # obs_m = self.obstacle_detector.get_distance()
        angle = self.line_detector.detect_lines()
        self.line_detector.show_images()
        if 80 <= angle <= 100:
            self.driver.drive(90, 130)
        elif 60  <= angle < 80:
            self.driver.drive(50, 125)
        elif 50 <= angle < 60:
            self.driver.drive(30, 120)
        elif angle < 50:
            self.driver.drive(20, 120)
        elif 100 < angle <= 120:
            self.driver.drive(130, 125)
        elif 120 < angle <= 130:
            self.driver.drive(150, 120)
        elif 130 < angle:
            self.driver.drive(170, 20)
        # else:
        #     print('tttttttttttttttttuuuuuuuurrrrrn')
    def exit(self):
        print('finished')


if __name__ == '__main__':
    car = AutoDrive()
    time.sleep(2)
    rate = rospy.Rate(10)
    while not rospy.is_shutdown():
        car.trace()
        rate.sleep()
    rospy.on_shutdown(car.exit)
