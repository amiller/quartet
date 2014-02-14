import glob
import cv2
import numpy as np
import os
import snappy

def view(filename):
    cv2.namedWindow('rgb')
    cv2.namedWindow('depth')
    cv2.moveWindow('rgb',640,0)
    cv2.moveWindow('depth',0,0)
    files = glob.glob('%s/*.snappy' % (filename,)) + glob.glob('%s/*.jpg' % (filename,))
    files = sorted(files, key=lambda f: os.path.basename(f)[2:])
    for f in files:
        if f.endswith('.jpg'):
            cv2.imshow('rgb', cv2.imread(f))
            cv2.waitKey(5)
        if f.endswith('.snappy'):
            depth = np.fromstring(snappy.decompress(open(f).read()), dtype='uint16').reshape((480,640))
            cv2.imshow('depth', 1024./depth)
            cv2.waitKey(5)
