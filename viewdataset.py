import opennpy
import numpy as np
import os
import shutil
import cv
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
def post_draw():
    global points
    if not 'points' in globals(): return

    # Perturbed points (previous estimate)
    glColor(0,1,0)
    glPointSize(1)
    points.draw()

window.Refresh()

def show_depth(name, depth):
    im = cv.CreateImage((depth.shape[1],depth.shape[0]), 8, 3)
    cv.SetData(im, colormap.color_map(depth/2))
    cv.ShowImage(name, im)

def once():
    # 2D colormap preview
    dataset.advance()
    show_depth("depth_0", dataset.depths[0])

    # 3D point cloud view
    depth = dataset.depths[0]
    rimg = RangeImage(depth, cam)
    rimg.compute_points()
    global points
    points = rimg.point_model()
    window.lookat = points.RT[:3,3] + points.xyz[:,:3].mean(0)
    window.Refresh()

    pylab.waitforbuttonpress(0.05)
    

def go(dset=None):
    if dset is None:
        dataset.load_random_dataset()
    else:
        dataset.load_dataset(dset)

    while True:
        once()
