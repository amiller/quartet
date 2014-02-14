import matplotlib
matplotlib.use('WX')
import record
import view2d
import signal
import sys
import argparse
from config import NUM_KINECTS, KINECT_PATH

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
        while 1:
            view2d.preview(range(NUM_KINECTS))
    elif mode == 'playback':
        import viewdataset
        viewdataset.go(path=KINECT_PATH)
    elif mode == 'playback3d':
        import viewdataset
        viewdataset.go(path=KINECT_PATH, threed=True)
    elif mode == 'save':
        record.record(cams=range(NUM_KINECTS), do_rgb=True)

if __name__ == '__main__':
    main()

