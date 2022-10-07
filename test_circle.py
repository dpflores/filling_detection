from unicodedata import name
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt

from rcircle import RCircle


def run_detection_circle(img):
    roi.set_image(img)
    # # Filtering ROI with gaussian
    # roi.filter(5)
    roi.filter_median(7)

    # hist = roi.get_histogram()

    roi.thresh(80,invert=1)
    
    # # Opening and closing
    # op_close_window = 3
    # roi.dilate(op_close_window)
    # roi.erode(op_close_window)

    roi.detect_fillig()
    roi.get_circles()

    roi.detect_fillig()

    roi.show_results()

    final_image = roi.draw(0.9)
    analyzed= roi.analyzed_layer

    return analyzed,final_image



if __name__=='__main__':


    img = cv.imread('images/rellena_partially_filled_close.png')

    # ROI
    start = [550,200]
    roi = RCircle(start, 340, 450, img)

    # analyzed, final_image =run_detection_percent(img)
    analyzed, final_image = run_detection_circle(img)

    # print(hist)
    # plt.plot(hist)
    # plt.show()

    # print(hsv)
    cv.imshow('ROI image',analyzed)
    cv.imshow('Test image',final_image)
    cv.waitKey(0)
    cv.destroyAllWindows()