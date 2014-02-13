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

import opennpy
import numpy as np
import os
import time
import shutil
import cv
import subprocess
import dataset
import colormap
import pylab
import cv2
import hashlib
import multiprocessing
import snappy

from config import KINECT_PATH

def show_depth(name, depth):
    #im = cv.CvreateImage((depth.shape[1],depth.shape[0]), 8, 3)
    #cv.SetData(im, colormap.color_map(depth/2))
    #cv.ShowImage(name, im)
    #cv2.imshow(name, colormap.color_map(depth/2))
    cv2.imshow(name, 1024./depth)
    #pylab.imshow(colormap.color_map(depth))
    pylab.waitforbuttonpress(0.005)

depth_cache = []

def worker(q):
    while 1:
        fn_data = q.get()
        st = time.time()
        if fn_data is None:
            break
        orig = comp = 0
        fn, data = fn_data
        if fn.endswith('.jpg') or fn.endswith('.ppm'):
            cv2.imwrite(fn, data)
        elif fn.endswith('.npy'):
            np.save(fn, data)
        elif fn.endswith('.snappy'):
            data_snappy = snappy.compress(data)
            open(fn, 'w').write(data_snappy)
            orig = len(data)
            comp = len(data_snappy)
        print('Size[%d] Fn[%s] Time[%f] Orig[%d] Comp[%d]' % (q.qsize(), os.path.basename(fn), time.time() - st, orig, comp))

def is_aligned(depth): return np.var(depth[:10,:]) == 0

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


def go(cams=(0,)):
    opennpy.align_depth_to_rgb()
    while 1:
        preview(cams)
        pylab.waitforbuttonpress(0.005)


def record(filename=None, cams=(0,), do_rgb=False):
    if len(cams) > 1 and do_rgb:
        print """You're trying to record from 2+ kinects with RGB and depth.
        This probably will not work out for you, but it depends on if you have
        enough USB bandwidth to support all four streams. Call record with 
        do_rgb=False to turn off rgb."""
    q = multiprocessing.Queue(10000)
    p = multiprocessing.Process(target=worker, args=(q,))
    p.start()
        
    opennpy.align_depth_to_rgb()
    if filename is None:
        filename = str(time.time())

    foldername = KINECT_PATH + '%s' % filename
    dataset.folder = foldername
    try:
        os.makedirs(foldername)
    except OSError:
        pass
    #shutil.copytree('data/newest_calibration/config', '%s/config' % foldername)
    print "Created new dataset: %s" % foldername
    min_delay = 1
    frame = 0
    frame_md5s = {}
    frame_last_update = {}
    def check_frame(name, cam, frame_data):
        frame_md5 = hashlib.md5(frame_data).digest()
        key = '%s:%d' % (name, cam)
        if frame_md5s.get(key) == frame_md5:
            #print('Kinect [%s] is repeating data, likely crashed...' % key)
            last_update = frame_last_update.get(key)
            if last_update is None or (time.time() - last_update) > 10.:
                return 'die'
        else:
            frame_last_update[key] = time.time()
            frame_md5s[key] = frame_md5
            return 'new'

    def die():
        q.put(None)

    while 1:
        print('')
        st = time.time()
        opennpy.sync_update()
        for cam in cams:
            (depth,_) = opennpy.sync_get_depth(cam)
            ret = check_frame('depth', cam, depth.tostring())
            if ret == 'die':
                return die()
            elif ret == 'new':
                q.put(('%s/depth_%f_%05d_%d.snappy' % (foldername,st,frame,cam), depth.tostring()))
            if do_rgb:
                (rgb,_) = opennpy.sync_get_video(cam)
                ret = check_frame('rgb', cam, rgb.tostring())
                if ret == 'die':
                    return die()
                elif ret == 'new':
                    rgb = cv2.cvtColor(rgb, cv.CV_RGB2BGR)
                    q.put(('%s/rgb_%f_%05d_%d.ppm' % (foldername,st,frame,cam), rgb))

        if frame % 30 == 0:
            print 'frame: %d' % frame
        cur_time = time.time()
        print({k: cur_time - v for k, v in frame_last_update.items()})
        frame = frame + 1
        sleep_time = max(0, min_delay - (time.time() - st))
        #time.sleep(sleep_time)
        print('Time: %f' % (time.time() - st,))


def compress():
    cmd = "gzip %s/*.npy" % (dataset.folder,)
    print "Running %s" % cmd
    import sys
    sys.stdout.flush()
    subprocess.call(cmd, shell=True)
