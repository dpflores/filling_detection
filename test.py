import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt

from roi import ROI

# img = cv.imread('images/casino_menta_filled_close.png')
img = cv.imread('images/rellena_not_filled_close.png')
# img = cv.imread('images/rellena_not_filled_close.png')

gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
h = hsv[:,:,0]
s = hsv[:,:,1]
v = hsv[:,:,2]

# ROI
start = [550,200]
roi = ROI(start, 340, 450, img)



# Filtering ROI with gaussian
roi.filter(7)

hist = roi.get_histogram()

roi.thresh(50)

# Opening and closing
roi.dilate(7)
roi.erode(7)

# # Detecting circles
# roi.get_circles()

# roi.draw_circles()

# define background

roi.define_background()


img = cv.imread('images/rellena_partially_filled_close.png')


roi.set_image(img)
# Filtering ROI with gaussian
roi.filter(7)

hist = roi.get_histogram()

roi.thresh(50)

# Opening and closing
roi.dilate(7)
roi.erode(7)

roi.detect_fillig()

roi.show_results()

final_image = roi.draw(0.9)


# print(hist)
# plt.plot(hist)
# plt.show()

# print(hsv)
cv.imshow('ROI image',h)
cv.imshow('Test image',final_image)
cv.waitKey(0)
cv.destroyAllWindows()