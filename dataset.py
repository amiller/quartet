# Andrew Miller <amiller@cs.ucf.edu> 2011
#
# BlockPlayer - 3D model reconstruction using the Lattice-First algorithm
# See: 
#    "Interactive 3D Model Acquisition and Tracking of Building Block Structures"
#    Andrew Miller, Brandyn White, Emiko Charbonneau, Zach Kanzler, and Joseph J. LaViola Jr.
#    IEEE VR 2012, IEEE TVGC 2012
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

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

depths = []
rgbs = []
current_path = None
frame_num = None

FN_RE = re.compile('(.+)_(.+)_(.+)_(.+)\.(.+)')
def iter(rgb=True, depth=True, skip=1):
    # Load the image
    depths = []
    rgbs = []
    fns = []
    for fn in glob.glob(current_path + '/*'):
        fnbase = os.path.basename(fn)
        fngroups = list(FN_RE.search(fnbase).groups())
        fngroups[1] = float(fngroups[1])
        fngroups[3] = int(fngroups[3])
        fns.append((fn, fngroups))
    fns.sort(key=lambda x: x[1][1])
    fns = fns[::skip]
    for fn, fngroups in fns:
        if (fn.endswith('.ppm') or fn.endswith('.jpg')) and rgb:
            yield ((fngroups[3], cv2.imread(fn)),), ()
        elif fn.endswith('.snappy') and depth:
            d = np.fromstring(snappy.decompress(open(fn).read()), dtype=np.uint16).reshape((480, 640))
            yield (), ((fngroups[3], d),)
        #if rgbs or depths:
        #    yield rgbs, depths

def advance():
    global depths, rgbs, frame_iter
    while True:
        r, d = frame_iter.next()
        print len(r),len(d)
        for (cam,rgb) in r:
            rgbs[cam] = rgb
        for (cam,depth) in d:
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
    depths = [None, None]
    rgbs = [None, None]

def load_random_dataset(path=KINECT_PATH):
    # Look in the datasets folder, find all the datasets
    # pick one
    sets = glob.glob(path + '/*/')
    load_dataset(sorted(sets)[-1])


if __name__ == "__main__":
    pass
