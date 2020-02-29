import cv2
import csv
import glob
import tensorflow as tf
import numpy as np
import tensorflow.compat.v1 as tf
def Imagecapture(classcount):
    cap = cv2.VideoCapture(0)
    count=0
    while(count<10):
        ret, frame = cap.read() 
        dst = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        dst = cv2.resize(dst, (50,50), interpolation=cv2.INTER_CUBIC)
    cap.release()
    cv2.destroyAllWindows()
Imagecapture(1)
