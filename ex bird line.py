import cv2
import numpy as np
import math
cap = cv2.VideoCapture("2.avi")
x_1, y_1 = 105, 275
x_2, y_2 = 530, 275
x_3, y_3 = 0, 320
x_4, y_4 = 640, 320
image_width = 640
scan_width, scan_height = 230, 350
lmid, rmid = scan_width, image_width - scan_width
area_width, area_height = 15, 15
roi_vertical_pos = 250
row_begin = (scan_height - area_height) // 2
row_end = row_begin + area_height
pixel_cnt_threshold = 0.6 * 3 * 3
init_left, init_right = 40, 570
left, right = init_left, init_right
ex_left, ex_right = init_left, init_right

while True:
    _, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    dst = cv2.bitwise_not(gray)
    img_result1 = cv2.adaptiveThreshold(dst, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 21, 12)
    final = cv2.bitwise_not(img_result1)

    cv2.circle(frame, (x_1, y_1), 5, (0, 0, 255), -1)
    cv2.circle(frame, (x_2, y_2), 5, (0, 0, 255), -1)
    cv2.circle(frame, (x_3, y_3), 5, (0, 0, 255), -1)
    cv2.circle(frame, (x_4, y_4), 5, (0, 0, 255), -1)

    pts1 = np.float32([[x_1, y_1], [x_2, y_2], [x_3, y_3], [x_4, y_4]])
    pts2 = np.float32([[0, 0], [640, 0], [0, 225], [640, 225]])
    matrix = cv2.getPerspectiveTransform(pts1, pts2)

    bird = cv2.warpPerspective(final, matrix, (640, 225))
    view = cv2.cvtColor(bird, cv2.COLOR_GRAY2BGR)

    minLineLength = 100
    maxLineGap = 223
    cv2.imshow('bird', bird)
    angle = 0
    angle_list = []
    try:
        lines = cv2.HoughLinesP(bird, 1, np.pi / 360, 120, minLineLength, maxLineGap)
        for i in range(len(lines)):
            for x1, y1, x2, y2 in lines[i]:
                cv2.line(view, (x1, y1), (x2, y2), (0, 0, 255), 3)
                diff_y = y2 - y1
                diff_x = x2 - x1
                angle = math.atan2(diff_y, diff_x) * 180 /math.pi
                if angle >= 0:
                    angle = int(angle)
                else:
                    angle = int(angle) + 180
                angle_list.append(angle)
        # print(angle_list)
        # print(np.bincount(angle_list).argmax())
        # print(np.average(angle_list))
        if 80 <= angle <= 100:
            # self.driver.drive(90, 130)
            print('straight')
        elif 60 <= angle < 80:
            # self.driver.drive(50, 125)
            print('left little')
        elif 50 <= angle < 60:
            print('left quite')
            # self.driver.drive(30, 120)
        elif angle < 50:
            # self.driver.drive(20, 120)
            print('turrrrrrrn left')
        elif 100 < angle <= 120:
            # self.driver.drive(130, 125)
            print('right little')
        elif 120 < angle <= 130:
            # self.driver.drive(150, 120)
            print('right quite')
        elif 130 < angle:
            # self.driver.drive(170, 20)
            print('tturrrrrrn right')
    except Exception as e:
        pass
    lower_red = np.array([-10, 100, 100])
    upper_red = np.array([10, 255, 255])
    hsv = cv2.cvtColor(view, cv2.COLOR_BGR2HSV)
    red_range = cv2.inRange(hsv, lower_red, upper_red)
    red_view = cv2.cvtColor(red_range, cv2.COLOR_GRAY2BGR)
    cv2.imshow('bird', bird)
    cv2.imshow("re3", final)
    cv2.imshow("real", view)
    cv2.imshow("red range", red_view)

    key = cv2.waitKey(1)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()










