import freenect
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
    while 1: 
        cmd = socket.recv()
        print 'command', cmd
        if cmd == 'getframe':
            depth,_ = freenect.sync_get_depth(0,freenect.DEPTH_REGISTERED)
            rgb,_ = freenect.sync_get_video(0)
            socket.send_pyobj((depth,rgb))

if __name__ == '__main__': main()
