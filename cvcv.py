import cv2
import numpy as np

lower = {'red': (-10, 30, 30), 'green': (50, 30, 30)}
upper = {'red': (10, 255, 255), 'green': (70, 255, 255)}

colors = {'red': (0, 140, 255), 'green': (0, 255, 0)}

cap = cv2.VideoCapture(0)

while True :
    ret, img_color = cap.read()
    img_color=cv2.flip(img_color,1)


    height, width = img_color.shape[:2]
    img_color = cv2.resize(img_color, (width, height), interpolation=cv2.INTER_AREA)

    img_blurred = cv2.GaussianBlur(img_color, (7,7), 0)
    img_hsv = cv2.cvtColor(img_blurred, cv2.COLOR_BGR2HSV)

    for key, value in upper.items():
        kernel = np.ones((9, 9), np.uint8)
        mask = cv2.inRange(img_hsv, lower[key], upper[key])
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
                                cv2.CHAIN_APPROX_SIMPLE)[-2]

        center = None

        if len(cnts)>0 :
            c = max(cnts, key=cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            M = cv2.moments(c)
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

            if radius > 0.5:

                cv2.circle(img_color, (int(x), int(y)), int(radius), colors[key], 2)
                cv2.putText(img_color, key + " ball", (int(x - radius), int(y - radius)), cv2.FONT_HERSHEY_SIMPLEX, 0.6,
                            colors[key], 2)
                print(key + " ball")


    cv2.imshow('img_color',img_color)
    cv2.imshow('img_mask',mask)

    if not ret:
        break

    if cv2.waitKey(1) & 0xFF == 27 :
        break

cv2.destroyAllWindows()