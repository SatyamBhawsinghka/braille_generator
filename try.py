#!/usr/bin/python3
# coding=utf8
import logging
logging_format = "%(asctime)s: %(message)s"
import atexit
from logdecorator import log_on_start, log_on_end, log_on_error
import cv2
import time
import math
import numpy as np
import threading
import sys
sys.path.append('./Lib/ArmPi/')
from Camera import Camera
from LABConfig import *
from ArmIK.Transform import *
from ArmIK.ArmMoveIK import *
import HiwonderSDK.Board as Board
from CameraCalibration.CalibrationConfig import *

AK = ArmIK()
AK.setPitchRangeMoving((0, 10, 10), -30, -30, -90, 1000)
time.sleep(1.5)

AK.setPitchRangeMoving((0, 20, 0), -110, -30, -120, 1000)
time.sleep(1)


AK.setPitchRangeMoving((0, 20, -1), -110, -30, -120, 100)
time.sleep(0.1)


AK.setPitchRangeMoving((0, 20, 10), -110, -30, -120, 100)
time.sleep(0.1)
