from cgi import test
import sys
sys.path.append('./')
from motion import Motion
from perception import Perception, convert_pixel_to_world, average_contour_corner, sort_rect, get_angle_from_coordinates
import numpy as np
import braille_lib.alphaToBraille2 as alphaToBraille
import cv2 
import time

if __name__ == "__main__":
    cam = Perception()
    motion = Motion()
    flag = True
    w_coord_values = []
    flag_counter = 0
    time.sleep(2)
    while flag:
        ret, frame = cam.read()
        frame, box, angle = cam.find_contours(frame)
        
        if len(box)>1:
            #print(convert_pixel_to_world(box, (640, 480)))
            w_coord_values.append(convert_pixel_to_world(box, (640,480)))
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
    #print(world_coordinates)
    world_coordinates = sort_rect(np.array(world_coordinates))
    angle = get_angle_from_coordinates(world_coordinates)
    print(angle)

    motion.set_starts(angle, world_coordinates[3][0], world_coordinates[3][1])
    points = motion.get_xy()

    test_string = "abc123"
    test_string_braille = alphaToBraille.translate(test_string)
    test_string_braille = np.array(test_string_braille[0]).astype('uint8')
    # test_string_braille = test_string_braille.reshape(-1)
    for k in range(test_string_braille.shape[0]):
        # the 6 points for each characters
        points = motion.get_xy()
        for j,i in enumerate(points):
            if(((test_string_braille[k]).reshape[-1])[j]==1):
                motion.move(i[0], i[1])
                print(i[0], i[1])
        # get the new starting location
        motion.getXY()
    # test_string = "s"
    # test_string_braille = alphaToBraille.translate(test_string)
    # test_string_braille = np.array(test_string_braille[0]).astype('uint8')
    # test_string_braille = test_string_braille.reshape(-1)
    # for j,i in enumerate(points):
    #     if(test_string_braille[j]==1):
    #         motion.move(i[0], i[1])
    #         print(i[0], i[1])
    cv2.destroyAllWindows()
