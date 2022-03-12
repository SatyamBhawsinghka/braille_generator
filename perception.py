import cv2
import numpy as np
import atexit
import time
import sys
sys.path.append('./Lib/ArmPi/')
from ArmIK.Transform import convertCoordinate
from ArmIK.ArmMoveIK import ArmIK
import HiwonderSDK.Board as Board
from scipy.spatial import distance as dist

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
        ret, thresh = cv2.threshold(img_gray, 150, 255, cv2.THRESH_BINARY)
        return thresh

    def find_contours(self, img):
        #Grayscale image
        #Do you wann blur and close?
        thresh_img = self.thresh(img)
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
        return None, np.array([None]), None
               

    def read(self):
        self.img = self.cap.read()
        return self.img

    def __cleanup(self):
        self.cap.release()


def convert_pixel_to_world(box, shape, idx = 0, offset = 5):
    world_coordinates = []
    for idx in box:
        world_coordinates.append(list(convertCoordinate(idx[0], idx[1], shape)))
    for j,i in enumerate(world_coordinates):
        world_coordinates[j][1] = world_coordinates[j][1] - 5 
    return world_coordinates

def reset_arm(AK):
    AK.setPitchRangeMoving((0, 10, 10), -30, -30, -90, 1000)

def sort_rect(pts):
	# sort the points based on their x-coordinates
	xSorted = pts[np.argsort(pts[:, 0]), :]
	# grab the left-most and right-most points from the sorted
	# x-roodinate points
	leftMost = xSorted[:2, :]
	rightMost = xSorted[2:, :]
	# now, sort the left-most coordinates according to their
	# y-coordinates so we can grab the top-left and bottom-left
	# points, respectively
	leftMost = leftMost[np.argsort(leftMost[:, 1]), :]
	(tl, bl) = leftMost
	# now that we have the top-left coordinate, use it as an
	# anchor to calculate the Euclidean distance between the
	# top-left and right-most points; by the Pythagorean
	# theorem, the point with the largest distance will be
	# our bottom-right point
	D = dist.cdist(tl[np.newaxis], rightMost, "euclidean")[0]
	(br, tr) = rightMost[np.argsort(D)[::-1], :]
	# return the coordinates in top-left, top-right,
	# bottom-right, and bottom-left order
	return np.array([tl, tr, br, bl], dtype="float32")

def average_contour_corner(coord_list):
    pts = []
    for i in range(4):
        sum_x = 0
        sum_y = 0
        sum_angle = 0
        for pt in coord_list:
            x = pt[i][0]
            y = pt[i][1]
            sum_x+=x
            sum_y+=y
        pts.append([sum_x/len(coord_list), sum_y/len(coord_list)])
    return pts
            

if __name__ == "__main__":
    cam = Perception()
    flag = True
    w_coord_values = []
    flag_counter = 0
    time.sleep(2)
    while flag:
        ret, frame = cam.read()
        frame, box, angle = cam.find_contours(frame)
        
        if len(box)>1:
            print(convert_pixel_to_world(box,(640, 480)))
            w_coord_values.append([*convert_pixel_to_world(box, (640, 480)), angle])
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
    world_coordinates = sort_rect(world_coordinates)
    print(world_coordinates)

    cv2.destroyAllWindows()
