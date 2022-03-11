import cv2
import numpy as np
import atexit
import time
import sys
sys.path.append('./Lib/ArmPi/')
from ArmIK.Transform import convertCoordinate
from ArmIK.ArmMoveIK import ArmIK
import HiwonderSDK.Board as Board

class Perception():
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        time.sleep(1)
        self.img = None
        # Check if the webcam is opened correctly
        if not self.cap.isOpened():
            raise IOError("Cannot open webcam")
        atexit.register(self.__cleanup)

    @staticmethod
    def thresh(img):
        # apply binary thresholding
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        ret, thresh = cv2.threshold(img_gray, 120, 255, cv2.THRESH_BINARY)
        return thresh

    @staticmethod
    def find_contours(img):
        #Grayscale image
        #Do you wann blur and close?
        thresh_img = cam.thresh(img)
        #ls
        #detect the contours on the binary image using cv2.CHAIN_APPROX_NONE
        contours, hierarchy = cv2.findContours(thresh_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[-2:]
        image_copy = img.copy()
        
        if(len(contours) != 0):
            c = max(contours, key = cv2.contourArea)
            rect = cv2.minAreaRect(c)
            angle = rect[2]
            box = cv2.boxPoints(rect)
            box = np.int0(box)
        
            # draw contours on the original image
            cv2.drawContours(image_copy, [box], -1, (0,255,0), 2)
            # cv2.rectangle(image_copy,(int(x),int(y)),(int(x+w),int(y+h)),(0,255,0),2)
            return image_copy, box, angle
        return None,np.array([None], None)
               

    def read(self):
        self.img = self.cap.read()
        return self.img

    def __cleanup(self):
        self.cap.release()


def convert_pixel_to_world(box, idx = 0, offset = 5):
    world_coordinates = convertCoordinate(box[0][0], box[0][1]-offset, frame.shape[:2])
    return world_coordinates

def reset_arm(AK):
    AK.setPitchRangeMoving((0, 10, 10), -30, -30, -90, 1000)

def average_contour_corner(coord_list):
    sum_x = 0
    sum_y = 0
    sum_angle = 0
    for x, y, angle in coord_list:
        sum_x+=x
        sum_y+=y
        sum_angle+=angle
    return (sum_x/len(coord_list), sum_y/len(coord_list), sum_angle/len(coord_list))
            

if __name__ == "__main__":
    cam = Perception()
    flag = True
    w_coord_values = []
    flag_counter = 0
    time.sleep(2)
    while flag:
        ret, frame = cam.read()
        frame, box = cam.find_contours(frame)
        
        if len(box)>1:
            print(convert_pixel_to_world(box))
            w_coord_values.append(convert_pixel_to_world(box))
            flag_counter+=1
            #time.sleep(0.5)
            frame = cv2.resize(frame, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)
            cv2.imshow('Input', frame)
            c = cv2.waitKey(1)
            if c & 0xFF == 27:
                break
            if(flag_counter == 60):
                flag = False
    world_coordinates = average_contour_corner(w_coord_values[10:])
    print(world_coordinates)

    cv2.destroyAllWindows()
