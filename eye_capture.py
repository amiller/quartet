import matplotlib
matplotlib.use('WX')
import cv2
import numpy as np
import random
import argparse
import os
import time
import glob
from config import EYE_PATH, NUM_EYE_CAMERAS

def camera_capture(camera_ids, dump, mode):
    cameras = []
    for camera_id in camera_ids:
        camera = cv2.VideoCapture(camera_id)
        camera.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, 640)
        camera.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, 480)
        cameras.append((camera_id, camera))
    frame_num = 0
    while 1:
        st = time.time()
        for camera_id, camera in cameras:
            rval, frame = camera.read()
            assert frame is not None
            if mode == 'save':
                cv2.imwrite(dump + '/rgb_%f_%05d_%d.jpg' % (time.time(), frame_num, camera_id), frame)
            if mode == 'display':
                cv2.imshow(str(camera_id), frame)
                cv2.waitKey(10)
        frame_num += 1
        print(time.time() - st)

def main():
    parser = argparse.ArgumentParser(description='Webcam Data Saver')
    subparsers = parser.add_subparsers()
    subparser = subparsers.add_parser('display')
    subparser.set_defaults(mode='display')
    subparser = subparsers.add_parser('save')
    subparser.set_defaults(mode='save')
    subparser = subparsers.add_parser('playback')
    subparser.set_defaults(mode='playback')
    args = vars(parser.parse_args())
    args['dump'] = EYE_PATH
    dump = os.path.join(os.path.abspath(args['dump']), str(time.time()))
    mode = args['mode']
    if mode == 'playback':
        import viewdataset
        viewdataset.go(path=EYE_PATH)
    else:
        try:
            os.makedirs(dump)
        except OSError:
            pass
        camera_capture(range(NUM_EYE_CAMERAS), dump, mode)

if __name__ == '__main__':
    main()
