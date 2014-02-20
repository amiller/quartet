import opennpy
import numpy as np
import os
import shutil
import cv2
import subprocess
import dataset
import colormap
import pylab
from wxpy3d import PointWindow
from OpenGL.GL import *
from rtmodel import pointmodel
from rtmodel.rangeimage import RangeImage
from rtmodel.camera import kinect_camera
from config import KINECT_PATH
cam = kinect_camera()

if not 'window' in globals():
    window = PointWindow(size=(640,480))
    #window.Move((632,100))
    print """
    Demo Objrender:
        search for "Points to draw" and uncomment different points
        refresh()
        perturb(): apply a random matrix to the point model
        load_obj(): select a random object and load it
    """

@window.event
def pre_draw():
    glLightfv(GL_LIGHT0, GL_POSITION, (-40, 200, 100, 0.0))
    glLightfv(GL_LIGHT0, GL_AMBIENT, (0.3, 0.3, 0.3, 0.0))
    glLightfv(GL_LIGHT0, GL_DIFFUSE, (0.3, 0.3, 0.3, 0.0))
    glEnable(GL_LIGHT0)
    glEnable(GL_LIGHTING)
    #glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)
    glEnable(GL_COLOR_MATERIAL)
    glEnable(GL_DEPTH_TEST)
    glShadeModel(GL_SMOOTH)
    glMatrixMode(GL_MODELVIEW)


@window.event
def post_draw():
    global points
    if not 'points' in globals(): return

    # Perturbed points (previous estimate)
    glColor(1,1,1)
    glPointSize(1)
    points.draw()

window.Refresh()

def show_rgb(name, image):
    cv2.imshow(name, image)

def show_depth(name, depth):
    cv2.imshow(name, 1024./depth)

def once(rgbs, depths, threed=False):
    # 2D colormap preview
    global depth, rgb
    if not threed:
        for i,depth in depths:
            show_depth("depth_%d" % (i,), depth)
        for i,rgb in rgbs:
            show_rgb("image_%d" % (i,), rgb)
    if threed and depths:
        # 3D point cloud view
        for i,_depth in depths:
            print 'depth', i
            if i == 2: depth = _depth
        for i,_rgb in rgbs:
            print 'rgb', i
            if i == 1: rgb = _rgb
        if not ('depth' in globals() and 'rgb' in globals()): return
        rimg = RangeImage(depth, cam)
        rimg.compute_points()
        global points
        show_rgb("image_%d" % (2,), rgb)
        points = rimg.point_model()
        pts = (points.RT[:3,3] + points.xyz[:,:3])
        #points.rgba = np.empty((rgb.shape[0]*rgb.shape[1],4),dtype='f')
        #points.rgba[:,:3] = rgb.reshape((-1,3)).astype('f')[:,::-1]/256.0
        window.lookat = pts[~np.isnan(pts.sum(0))].mean(1)
        window.Refresh()
    cv2.waitKey(50)
    

def go(dset=None, path=KINECT_PATH, threed=False, skip=1):
    if dset is None:
        dataset.load_random_dataset(path)
    else:
        dataset.load_dataset(dset)
    for rgbs, depths in dataset.iter(skip=skip):
        once(rgbs, depths, threed=threed)
