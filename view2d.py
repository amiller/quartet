import opennpy
import numpy as np
import os
import shutil
import cv2
import subprocess
import dataset
import pylab
from config import KINECT_PATH

def show_rgb(name, image):
    cv2.imshow(name, image)

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
    opennpy.align_depth_to_rgb()
    opennpy.sync_update()
    global depth_cache
    for cam in cams:
        (depth,_) = opennpy.sync_get_depth(cam)
        print(depth.shape)
        print "Depth aligned:", is_aligned(depth)
        depth_cache.append(np.array(depth))
        depth_cache = depth_cache[-6:]
        show_depth('depth_%d'%cam, depth)

def go(dset=None, path=KINECT_PATH, threed=False):
    if dset is None:
        dataset.load_random_dataset(path)
    else:
        dataset.load_dataset(dset)
    for rgbs, depths in dataset.iter(skip=1):
        once(rgbs, depths, threed=threed)
