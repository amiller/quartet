import config
import glob
import os
import time
import re

kinect_dir = sorted(glob.glob(config.KINECT_PATH + '/*'))[-1]
fn_re = re.compile('.+/(.+)_(.+)_(.+)_(.+)\.(.+)')

def check_dir(name, d, prefixes):
    for prefix in prefixes:
        data = [fn_re.search(fn).groups()
                for fn in sorted(glob.glob(d + "/%s_*" % prefix))]
        data = [(x[0], float(x[1]), int(x[2]), int(x[3]), x[4]) for x in data]
        camera_nums = [(x[3], x[1]) for x in data]
        cur_time = time.time()
        camera_counts = {}
        camera_counts_recent = {}
        for camera_num, camera_time in camera_nums:
            if cur_time - camera_time < 30.:
                try:
                    camera_counts_recent[camera_num] += 1
                except KeyError:
                    camera_counts_recent[camera_num] = 1
            try:
                camera_counts[camera_num] += 1
            except KeyError:
                camera_counts[camera_num] = 1
        camera_counts = [str(x) for _, x in sorted(camera_counts.items())]
        camera_counts_recent = [str(x) for _, x in sorted(camera_counts_recent.items())]
        duration = data[-1][1] - data[0][1]
        fps = len(data) / (duration * len(camera_counts))
        print('[%s][%s] Last (sec): %f Dur (sec): %f Cam: %s CamRecent: %s Fps: %f' % (name, prefix, (time.time() - data[-1][1]), duration, ','.join(camera_counts), ','.join(camera_counts_recent), fps))
try:
    eye_dir = sorted(glob.glob(config.EYE_PATH + '/*'))[-1]
    check_dir('eye', eye_dir, ('rgb',))
except IndexError:
    pass
check_dir('kinect', kinect_dir, ('rgb', 'depth'))
