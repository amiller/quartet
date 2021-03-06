#import opennpy
import freenect
import numpy as np
import os
import shutil
import cv2
import subprocess
import dataset
from config import KINECT_PATH

def show_rgb(name, image):
    cv2.imshow(name, image[:,:,::-1])

def show_depth(name, depth):
    cv2.imshow(name, 1024./depth)

def once(rgbs, depths):
    # 2D colormap preview
    global depth, rgb
    for i,depth in depths:
        show_depth("depth_%d" % (i,), depth)
    for i,rgb in rgbs:
        show_rgb("image_%d" % (i,), rgb)
    cv2.waitKey(50)

def preview(cams):
    #opennpy.align_depth_to_rgb()
    #opennpy.sync_update()
    cv2.namedWindow('depth_0')
    cv2.moveWindow('depth_0', 0, 0)
    cv2.namedWindow('rgb_0')
    cv2.moveWindow('rgb_0', 640, 0)
    for cam in cams:
        #(depth,_) = opennpy.sync_get_depth(cam)
        (depth,_) = freenect.sync_get_depth(cam, freenect.DEPTH_REGISTERED)
        show_depth('depth_%d'%cam, depth)
        #(rgb,_) = opennpy.sync_get_video(cam)
        (rgb,_) = freenect.sync_get_video(cam)
        show_rgb('rgb_%d'%cam, rgb)
        cv2.waitKey(20)

def go(dset=None, path=KINECT_PATH, threed=False):
    if dset is None:
        dataset.load_random_dataset(path)
    else:
        dataset.load_dataset(dset)
    for rgbs, depths in dataset.iter(skip=1):
        once(rgbs, depths, threed=threed)
