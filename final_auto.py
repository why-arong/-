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
        self.weight_speed = 0.1

    def trace(self):
        # '- ' mean left, '+ 'mean right
        angle = self.line_detector.detect_lines()
        self.line_detector.show_images()
        float_angle = angle - int(angle)
        if -4 <= angle <= 4:
            self.driver.drive(angle + 90, 125)

        elif -6 <= angle <= 6:
            self.driver.drive(angle + 90, 123)

        elif 15 >= angle > 6:
            wighted_angle = int(angle * 2.1)
            for a in range(int(angle) + 90, wighted_angle + 90):
                self.driver.drive(a + float_angle + 2, 111)
        elif angle > 15:
            wighted_angle = int(angle * 1.8)
            for a in range(int(angle) + 90, wighted_angle + 90):
                self.driver.drive(a + float_angle, 110)

        elif -20 <= angle < -6:
            wighted_angle = int(angle * 2.1)
            for a in range(int(angle) + 87, wighted_angle + 90, -1):
                self.driver.drive(a + float_angle - 12, 111)
        elif angle < -20:
            wighted_angle = int(angle * 1.8)
            for a in range(int(angle) + 85, wighted_angle + 90, -1):
                self.driver.drive(a + float_angle -10, 110)

    def exit(self):
        print('finished')


if __name__ == '__main__':
    car = AutoDrive()
    time.sleep(2)
    rate = rospy.Rate(10)
    #for i in range(5):
     #   for count in range(20):
      #      car.driver.drive(90, 120 + count)
       #     time.sleep(0.01)
    while not rospy.is_shutdown():
        car.trace()
        rate.sleep()
    rospy.on_shutdown(car.exit)
