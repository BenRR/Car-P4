import cv2
import numpy as np
import pickle
import os


def warp_points():
    src = np.float32(
        [[585, 455],
         [705, 455],
         [1130, 720],
         [190, 720]
        ]
    )
    dst = np.float32(
        [[300, 100],
         [1000, 100],
         [1000, 720],
         [300, 720]
        ]
    )
    return src, dst


def warp_ms(src, dst):

    pickle_file = 'warp.p'
    if os.path.isfile(pickle_file):
        cali_dict = pickle.load(open(pickle_file, 'rb'))
        return cali_dict['m'], cali_dict['in_m']

    m = cv2.getPerspectiveTransform(src, dst)
    in_m = cv2.getPerspectiveTransform(dst, src)

    cali_dict = {'m': m, 'in_m': in_m}
    pickle.dump(cali_dict, open(pickle_file, 'wb'))

    return m, in_m


def warp_img(img, mxt):
    img_size = (img.shape[1], img.shape[0])
    return cv2.warpPerspective(img, mxt, img_size)
