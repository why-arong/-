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
        self.driver = MotorDriver('/xycar_motor_msg')

    def trace(self):
        angle = self.line_detector.detect_lines()
        self.line_detector.show_images()

        if 65 <= angle <= 115:
            self.driver.drive(angle, 150)

        elif 40 <= angle < 65:
            self.driver.drive(angle, 130)

        elif angle < 40:
            self.driver.drive(angle, 122)

        elif 140 >= angle > 115:
            self.driver.drive(angle, 130)
        else:
            =elf.driver.drive(angle, 122)

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
