import numpy as np
import os
import shutil
import cv2
import datasetfull as dataset
import pylab
from wxpy3d import PointWindow
from OpenGL.GL import *
from rtmodel import pointmodel
from rtmodel.rangeimage import RangeImage
from rtmodel.camera import kinect_camera
cam = kinect_camera()

if not 'window' in globals():
    window = PointWindow(size=(640,480))

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
    colors = [[1,0,0],[0,1,0],[0,0,1],[1,1,0],[0,1,1]]
    for i,pm in enumerate(points):
        glColor(*colors[i])
        glPointSize(2)
        pm.draw()

window.Refresh()

def once():
    # 2D colormap preview
    dataset.advance()
    for i,depth in enumerate(dataset.depths):
        nm = "depth_%d" % (i,)
        cv2.namedWindow(nm, cv2.WINDOW_NORMAL)
        show_depth(nm, depth)
        cv2.waitKey(5)
        cv2.resizeWindow(nm, 640/2, 480/2)
        cv2.moveWindow(nm, 640/2*i,0)
    cv2.waitKey(5)
    
    # 3D point cloud view
    global points, rimgs
    rimgs = []
    points = []
    for i,depth in enumerate(dataset.depths):
        rimg = RangeImage(depth, cam)
        if dataset.rgbs and 0:
            rimg.compute_points()
            pm = rimg.point_model()
            rgb = dataset.rgbs[i]
            pm.rgba = np.empty((rgb.shape[0]*rgb.shape[1],4),dtype='f')
            pm.rgba[:,:3] = rgb.reshape((-1,3)).astype('f')[:,::-1]/256.0
        else:
            rimg.compute_points()
            rimg.compute_normals()
            pm = rimg.point_model()
        if dataset.calib_mats:
            pm.RT = dataset.calib_mats[1][i]
        rimgs.append(rimg)
        points.append(pm)
        
    #pts = (points.RT[:3,3] + points.xyz[:,:3])
    #window.lookat = pts[~np.isnan(pts.sum(0))].mean(0)
    window.Refresh()
    pylab.waitforbuttonpress(0.03)
    #cv2.waitKey(50)
    
def start(dset=None):
    if dset is None:
        dataset.load_random_dataset()
    else:
        dataset.load_dataset(dset)

def resume():
    while True:
        dataset.advance()
        once()

def go(dset=None):
    start(dset)
    resume()
