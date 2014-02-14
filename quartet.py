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

def main():
    parser = argparse.ArgumentParser(description='Kinect Data Saver')
    subparsers = parser.add_subparsers()
    subparser = subparsers.add_parser('display')
    subparser.set_defaults(mode='display')
    subparser = subparsers.add_parser('save')
    subparser.set_defaults(mode='save')
    subparser = subparsers.add_parser('playback')
    subparser.set_defaults(mode='playback')
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
        viewfakenect.view(sorted(sets)[-1])
    elif mode == 'playback3d':
        import viewdataset
        viewdataset.go(path=KINECT_PATH, threed=True)
    elif mode == 'save':
        subprocess.call(('regview %s/%f' % (KINECT_PATH, time.time())).split(), shell=True)

if __name__ == '__main__':
    main()

