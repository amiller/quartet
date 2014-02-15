import numpy as np
import shutil
import glob
import gzip_patch
import gzip
import os
import cv2
import re
import snappy
from config import KINECT_PATH
import calib
import cPickle as pickle

depths = []
rgbs = []
current_path = None
frame_num = None
calib_mats = None

FN_RE = re.compile('[dr]-(.*)-(.*)\.(.*)')
def iter(rgb=True, depth=True, skip=1):
    # Load the image
    fns = []
    fns_ = glob.glob(current_path+'/host-*/*/*.snappy')+glob.glob(current_path+'/host-*/*/*.jpg')
    print len(fns_)
    for fn in fns_:
        host,_,fnbase = fn.split('/')[-3:]
        fngroups = list(FN_RE.search(fnbase).groups())
        cam = int(host[-1])-1
        fns.append((fn, cam, float(fngroups[0])))
    fns.sort(key=lambda x: x[2])
    fns = fns[::skip]
    for fn, cam, ts in fns:
        if (fn.endswith('.ppm') or fn.endswith('.jpg')) and rgb:
            yield ((cam, ts, cv2.imread(fn)),), ()
        elif fn.endswith('.snappy') and depth:
            d = np.fromstring(snappy.decompress(open(fn).read()), dtype=np.uint16).reshape((480, 640))
            yield (), ((cam, ts, d),)
        #if rgbs or depths:
        #    yield rgbs, depths

def advance():
    global depths, rgbs, frame_iter
    while True:
        r, d = frame_iter.next()
        for (cam,_,rgb) in r:
            rgbs[cam] = rgb
        for (cam,_,depth) in d:
            depths[cam] = depth
        if not (None in depths or None in rgbs): break

def load_dataset(pathname):
    global current_path, frame_num

    # Check for consistency, count the number of images
    current_path = pathname
    frame_num = 0
    global frame_iter
    frame_iter = iter()
    global depths, rgbs
    depths = [np.zeros((480,640),np.uint16) for _ in range(5)]
    rgbs = [np.zeros((480,640,3),np.uint8) for _ in range(5)]

    global image_sets
    image_setses = glob.glob(current_path + '/image_sets-*.npz')
    image_sets = np.load(sorted(image_setses)[-1])

def load_random_dataset(path=KINECT_PATH):
    # Look in the datasets folder, find all the datasets
    # pick one
    sets = glob.glob(path + '/*/')
    load_dataset(sorted(sets)[-1])

def load_calibration(pathname):
    # Load the most recent calibration points in this directory
    current_path = pathname
    calib_files = glob.glob(current_path + '/calib_points-*.pkl')
    fname = sorted(calib_files)[-1]
    with open(fname) as f:
        points_in_sets = pickle.load(f)
    global calib_mats
    calib_mats = calib.compute_all_mappings(points_in_sets)


if __name__ == "__main__":
    pass
