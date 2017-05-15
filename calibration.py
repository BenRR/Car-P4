import os
import pickle
import cv2
import matplotlib.image as mpimg
import numpy as np
import glob


def cam_cali():
    pickle_file = 'cam_cali.p'
    if os.path.isfile(pickle_file):
        return pickle.load(open(pickle_file,'rb'))

    objpoints=[]
    imgpoints=[]
    objp = np.zeros((6*9,3), np.float32)
    objp[:,:2] = np.mgrid[0:9,0:6].T.reshape(-1,2)
    images = glob.glob("camera_cal/calibration*.jpg")

    for image in images:
        img = mpimg.imread(image)
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        ret, corners = cv2.findChessboardCorners(gray, (9,6), None)
        if ret:
            imgpoints.append(corners)
            objpoints.append(objp)
    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)
    cali_dict = {'mtx': mtx, 'dist': dist}
    pickle.dump(cali_dict, open('cam_cali.p','wb'))

    return cali_dict


def cali_img(image, cali_dict):
    mtx = cali_dict['mtx']
    dist = cali_dict['dist']
    return cv2.undistort(image, mtx, dist, None, mtx)

