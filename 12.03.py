#!/usr/bin/env python

import rospy
import time
from linedetector import LineDetector
from motordriver import MotorDriver
from obstacledetector import ObstacleDetector


class AutoDrive:
    def __init__(self):
        rospy.init_node('xycar_driver')
        self.line_detector = LineDetector('/usb_cam/image_raw')
        self.obstacle_detector = ObstacleDetector('/ultrasonic')
        self.driver = MotorDriver('/xycar_motor_msg')

    def trace(self):

        obs_m = self.obstacle_detector.get_distance()
        angle = self.line_detector.detect_lines()
        self.line_detector.show_images()
        # if obs_m <= 30:
        #     self.driver.drive(90, 90)
        #     print('STOP!!')
        #     time.sleep(1)
        if (time.time()-start <= 40):
            if -4 <= angle <= 4:
                self.driver.drive(angle + 90, 130)
            elif -7 <= angle <= 7:
                self.driver.drive(angle + 90, 120)
            else:
                self.driver.drive(angle* 1.5 + 90, 119)
        else:
            if obs_m <=30:
                self.driver.drive(90,90)
                time.sleep(0.1)
                self.driver.drive(90, 90)
            else:
                if -4 <= angle <= 4:
                    self.driver.drive(angle + 90, 130)
                elif -7 <= angle <= 7:
                    self.driver.drive(angle + 90, 120)
                else:
                    self.driver.drive(angle* 1.5 + 90, 119)



    def exit(self):
        print('finished')


if __name__ == '__main__':
    car = AutoDrive()
    time.sleep(2)
    rate = rospy.Rate(10)
    start = time.time()
    print('start')
    for i in range(20):
        car.driver.drive(92, 150)
        time.sleep(0.1)
    while not rospy.is_shutdown():
        car.trace()
        rate.sleep()
    rospy.on_shutdown(car.exit)



