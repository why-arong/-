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
        self.driver = MotorDriver('/xycar_motor_msg')
        self.obstacle_detector = ObstacleDetector('/ultrasonic')
        self.count = 0

    def trace(self):
        angle = self.line_detector.detect_lines()
        obs_m = self.obstacle_detector.get_distance()
        self.line_detector.show_images()

        if 47.5 < time.time()-start < 68:
            if angle >= 110:
                self.driver.drive(angle + (0.2*(angle - 90)), 133)
            elif 70 < angle < 110:
                self.driver.drive(angle, 130)
            else:
                self.driver.drive(angle-(0.2 * (90 -angle)) + 1,134)
                # if abs(angle-90) > 20:
                #     self.driver.drive(angle+(0.2*abs(angle-90)), 125)
                # else:
                #     self.driver.drive(angle, 125)

        elif time.time() - start <= 47.5:
            self.driver.drive(angle + 3, 200)

        else:
            if 0 < obs_m < 113:
                self.count += 1
            else:
                self.count = 0

            if self.count < 3:
                if angle >= 110:
                    self.driver.drive(angle+(0.2*(angle - 90)), 140)
                elif 70 < angle < 110:
                    self.driver.drive(angle, 133)
                else:
                    self.driver.drive(angle-(0.2*(90 -angle)) + 5,140)
            else:
                self.driver.drive(91, 90)
                time.sleep(1)

        # else:
        #     self.driver.drive(angle+3,200)

    def exit(self):
        print('finished')


if __name__ == '__main__':
    car = AutoDrive()
    time.sleep(2)
    rate = rospy.Rate(25)
    start = time.time()
    while not rospy.is_shutdown():
        car.trace()
        rate.sleep()
    rospy.on_shutdown(car.exit)



