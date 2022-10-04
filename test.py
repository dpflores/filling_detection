import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt

from roi import ROI

# img = cv.imread('images/casino_menta_filled_close.png')
img = cv.imread('images/rellena_partially_filled_far.png')
# img = cv.imread('images/rellena_not_filled_close.png')

gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
h = hsv[:,:,0]
s = hsv[:,:,1]
v = hsv[:,:,2]

# ROI
start = [580,200]
roi = ROI(start, 360, 450, img)
print(np.max(roi.roi_img))
img2 = roi.draw(0.9)


# Filtering ROI with gaussian
roi.filter(7)

hist = roi.get_histogram()

roi.thresh(50)

# Opening and closing
roi.dilate(7)
roi.erode(7)

# Detecting circles
roi.get_circles()

roi.draw_circles()

# print(hist)
# plt.plot(hist)
# plt.show()

# print(hsv)
cv.imshow('ROI image',h)
cv.imshow('Test image',roi.roi_h)
cv.waitKey(0)
cv.destroyAllWindows()