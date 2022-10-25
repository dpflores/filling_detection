import cv2 as cv
from rcircle import RCircle

# For timing analysis
import time 



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

    roi.get_circles()
    

    roi.detect_filling()

    roi.draw_circles()

    roi.show_results()

    final_image = roi.draw(0.9)
    analyzed= roi.analyzed_layer

    return analyzed,final_image


if __name__=='__main__':

    # start time
    st = time.time()

    img = cv.imread('images/rellena.png')

    # print(img.shape)
    # Init ROI
    start = [480,200]
    length = 400
    width = 400
    roi = RCircle(start, length, width)

    roi.set_image(img)

    # analyzed, final_image =run_detection_percent(img)
    analyzed, final_image = run_detection_circle(img)


    # FOR TERMINAL 
    print(roi.filling_percentage)

    # end time
    et = time.time()
    # get the execution time
    elapsed_time = et - st
    print('Execution time:', elapsed_time, 'seconds')

