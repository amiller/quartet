import opennpy
import numpy as np
import os
import shutil
import cv
import subprocess
import dataset
import colormap
import pylab

def show_depth(name, depth):
    im = cv.CreateImage((depth.shape[1],depth.shape[0]), 8, 3)
    cv.SetData(im, colormap.color_map(depth/2))
    cv.ShowImage(name, im)

def go(dset=None):
    if dset is None:
        dataset.load_random_dataset()
    else:
        dataset.load_dataset(dset)

    while True:
        dataset.advance()
        for i,depth in enumerate(dataset.depths):
            show_depth("depth_%d" % (i,), depth)
        pylab.waitforbuttonpress(0.05)
