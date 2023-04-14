#!/usr/bin/env python

import rospy, time

from linedetector import LineDetector
from obstacledetector import ObstacleDetector
from motordriver import MotorDriver

class AutoDrive:

    def __init__(self):
        rospy.init_node('xycar_driver')
        self.line_detector = LineDetector('/usb_cam/image_raw')
        self.obstacle_detector = ObstacleDetector('/ultrasonic')
        self.driver = MotorDriver('/xycar_motor_msg')

    def trace(self):
        line_l, line_r = self.line_detector.detect_lines()
        self.line_detector.show_images(line_l, line_r)
        while line_l !=-1 and line_r !=-1:
            mid = (line_l + line_r) // 2
            if mid < 300:
                angle = (mid -320)//3
                speed = 25
                print("left")


            elif mid > 340:
                angle = (mid-320)//3
                speed = 25
                print("right")
            else:
                angle = 0
                speed = 30
            for i in range(10):
                self.driver.drive(angle + 90, speed + 90)
                time.sleep(0.1)


        while (line_l ==-1 and line_r !=-1) :
            diff = line_r -320
            angle = 90 - (100//diff)
            speed = 112
            for i in range(10):
                self.driver.drive(angle + 90, speed + 90)
                time.sleep(0.1)
        while (line_l!=-1 and line_r==-1):
            diff = line_l - 320
            angle = 90 + (100 // diff)
            speed = 112
            for i in range(10):
                self.driver.drive(angle + 90, speed + 90)
                time.sleep(0.1)



    def exit(self):
        print('finished')

if __name__ == '__main__':
    car = AutoDrive()
    time.sleep(3)
    rate = rospy.Rate(30)
    while not rospy.is_shutdown():
        car.trace()
        rate.sleep()
    rospy.on_shutdown(car.exit)