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

def show_depth(name, depth):
    cv2.imshow(name, colormap.color_map(depth/2))

def once():
    # 2D colormap preview
    dataset.advance()
    for i,depth in enumerate(dataset.depths):
        show_depth("depth_%d" % (i,), depth)
    
    # 3D point cloud view
    depth = dataset.depths[0]
    rimg = RangeImage(depth, cam)
    global points
    if dataset.rgbs:
        rimg.compute_points()
        points = rimg.point_model()
        rgb = dataset.rgbs[0]
        points.rgba = np.empty((rgb.shape[0]*rgb.shape[1],4),dtype='f')
        points.rgba[:,:3] = rgb.reshape((-1,3)).astype('f')/256.0
    else:
        #rimg.filter()
        rimg.compute_points()
        rimg.compute_normals()
        points = rimg.point_model()

        
    #pts = (points.RT[:3,3] + points.xyz[:,:3])
    #window.lookat = pts[~np.isnan(pts.sum(0))].mean(0)
    print window.lookat
    window.Refresh()

    #pylab.waitforbuttonpress(0.05)
    cv2.waitKey(50)
    

def go(dset=None):
    if dset is None:
        dataset.load_random_dataset()
    else:
        dataset.load_dataset(dset)

    while True:
        dataset.advance()
        once()
