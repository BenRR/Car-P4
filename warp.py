import cv2
import numpy as np
import pickle
import os


def warp_ms():
    src = np.float32(
        [[285, 670],
         [1075, 670],
         [605, 440],
         [670, 440]
        ]
    )
    dst = np.float32(
        [[385, 700],
         [975, 700],
         [385, 0],
         [975, 0]
        ]
    )

    pickle_file = 'warp.p'
    if os.path.isfile(pickle_file):
        cali_dict = pickle.load(open(pickle_file, 'rb'))
        return cali_dict['m'], cali_dict['in_m']

    m = cv2.getPerspectiveTransform(src, dst)
    in_m = cv2.getPerspectiveTransform(dst, src)

    cali_dict = {'m': m, 'in_m': in_m}
    pickle.dump(cali_dict, open('warp.p', 'wb'))

    return m, in_m


def warp_img(img, mxt):
    img_size = (img.shape[1], img.shape[0])
    return cv2.warpPerspective(img, mxt, img_size)
