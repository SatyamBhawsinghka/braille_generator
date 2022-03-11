#!/usr/bin/python3
# coding=utf8
import logging
logging_format = "%(asctime)s: %(message)s"

from logdecorator import log_on_start, log_on_end, log_on_error

import time

import numpy as np

import sys
sys.path.append('./Lib/ArmPi/')
from ArmIK.Transform import *
from ArmIK.ArmMoveIK import *
import HiwonderSDK.Board as Board

class Motion(object):
    def __init__(self):
        self.X = None
        self.Y = None
        self.AK = ArmIK()
        self.margin = np.array([3, 0, 1])
        self.init_move()

    def set_starts(self, starting_angle, starting_X, starting_Y):
        self.starting_angle = starting_angle
        self.starting_X = starting_X
        self.starting_Y = starting_Y
        #call perception code here, get starting_X, starting_Y, starting_angle
        starting_T = np.array([[np.cos(self.starting_angle), -np.sin(self.starting_angle), self.starting_X],
                               [np.sin(self.starting_angle), np.cos(self.starting_angle), self.starting_Y],
                               [0, 0, 1]])

        mat_mul = starting_T @ self.margin
        self.X = mat_mul[0]
        self.Y = mat_mul[1]

    def init_move(self):
        self.AK.setPitchRangeMoving((0, 5, 10), -30, -30, -90, 1000)
        time.sleep(1)

    def move(self, x, y):
        self.AK.setPitchRangeMoving((x, y, 8), -110, -30, -120, 1000)
        time.sleep(2)
        self.AK.setPitchRangeMoving((x, y, 1), -110, -30, -120, 100)
        time.sleep(0.2)
        self.AK.setPitchRangeMoving((0, 10, 10), -30, -30, -90, 1000)
        time.sleep(2)

    def get_XY(self):
        T = np.array([[np.cos(self.starting_angle), -np.sin(self.starting_angle), self.X],
                      [np.sin(self.starting_angle), np.cos(self.starting_angle), self.Y],
                      [0, 0, 1]])
        mat_mul = T @ self.margin
        self.X = mat_mul[0]
        self.Y = mat_mul[1]

    def get_xy(self):
        points = []
        mx = np.array([1, 0, 1])
        my = np.array([0, -1, 1])

        p1 = np.array([self.X, self.Y, 1])

        for i in range(3):
            points.append([p1[0], p1[1]])
            t = np.array([[np.cos(self.starting_angle), -np.sin(self.starting_angle), p1[0]],
                          [np.sin(self.starting_angle), np.cos(self.starting_angle), p1[1]],
                          [0, 0, 1]])
            p2 = t @ mx
            points.append([p2[0], p2[1]])
            p1 = t @ my

        return points







if __name__ == '__main__':
    motion = Motion()
    motion.set_starts(0, -4, 15)
    points = motion.get_xy()

    for i in points:
        print(i)
        motion.move(i[0], i[1])

