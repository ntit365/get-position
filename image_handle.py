import cv2
import numpy as np


def find_out_point(image, template):
    img = cv2.imread(image)
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    template = cv2.imread(template, cv2.IMREAD_GRAYSCALE)
    w, h = template.shape[::-1]

    result = cv2.matchTemplate(gray_img, template, cv2.TM_CCOEFF_NORMED)
    loc = np.where(result >= 0.8)

    position = {"x": None, "y": None}
    for pt in zip(*loc[::-1]):
        position = {"x": pt[0] + w//2, "y": pt[1] + h//2}

    return position
