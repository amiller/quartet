import config
import glob
import os
import time
import re

def check_dir(name, d, extension, fn_re, recent_time=30.):
    data = [float(fn_re.search(fn).groups()[0])
            for fn in sorted(glob.glob(d + "/*" + extension))]
    data.sort()
    cur_time = time.time()
    counts_recent = 0
    for x in data:
        if cur_time - x < recent_time:
            counts_recent += 1
    duration = data[-1] - data[0]
    fps = len(data) / float(duration)
    fps_recent = counts_recent / min(float(duration), recent_time)
    print('[%s][%s] Last (sec): %.2f Dur (sec): %.1f Cam: %.2f CamRecent: %.2f Fps: %.2f FpsRecent: %.2f' % (name, extension, (time.time() - data[-1]), duration, len(data), counts_recent, fps, fps_recent))

try:
    eye_dir = sorted(glob.glob(config.EYE_PATH + '/*'))[-1]
except IndexError:
    pass
else:
    check_dir('eye', eye_dir, '.jpg', re.compile('.+/.+_(.+)_.+_.+\..+'))

try:
    kinect_dir = sorted(glob.glob(config.KINECT_PATH + '/*'))[-1]
except IndexError:
    pass
else:
    check_dir('kinect', kinect_dir, '.snappy', re.compile('.+/.+-(.+)-.+\..+'))
    check_dir('kinect', kinect_dir, '.jpg', re.compile('.+/.+-(.+)-.+\..+'))
