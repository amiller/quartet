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
    colors = [[1,0,0],[0,1,0],[0,0,1]]
    for i,pm in enumerate(points):
        glColor(*colors[i])
        glPointSize(2)
        pm.draw()

def solve_rotation():
    global calib_points,points

    global pts
    pts = []
    for rimg,p in zip(rimgs,calib_points):
        pts2 = []
        for cp in p:
            pts2.append(rimg.xyz[int(cp[1]),int(cp[0]),:])
        pts.append(pts2)
    pts = np.array(pts)

    # Register each to the first
    t0 = pts[0].mean(1)
    fixes = []
    import transformations
    global mats
    mats = [np.eye(4)]
    for p in pts[1:]:
        v0 = np.concatenate((pts[0],pts[0]))
        v1 = np.concatenate((p,p))
        mat = transformations.affine_matrix_from_points(v0.T,v1.T,shear=False,scale=False)
        mats.append(mat)
        print v0 - v1
        print (np.dot(mat[:3,:3],v0.T).T+mat[:3,3].T) - v1
    points[1].RT = np.linalg.inv(mats[1])
    return mats

def burger_calib():
    cams = (0,1)

    global calib_points
    calib_points = [[] for _ in cams]
    for cam in cams:
        fig = figure(1);
        clf();
        def pick(event):
            calib_points[cam].append((event.xdata, event.ydata))
            print('Picked point %d of 3' % (len(calib_points[cam])))

        depth = dataset.depths[cam]
        # imshow(depth)
        imshow(1./depth)

        cid = fig.canvas.mpl_connect('button_press_event', pick)
        print("Camera %d of %d" % (cam, len(cams)))
        print("Click the middle of each of the three balls, in clockwise order, starting from the left")
        try:
            while len(calib_points[cam]) < 3:
                waitforbuttonpress(0.001)
        finally:
            fig.canvas.mpl_disconnect(cid)
        print 'OK'

    #np.save('%s/config/boundpts_%d' % (newest_folder, cam), points)
    #np.save('%s/config/depth_%d' % (newest_folder, cam), depth)



window.Refresh()

def show_depth(name, depth):
    cv2.imshow(name, 1024./depth)

def once():
    # 2D colormap preview
    dataset.advance()
    if 0:
        for i,depth in enumerate(dataset.depths):
            show_depth("depth_%d" % (i,), depth)
        for i,rgb in enumerate(dataset.rgbs):
            cv2.imshow("rgb_%d"%(i,),rgb)
    
    # 3D point cloud view
    global points, rimgs
    rimgs = []
    points = []
    for i,depth in enumerate(dataset.depths):
        rimg = RangeImage(depth, cam)
        if dataset.rgbs:
            rimg.compute_points()
            pm = rimg.point_model()
            rgb = dataset.rgbs[i]
            pm.rgba = np.empty((rgb.shape[0]*rgb.shape[1],4),dtype='f')
            pm.rgba[:,:3] = rgb.reshape((-1,3)).astype('f')[:,::-1]/256.0
        else:
            # rimg.filter()
            rimg.compute_points()
            rimg.compute_normals()
            pm = rimg.point_model()
        global mats
        if "mats" in globals():
            pm.RT = np.linalg.inv(mats[i])
        rimgs.append(rimg)
        points.append(pm)
        
    #pts = (points.RT[:3,3] + points.xyz[:,:3])
    #window.lookat = pts[~np.isnan(pts.sum(0))].mean(0)
    window.Refresh()
    pylab.waitforbuttonpress(0.03)
    #cv2.waitKey(50)
    

def go(dset=None):
    if dset is None:
        dataset.load_random_dataset()
    else:
        dataset.load_dataset(dset)

    while True:
        dataset.advance()
        once()
