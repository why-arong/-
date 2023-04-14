import cv2, time
import numpy as np

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
pixel_cnt_threshold = 0.8 * area_width * area_height

while True:
    _, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    dst = cv2.bitwise_not(gray)
    img_result1 = cv2.adaptiveThreshold(dst, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 21, 12)
    final = cv2.bitwise_not(img_result1)

    cv2.circle(frame, (x_1, y_1),5, (0, 0, 255), -1)
    cv2.circle(frame, (x_2, y_2),5, (0, 0, 255), -1)
    cv2.circle(frame, (x_3, y_3),5, (0, 0, 255), -1)
    cv2.circle(frame, (x_4, y_4),5, (0, 0, 255), -1)

    pts1 = np.float32([[x_1, y_1], [x_2, y_2], [x_3, y_3], [x_4, y_4]])
    pts2 = np.float32([[0,0],[640,0],[0,225],[640,225]])
    matrix = cv2.getPerspectiveTransform(pts1, pts2)

    bird = cv2.warpPerspective(final, matrix, (640, 225))
    view = cv2.cvtColor(bird, cv2.COLOR_GRAY2BGR)

    minLineLength = 200
    maxLineGap = 100

    lines = cv2.HoughLinesP(bird, 1, np.pi / 360, 100, minLineLength, maxLineGap)
    for i in range(len(lines)):
        for x1, y1, x2, y2 in lines[i]:
            cv2.line(view, (x1, y1), (x2, y2), (0, 0, 255), 3)

    lower_red = np.array([-10, 100, 100])
    upper_red = np.array([10, 255, 255])
    hsv = cv2.cvtColor(view, cv2.COLOR_BGR2HSV)
    red_range = cv2.inRange(hsv, lower_red, upper_red)
    red_range = cv2.cvtColor(red_range, cv2.COLOR_GRAY2BGR)

    left, right = -1, -1

    for l in range(area_width, lmid):
        area = bird[row_begin:row_end, l - area_width:l]
        if cv2.countNonZero(area) > pixel_cnt_threshold:
            left = l
            break

    for r in range(image_width - area_width, rmid, -1):
        area = bird[row_begin:row_end, r:r + area_width]
        if cv2.countNonZero(area) > pixel_cnt_threshold:
            right = r
            break

    if left != -1:
        lsquare = cv2.rectangle(red_range,
                                (left - area_width, row_begin),
                                (left, row_end),
                                (0, 255, 0), 3)
    else:
        print("Lost left line")

    if right != -1:
        rsquare = cv2.rectangle(red_range,
                                (right, row_begin),
                                (right + area_width, row_end),
                                (0, 255, 0), 3)
    else:
        print("Lost right line")


    cv2.imshow("origin", frame)
    cv2.imshow("re3",final)
    cv2.imshow("real", view)
    cv2.imshow("red range", red_range)

    key = cv2.waitKey(1)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()
