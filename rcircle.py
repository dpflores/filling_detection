from roi import ROI 
import numpy as np

import cv2 as cv

class RCircle (ROI):

    def get_circles(self):
        self.circles = cv.HoughCircles(self.analyzed_layer,cv.HOUGH_GRADIENT,1.5,500,
                            param1=50,param2=20,minRadius=32)
        if self.circles is not None:
            self.circles = np.uint16(np.around(self.circles))
        return self.circles
    
    def draw_circles(self):
        if self.circles is not None:
            for i in self.circles[0,:]:
                # draw the outer circle
                cv.circle(self.roi_img,(i[0],i[1]),i[2],(0,255,0),2)
                # draw the center of the circle
                cv.circle(self.roi_img,(i[0],i[1]),2,(0,0,255),3)
        else:
            print('No cookie')

    def detect_filling(self):

        circle = self.get_circles()
        
        if circle is None:
            self.cookie = False
            self.filling_percentage = 0
            return
        else:
            self.cookie = True
            circle_area = np.pi*circle[0,0,2]**2
            mask = np.zeros_like(self.analyzed_layer)
            mask = cv.circle(mask, (circle[0,0,0], circle[0,0,1]), circle[0,0,2], (255,255,255), -1)

            self.result = cv.bitwise_and(self.analyzed_layer, mask)
            white_count = cv.countNonZero(self.result)

            
            self.filling_percentage = (white_count/circle_area)*100
        

        

