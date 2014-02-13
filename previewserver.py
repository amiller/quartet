import opennpy
import numpy as np
import dataset
import cv2
import hashlib
import snappy
import zmq

def main():
    context = zmq.Context()
    socket = context.socket(zmq.PAIR)
    socket.bind('tcp://*:4567')
    opennpy.align_depth_to_rgb()
    while 1: 
        cmd = socket.recv()
        print 'command', cmd
        if cmd == 'getframe':
            depth,_ = opennpy.sync_get_depth(0)
            rgb,_ = opennpy.sync_get_video(0)
            socket.send_pyobj((depth,rgb))

if __name__ == '__main__': main()
