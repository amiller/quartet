import zmq
import opennpy
import numpy as np
import dataset
import cv2
import hashlib
import snappy

NUM_SERVERS = 5

if 'context' not in globals():
    context = zmq.Context()

if 'sockets' in globals():
    for socket in sockets:
        socket.close()
    del sockets

if 'sockets' not in globals():
    sockets = []
    #for i in range(NUM_SERVERS):
    for i in range(1):
        socket = context.socket(zmq.PAIR)
        #socket.connect('tcp://%d:4567' % (100+i+1,))
        socket.connect('tcp://127.0.0.1:4567')
        sockets.append(socket)

def get_frame(index):
    assert type(index) is int and 0 <= index < NUM_SERVERS
    sockets[index].send('getframe')
    depth, rgb = sockets[index].recv_pyobj()
    print 'got frame', depth, rgb

