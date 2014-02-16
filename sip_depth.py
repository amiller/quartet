import snappy
import numpy as np
import glob
import cv2
for x in glob.glob('sip/*.snappy'):
    data = np.asfarray(np.fromstring(snappy.decompress(open(x).read()), dtype=np.uint16).reshape((480, 640)))
    data_sorted = sorted(data.ravel())
    Mval = float(data_sorted[len(data_sorted) - len(data_sorted) / 20])
    mval = float(data_sorted[len(data_sorted) / 20])
    data = np.asarray(np.clip(255 * (data - mval) / (Mval - mval), 0, 255), dtype=np.uint8)
    cv2.imwrite(x + '.png', data)
