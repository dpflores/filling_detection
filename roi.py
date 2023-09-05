import numpy as np
import cv2 as cv
class ROI():
    def __init__(self,start_point, length, width):
        self.start_point = start_point
        self.length = length
        self.width = width

        self.roi_size = length*width
        
        self.vertices = np.array([start_point,[start_point[0]+length,start_point[1]],
                                [start_point[0]+length,start_point[1]+width], [start_point[0],start_point[1]+width]])
        

    def set_image(self, img):
        self.img = img
        self.roi_img = img[self.start_point[1]:self.start_point[1]+self.width,
                        self.start_point[0]:self.start_point[0]+self.length]

        hsv = cv.cvtColor(self.roi_img, cv.COLOR_BGR2HSV)
        roi_h = hsv[:,:,0]
        roi_s = hsv[:,:,1]
        roi_v = hsv[:,:,2]

        self.analyzed_layer = roi_s

    def define_background(self):
        self.background_size = cv.countNonZero(self.analyzed_layer)
        self.background_percentage = (self.background_size/self.roi_size)*100
        self.cookie_size = self.roi_size - self.background_size

    def draw(self, alpha=0.6):
        overlay = self.img.copy()
        # Quadrilateral perimeter
        cv.polylines(overlay, [self.vertices], isClosed=True, color=(0,0,255), thickness=3)
        new_img = cv.addWeighted(overlay, alpha, self.img, 1 - alpha, 0)
        return new_img
    
    def filter(self,window_size):
        self.analyzed_layer = cv.GaussianBlur(self.analyzed_layer, (window_size, window_size), 0)
        return self.analyzed_layer

    def filter_median(self, window_size):
        self.analyzed_layer = cv.medianBlur(self.analyzed_layer, window_size)
        return self.analyzed_layer

    def thresh(self, th=125, invert=0):
        ret, self.analyzed_layer = cv.threshold(self.analyzed_layer, th, 255, cv.THRESH_BINARY)
        if invert:
            self.analyzed_layer = 255-self.analyzed_layer
        return self.analyzed_layer

    def get_histogram(self):
        histogram = cv.calcHist([self.analyzed_layer], [0], None, [256], [0, 256])
        return histogram

    # Morphological Image processing
    def erode(self,window_size):
        self.analyzed_layer = cv.erode(self.analyzed_layer,np.ones((window_size,window_size)))
        return self.analyzed_layer
    
    def dilate(self,window_size):
        self.analyzed_layer = cv.dilate(self.analyzed_layer,np.ones((window_size,window_size)))
        return self.analyzed_layer


    def detect_filling(self):
        
        white_count = cv.countNonZero(self.analyzed_layer)

        white_percentage = (white_count/self.roi_size)*100

        black_percentage = 100 - white_percentage
        # print(white_count, self.roi_size, black_percentage)
        # Here we define a parameter
        #           PARAMETER
        self.cookie = black_percentage > 2.5

        if self.cookie:
            filling_size = white_count - self.background_size
            self.filling_percentage = (filling_size/self.cookie_size)*100
        else:
            self.filling_percentage = 0
        
        


    def draw_text(self, img, text,
            font=cv.FONT_HERSHEY_SIMPLEX,
            pos=(0, 0),
            font_scale=1,
            font_thickness=2,
            text_color=(0, 255, 0),
            text_color_bg=(0, 0, 0)
            ):

        x, y = pos
        text_size, _ = cv.getTextSize(text, font, font_scale, font_thickness)
        text_w, text_h = text_size
        cv.rectangle(img, pos, (x + text_w, y + text_h), text_color_bg, -1)
        cv.putText(img, text, (x, y + text_h + font_scale - 1), font, font_scale, text_color, font_thickness)

        return text_size

    def show_results(self):
        text = f'Cookie: {self.cookie} Percentage: {np.round(self.filling_percentage,2)}%'

        self.draw_text(self.img, text, text_color=(0, 0, 255))    
        



