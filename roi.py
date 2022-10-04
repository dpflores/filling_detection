import numpy as np
import cv2 as cv
class ROI():
    def __init__(self,start_point, length, width, img):
        self.start_point = start_point
        self.length = length
        self.width = width
        
        self.vertices = np.array([start_point,[start_point[0]+length,start_point[1]],
                                [start_point[0]+length,start_point[1]+width], [start_point[0],start_point[1]+width]])
        
        self.img = img
        self.roi_img = img[start_point[1]:start_point[1]+width,start_point[0]:start_point[0]+length]
        hsv = cv.cvtColor(self.roi_img, cv.COLOR_BGR2HSV)
        self.roi_h = hsv[:,:,0]
        self.roi_s = hsv[:,:,1]
        self.roi_v = hsv[:,:,2]

    def draw(self, alpha=0.6):
        overlay = self.img.copy()
        # Quadrilateral perimeter
        cv.polylines(overlay, [self.vertices], isClosed=True, color=(0,0,255), thickness=3)
        new_img = cv.addWeighted(overlay, alpha, self.img, 1 - alpha, 0)
        return new_img
    
    def filter(self,window_size):
        self.roi_h = cv.GaussianBlur(self.roi_h, (window_size, window_size), 0)
        return self.roi_h

    def thresh(self, th=125):
        ret, self.roi_h = cv.threshold(self.roi_h, th, 255, cv.THRESH_BINARY)

        return self.roi_h

    def get_histogram(self):
        histogram = cv.calcHist([self.roi_h], [0], None, [256], [0, 256])
        return histogram

    # Morphological Image processing
    def erode(self,window_size):
        self.roi_h = cv.erode(self.roi_h,np.ones((window_size,window_size)))
        return self.roi_h
    
    def dilate(self,window_size):
        self.roi_h = cv.dilate(self.roi_h,np.ones((window_size,window_size)))
        return self.roi_h

    
    # Shape detection
    def get_circles(self):
        self.circles = cv.HoughCircles(self.roi_h,cv.HOUGH_GRADIENT,1.5,500,
                            param1=50,param2=20,minRadius=0,maxRadius=0)
        
        print(self.circles)
    def draw_circles(self):
        self.circles = np.uint16(np.around(self.circles))
        for i in self.circles[0,:]:
            # draw the outer circle
            cv.circle(self.roi_h,(i[0],i[1]),i[2],(0,255,0),2)
            # draw the center of the circle
            cv.circle(self.roi_h,(i[0],i[1]),2,(0,0,255),3)
