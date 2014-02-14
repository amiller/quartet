import glob
import cv2
import numpy as np
import os

def view(filename):
    files = glob.glob('%s/*.pgm' % (filename,)) + glob.glob('%s/*.ppm' % (filename,))
    files = sorted(files, key=lambda f: os.path.basename(f)[2:])
    for f in files:
        if f.endswith('.ppm'):
            cv2.imshow('rgb', cv2.imread(f))
            cv2.waitKey(20)
        if f.endswith('.pgm'):
            depth = np.fromstring(open(f).read()[17:], dtype='uint16').reshape((480,640))
            cv2.imshow('depth', 1024./depth)
            cv2.waitKey(20)
