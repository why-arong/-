#!/usr/bin/env python

import rospy
import time
from linedetector import LineDetector
from motordriver import MotorDriver

class AutoDrive:
    def __init__(self):
        rospy.init_node('xycar_driver')
        self.line_detector = LineDetector('/usb_cam/image_raw')
        self.driver = MotorDriver('/xycar_motor_msg')
        self.weight_speed = 0.1

    def trace(self):
        angle = self.line_detector.detect_lines()
        self.line_detector.show_images()
        if -4 <= angle <= 4:
            self.driver.drive(angle+90, 127)
        elif -7 <= angle <= 7:
            self.driver.drive(angle+90, 125)
        else:
            self.driver.drive(angle * 2.15 + 90, 117)
        #
        # elif 15 >= angle > 7:
        #     self.driver.drive(angle*2.2+90 +10, 120)
        #
        # elif angle > 15:
        #     self.driver.drive(angle *2.2+90+11, 120)
        #
        # elif -20 <= angle < -7:
        #     self.driver.drive(angle*2.2+90-1, 120)
        #
        # elif angle < -20:
        #     self.driver.drive(angle*2.2+90-12, 120)

    def exit(self):
        print('finished')

if __name__ == '__main__':
    car = AutoDrive()
    time.sleep(2)
    rate = rospy.Rate(10)
    for i in range(20):
        car.driver.drive(92, 150)
        time.sleep(0.1)
    while not rospy.is_shutdown():
        car.trace()
        rate.sleep()
    rospy.on_shutdown(car.exit)



