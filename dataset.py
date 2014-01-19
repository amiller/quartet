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

depths = []
rgbs = []
current_path = None
frame_num = None


def advance(skip=1):
    # Load the image
    global frame_num, depths, rgbs
    frame_num += skip
    depths = []
    rgbs = []
    for cam in [0]:#range(len(config.cameras)):
        try:
            # Try the old style with no frame field (backward compatible)
            with gzip.open('%s/depth_%05d.npy.gz' % (current_path, frame_num),
                           'rb') as f:
                depths.append(np.load(f))
        except IOError:
            try:
                with gzip.open('%s/depth_%05d_%d.npy.gz' % (current_path, frame_num, cam),
                               'rb') as f:
                    depths.append(np.load(f))
            except IOError:
                if not depths: raise
        try:
            rgb = cv2.imread('%s/rgb_%05d_%d.png' % (current_path, frame_num,cam))
            if rgb is None: continue
            rgb = cv2.cvtColor(rgb, cv2.cv.CV_RGB2BGR)
            rgbs.append(np.fromstring(rgb.tostring(),'u1').reshape(480,640,3))
        except IOError:
            continue


def load_dataset(pathname):
    global current_path, frame_num

    # Check for consistency, count the number of images
    current_path = pathname
    frame_num = 0


def load_random_dataset():
    # Look in the datasets folder, find all the datasets
    # pick one
    sets = glob.glob('data/sets/*/')
    import random
    choice = random.choice(sets)
    load_dataset(choice)


if __name__ == "__main__":
    pass
