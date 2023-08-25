import cv2 as cv
from rcircle import RCircle

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
roi = RCircle(start, 340, 450)

roi.set_image(img)

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



# # print(hist)
# # plt.plot(hist)
# # plt.show()

# # print(hsv)
# cv.imshow('ROI image',h)
# cv.imshow('Test image',final_image)
# cv.waitKey(0)
# cv.destroyAllWindows()



#!/usr/bin/env python3

# # SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2020 ifm electronic gmbh
#
# THE PROGRAM IS PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND.
#

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


from ifm3dpy import O3R, FrameGrabber, buffer_id
import cv2
import argparse
import asyncio


def get_jpeg(frame):
    return cv2.imdecode(frame.get_buffer(buffer_id.JPEG_IMAGE), cv2.IMREAD_UNCHANGED)


async def display_2d(fg, getter, title):
    fg.start([buffer_id.NORM_AMPLITUDE_IMAGE,buffer_id.RADIAL_DISTANCE_IMAGE,buffer_id.XYZ,buffer_id.REFLECTIVITY,buffer_id.MONOCHROM_2D])
    cv2.startWindowThread()
    # cv2.namedWindow(title, cv2.WINDOW_NORMAL)
    while True:
        frame = await fg.wait_for_frame()

        img = getter(frame)
        # img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        hue, img = run_detection_circle(img)

        # FOR COMPUTER
        # cv2.imshow(title, img)
        # cv2.imshow('hue', hue)
        # cv2.waitKey(15)

        # FOR TERMINAL
        print(roi.filling_percentage)


        # if cv2.getWindowProperty(title, cv2.WND_PROP_VISIBLE) < 1:
        #     break


    cv2.destroyAllWindows()





async def main():
    image_choices = ["jpeg", "distance", "amplitude", "reflectivity", "mono"]

    parser = argparse.ArgumentParser()
    parser.add_argument("--pcic-port", help="The pcic port from which images should be received", type=int,
                        required=True)
    parser.add_argument("--image", help="The image to received (default: distance)", type=str,
                        choices=image_choices, required=True)
    parser.add_argument("--ip", help="IP address of the sensor (default: 192.168.0.69)",
                        type=str, required=False, default="192.168.0.69")
    parser.add_argument("--xmlrpc-port", help="XMLRPC port of the sensor (default: 80)",
                        type=int, required=False, default=80)
    args = parser.parse_args()

    getter = globals()["get_" + args.image]

    cam = O3R(args.ip, args.xmlrpc_port)
    fg = FrameGrabber(cam, pcic_port=args.pcic_port)
    fg.start()
    title = "O3R Port {}".format(str(args.pcic_port))

    if args.image == "xyz":
        # await display_3d(fg, getter, title)
        pass
    else:
        await display_2d(fg, getter, title)


if __name__ == "__main__":
    
    asyncio.run(main())