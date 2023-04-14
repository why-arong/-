import rospy
import cv2, time
import numpy as np
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import math


class LineDetector:

    def __init__(self, topic):
        self.image_width = 640
        self.scan_width, self.scan_height = 200, 35
        self.lmid, self.rmid = self.scan_width, self.image_width - self.scan_width
        self.left_d_x, self.left_d_y, self.left_u_x, self.left_u_y = 0, 0, 0, 0
        self.right_d_x, self.right_d_y, self.right_u_x, self.right_u_y = 0, 0, 0, 0
        self.roi_vertical_pos = 340
        self.row_begin = self.roi_vertical_pos
        self.row_end = self.row_begin + 5
        self.left_angle = 0
        self.right_angle = 0
        self.cam_img = np.zeros(shape=(480, 640, 3), dtype=np.uint8)
        self.mask = np.zeros(shape=(self.scan_height, self.image_width, 3),
                             dtype=np.uint8)
        self.edge = np.zeros(shape=(self.scan_height, self.image_width, 3),
                             dtype=np.uint8)
        self.bridge = CvBridge()
        rospy.Subscriber(topic, Image, self.conv_image)

    def conv_image(self, data):
        # convert ros img to opencv img
        self.cam_img = self.bridge.imgmsg_to_cv2(data, 'bgr8')

        v = self.roi_vertical_pos
        roi = self.cam_img[v:v + self.scan_height, :]

        hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
        # avg_value = np.average(hsv[:, :, 2])
        value_threshold = 450  # avg_value * 3
        lbound = np.array([0, 0, value_threshold], dtype=np.uint8)
        ubound = np.array([180, 255, 255], dtype=np.uint8)

        self.mask = cv2.inRange(hsv, lbound, ubound)

        self.gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        self.blur = cv2.GaussianBlur(self.gray, (5, 5), 0)

        self.edge = cv2.Canny(self.blur, 60, 70)
        self.view = cv2.cvtColor(self.edge, cv2.COLOR_GRAY2BGR)

    def detect_lines(self):
        # Return positions of left and right lines detected
        for i in range(300):

            if self.edge[15, i] == 255:
                self.left_d_x = i
                self.left_d_y = 0
                break

        for i in range(300):
            if self.edge[self.scan_height - 15, i] == 255:
                self.left_u_x = i
                self.left_u_y = self.scan_height-1
                break

        # if self.left_u_x == 0:
        #     for i in range(self.row_begin, self.row_end):
        #         if self.edge[i, 0] == 255:
        #             self.left_u_y = i
        #             break

        for i in range(390, 640):
            if self.edge[15, i] == 255:
                self.right_d_x = i
                self.right_d_y = 0
                break

        for i in range(390,640):
            if self.edge[self.scan_height - 15, i] == 255:
                self.right_u_x = i
                self.right_u_y = self.scan_height-1
                break

        # if self.right_u_x == 0:
        #     for i in range(self.row_begin, self.row_end):
        #         if self.edge[i, 640] == 255:
        #             self.right_u_y = i
        #             break

        self.left_angle = math.atan2(abs(self.left_u_y - self.left_d_y), abs(self.left_d_x - self.left_u_x)) * (
                    180 / math.pi)
        self.right_angle = math.atan2(abs(self.right_u_y - self.right_d_y), abs(self.right_d_x - self.right_u_x)) * (
                    180 / math.pi)

        return self.left_angle, self.right_angle

    def show_images(self):
        # Display images for debugging purposes;
        # do not forget to call cv2.waitKey().
        cv2.line(self.cam_img,
                 (self.left_d_x, self.left_d_y + self.roi_vertical_pos),
                 (self.left_u_x, self.left_u_y + self.roi_vertical_pos),
                 (255, 0, 0), 3)
        cv2.line(self.cam_img,
                 (self.right_d_x, self.right_d_y + self.roi_vertical_pos),
                 (self.right_u_x, self.right_u_y + self.roi_vertical_pos),
                 (0, 255, 0), 3)
        print('{}, {}, {}, {}'.format((self.left_u_x,self.left_u_y),(self.left_d_x, self.left_d_y), (self.right_u_x, self.right_u_y), (self.right_d_x, self.left_d_y)))
        print('left angle' + str(self.left_angle))
        print('right angle' + str(180 - self.right_angle))
        print('average angle' + str((self.left_angle + self.right_angle) / 2))
        cv2.imshow('cam', self.cam_img)
        # cv2.imshow("edge", self.edge)
        cv2.imshow("origin", self.view)
        # cv2.imshow("mask", self.mask)

        cv2.waitKey(1)

