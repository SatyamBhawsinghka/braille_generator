Run command:
`python main2.py <filename> <-t>`
## Usage
```

Usage:
    Usage:
        main.py <parameter>
        main.py <file name> <parameter>
    Parameters:
        -braille | --b      translate braille to text
        -text    | --t      translate text to braille
        -help    | --h      display this screen
        -map     | --m      print translation map

```
    # world_coordinates = average_contour_corner(w_coord_values[10:])
    # world_coordinates = sort_rect(world_coordinates)
    # print(world_coordinates)
    # motion.set_starts(0, world_coordinates[0], world_coordinates[1])
    # points = motion.get_xy()


    # test_string = "s"
    # test_string_braille = alphaToBraille.translate(test_string)
    # test_string_braille = np.array(test_string_braille[0]).astype('uint8')
    # test_string_braille = test_string_braille.reshape(-1)
    # for j,i in enumerate(points):
    #     if(test_string_braille[j]==1):
    #         motion.move(i[0], i[1])
    #         print(i[0], i[1])
    # cv2.destroyAllWindows()

    world_coordinates = average_contour_corner(w_coord_values[10:])
    world_coordinates = sort_rect(world_coordinates)
    print(world_coordinates)
    motion.set_starts(0, world_coordinates[0], world_coordinates[1])


    test_string = "abc123"
    test_string_braille = alphaToBraille.translate(test_string)
    test_string_braille = np.array(test_string_braille[0]).astype('uint8')
    test_string_braille = test_string_braille.reshape(-1)
    for k in range(test_string_braille.shape[0]):
        # the 6 points for each characters
        points = motion.get_xy()
        for j,i in enumerate(points):
            if(test_string_braille[j]==1):
                motion.move(i[0], i[1])
                print(i[0], i[1])
        # get the new starting location
        motion.getXY()
