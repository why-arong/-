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
    pts2 = np.float32([[0, 0], [485, 0], [0, 358], [485, 358]])
    matrix = cv2.getPerspectiveTransform(pts1, pts2)

    bird = cv2.warpPerspective(final, matrix, (485, 358))
    view = cv2.cvtColor(bird, cv2.COLOR_GRAY2BGR)

    minLineLength = 100
    maxLineGap = 333
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
                angle_list.append(angle-90)
        # print(angle_list)
        # print(np.bincount(angle_list).argmax())
        if -4 <= np.average(angle_list) <= 4:
            print("fast")
        elif -6 <= np.average(angle_list) <= 6:
            print("slow")
        elif 15 >= np.average(angle_list) > 6:
            print("small right")
        elif np.average(angle_list) > 15:
            print("big right")
        elif -20 <= np.average(angle_list) < -6:
            print("small left")
        elif np.average(angle_list) < -20:
            print("big left")

        print(np.average(angle_list))
    except Exception as e:
        pass
    lower_red = np.array([-10, 100, 100])
    upper_red = np.array([10, 255, 255])
    hsv = cv2.cvtColor(view, cv2.COLOR_BGR2HSV)
    red_range = cv2.inRange(hsv, lower_red, upper_red)
    red_view = cv2.cvtColor(red_range, cv2.COLOR_GRAY2BGR)
    cv2.imshow('origin', frame)
    cv2.imshow("bird", view)

    key = cv2.waitKey(1)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()










