import matplotlib
matplotlib.use('WX')
import record
import view2d
import signal
import sys
import argparse
import subprocess
from config import NUM_KINECTS, KINECT_PATH
import time
import os

def main():
    parser = argparse.ArgumentParser(description='Kinect Data Saver')
    subparsers = parser.add_subparsers()
    subparser = subparsers.add_parser('display')
    subparser.set_defaults(mode='display')
    subparser = subparsers.add_parser('save')
    subparser.add_argument('--decimate', dest='decimate', type=int, default='0')
    subparser.set_defaults(mode='save')
    subparser = subparsers.add_parser('playback')
    subparser.set_defaults(mode='playback')
    subparser.add_argument('--index', type=int, default=-1)
    subparser.add_argument('--skip', type=int, default=1)
    subparser = subparsers.add_parser('playback3d')
    subparser.set_defaults(mode='playback3d')
    args = vars(parser.parse_args())    
    mode = args['mode']
    if mode == 'display':
        subprocess.call('regview', shell=True)
    elif mode == 'playback':
        import glob
        import viewfakenect
        sets = glob.glob(KINECT_PATH + '/*/')
        viewfakenect.view(sorted(sets)[args['index']], skip=args['skip'])
    elif mode == 'playback3d':
        import viewdataset
        viewdataset.go(path=KINECT_PATH, threed=True)
    elif mode == 'save':
        mkdir_p(KINECT_PATH)
        subprocess.call('regview %s/%f %s' % (KINECT_PATH, time.time(), args['decimate']), shell=True)

def mkdir_p(path):
    import errno
    try:
        os.makedirs(path)
    except OSError as exc: # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else: raise

if __name__ == '__main__':
    main()

