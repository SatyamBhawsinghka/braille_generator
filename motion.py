#!/usr/bin/python3
# coding=utf8
import logging

logging_format = "%(asctime)s: %(message)s"
from logdecorator import log_on_start, log_on_end, log_on_error

logging.basicConfig(format=logging_format, level=logging.INFO, datefmt="%H:%M:%S")
import time
import numpy as np
import sys

sys.path.append('./Lib/ArmPi/')
from ArmIK.Transform import *
from ArmIK.ArmMoveIK import *
import HiwonderSDK.Board as Board


class Motion(object):
    """Motion class gives the starting position for a new character, positions for each dot of a character in
    workspace and indents on the specified point.

    Initialisation resets the position of the arm.
    Before printing each character call get_XY to reset the starting position of a character.
    Call get_xy to get coordinates of all six dots of a character.
    Call move for indenting any point.

    Attributes:
        margin: Gap between starting position of each character.
        dx: Gap in x direction between individual points of a character.
        dy: Gap in y direction between individual points of a character.
    """
    @log_on_error(logging.DEBUG, "Error in motion class initialisation")
    @log_on_end(logging.DEBUG, "Motion class initialised")
    def __init__(self, margin=1, dx=0.5, dy=0.5):

        # World frame coordinates for start of each character
        self.X = None
        self.Y = None

        self.AK = ArmIK()

        self.initial_margin = np.array([-2, -2, 1])  # Vector to calculate initial start position
        self.margin = np.array([-1 * margin, 0, 1])  # Vector that defines gap between each of the character
        self.dx = np.array([dx, 0, 1])  # Vector that sets resolution between points in x
        self.dy = np.array([0, -1 * dy, 1])  # Vector that sets resolution between points in y

        self.starting_angle = None  # Orientation of paper in workspace
        # Reset the position of arm
        self.init_move()

    @log_on_error(logging.DEBUG, "Error in setting start position and orientation")
    @log_on_end(logging.DEBUG, "Starting position and orientation set")
    def set_starts(self, starting_angle, starting_X, starting_Y):
        """Sets the starting point and orientation"""
        if starting_angle is None or starting_X is None or starting_Y is None:
            raise ValueError("Enter starting_angle, starting_X and starting_Y")
        self.starting_angle = starting_angle
        # Transformation Matrix
        starting_T = np.array([[np.cos(self.starting_angle), -np.sin(self.starting_angle), starting_X],
                               [np.sin(self.starting_angle), np.cos(self.starting_angle), starting_Y],
                               [0, 0, 1]])

        mat_mul = starting_T @ self.initial_margin
        self.X = mat_mul[0]
        self.Y = mat_mul[1]

    @log_on_error(logging.DEBUG, "Error in resetting position of the arm")
    @log_on_end(logging.DEBUG, "Arm position reset")
    def init_move(self):
        """Resets the position of the arm"""
        check = self.AK.setPitchRangeMoving((0, 10, 10), -30, -30, -90, 1000)
        time.sleep(1)
        if check is False:
            raise ValueError("Can't reach initial position")

    @log_on_error(logging.DEBUG, "Error in move")
    def move(self, x, y):
        """Moves the arm to position x, y in workspace"""
        check = True
        c1 = self.AK.setPitchRangeMoving((x, y, 8), -110, -30, -120, 1000)
        time.sleep(2)
        if c1 is False:
            check = False
        c2 = self.AK.setPitchRangeMoving((x, y, 1), -110, -30, -120, 100)
        time.sleep(0.2)
        if c2 is False:
            check = False
        c3 = self.AK.setPitchRangeMoving((0, 10, 10), -30, -30, -90, 1000)
        time.sleep(2)
        if c3 is False:
            check = False
        if check is False:
            raise ValueError(f"Can't reach position {x}, {y}")

    @log_on_error(logging.DEBUG, "Error in get_XY")
    def get_XY(self):
        """Gets world coordinates for starting position of a character"""
        if self.starting_angle is None:
            raise ValueError("Called get_XY without calling set_starts")
        # Transformation Matrix
        T = np.array([[np.cos(self.starting_angle), -1 * np.sin(self.starting_angle), self.X],
                      [np.sin(self.starting_angle), np.cos(self.starting_angle), self.Y],
                      [0, 0, 1]])
        mat_mul = T @ self.margin
        self.X = mat_mul[0]
        self.Y = mat_mul[1]

    @log_on_error(logging.DEBUG, "Error in get_xy")
    def get_xy(self):
        """Gets world coordinates for positions of each of the six dots of a character"""
        if self.starting_angle is None:
            raise ValueError("Called get_xy without calling set_starts")
        points = []
        p1 = np.array([self.X, self.Y, 1])

        for i in range(3):
            points.append([p1[0], p1[1]])
            # Transformation Matrix
            t = np.array([[np.cos(self.starting_angle), -1 * np.sin(self.starting_angle), p1[0]],
                          [np.sin(self.starting_angle), np.cos(self.starting_angle), p1[1]],
                          [0, 0, 1]])
            p2 = t @ self.dx
            points.append([p2[0], p2[1]])
            p1 = t @ self.dy

        return points


if __name__ == '__main__':
    motion = Motion()
    motion.set_starts(0, -3, 13)
    points = motion.get_xy()

    for i in points:
        print(i)
        motion.move(i[0], i[1])
