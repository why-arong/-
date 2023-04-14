import rospy
import cv2
import numpy as np
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import math


class LineDetector:

    def __init__(self, topic):
        self.maxLineGap = 210
        self.minLineLength = 100
        self.x_1, self.y_1 = 105, 275
        self.x_2, self.y_2 = 530, 275
        self.x_3, self.y_3 = 0, 320
        self.x_4, self.y_4 = 640, 320
        self.angle = 0
        self.angle_list = [90]
        self.cam_img = np.zeros(shape=(480, 640, 3), dtype=np.uint8)
        self.bird = np.zeros(shape=(225, 640, 3), dtype=np.uint8)
        self.view = np.zeros(shape=(225, 640, 3), dtype=np.uint8)
        self.bridge = CvBridge()
        rospy.Subscriber(topic, Image, self.conv_image)

    def conv_image(self, data):
        self.cam_img = self.bridge.imgmsg_to_cv2(data, 'bgr8')
        gray = cv2.cvtColor(self.cam_img, cv2.COLOR_BGR2GRAY)
        dst = cv2.bitwise_not(gray)
        img_result1 = cv2.adaptiveThreshold(dst, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 21, 12)
        final = cv2.bitwise_not(img_result1)
        pts1 = np.float32([[self.x_1, self.y_1], [self.x_2, self.y_2], [self.x_3, self.y_3], [self.x_4, self.y_4]])
        pts2 = np.float32([[0, 0], [640, 0], [0, 225], [640, 225]])
        matrix = cv2.getPerspectiveTransform(pts1, pts2)

        self.bird = cv2.warpPerspective(final, matrix, (640, 225))
        self.view = cv2.cvtColor(self.bird, cv2.COLOR_GRAY2BGR)

    def detect_lines(self):
        try:
            lines = cv2.HoughLinesP(self.bird, 1, np.pi / 360, 120, self.minLineLength, self.maxLineGap)
            for i in range(len(lines)):
                for x1, y1, x2, y2 in lines[i]:
                    cv2.line(self.view, (x1, y1), (x2, y2), (0, 0, 255), 3)
                    diff_y = y2 - y1
                    diff_x = x2 - x1
                    self.angle = math.atan2(diff_y, diff_x) * 180 / math.pi
                    # initialization
                    self.angle_list = []
                    if self.angle >= 0:
                        self.angle = int(self.angle)
                    else:
                        self.angle = int(self.angle) + 180
                    self.angle_list.append(self.angle)
        # print(self.angle_list)
        # np.bincount(self.angle_list).argmax())
        #print(np.average(self.angle_list))
            return np.average(self.angle_list)

        except Exception as e:
            return np.average(self.angle_list)

    def show_images(self):
        # cv2.circle(self.cam_img, (self.x_1, self.y_1), 5, (0, 0, 255), -1)
        # cv2.circle(self.cam_img, (self.x_2, self.y_2), 5, (0, 0, 255), -1)
        # cv2.circle(self.cam_img, (self.x_3, self.y_3), 5, (0, 0, 255), -1)
        # cv2.circle(self.cam_img, (self.x_4, self.y_4), 5, (0, 0, 255), -1)
        lower_red = np.array([-10, 100, 100])
        upper_red = np.array([10, 255, 255])
        hsv = cv2.cvtColor(self.view, cv2.COLOR_BGR2HSV)
        red_range = cv2.inRange(hsv, lower_red, upper_red)
        red_view = cv2.cvtColor(red_range, cv2.COLOR_GRAY2BGR)
	#print(np.average(self.angle_list))
        # cv2.imshow("real", self.view)
        #cv2.imshow("red range", red_view)
        # cv2.imshow('bird', self.bird)
        cv2.waitKey(1)
