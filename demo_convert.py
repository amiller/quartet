import numpy as np
import os
import shutil
import cv2
import datasetfull as dataset
import pylab
from rtmodel import pointmodel
from rtmodel.rangeimage import RangeImage
from rtmodel.rangeimage_speed import RangeImage # Monkey patch
from rtmodel.camera import kinect_camera
cam = kinect_camera()
import time
import pointcloudmaya

def once():
    r, d = dataset.advance()
    global pm
    if d:
        (cam,ts,_), = d
        depth = dataset.depths[cam]
        rgb = dataset.rgbs[cam]
        rimg = RangeImage(depth, kinect_camera())
        rimg.compute_points()
        pm = rimg.point_model()
        pm.rgba = np.empty((rgb.shape[0]*rgb.shape[1],4),dtype='f')
        pm.rgba[:,:3] = rgb.reshape((-1,3)).astype('f')/256.0
        M = dataset.calib_mats[1][cam]
        pm.xyz = np.dot(M[:3,:3], pm.xyz.T).T + M[:3,3]
        pointcloudmaya.pointcloud_to_partio(pm, folder + ('/pm-%f-%d.prt' % (ts,cam)))
        print cam, ts
    else:
        print 'rgb'
    

def start(dset, skip=1):
    global folder
    folder = dset + ('/partio-%f' % time.time())
    os.makedirs(folder)
    dataset.load_calibration('data/quartetdata/quartet/calib2')
    dataset.load_dataset(dset, skip)
