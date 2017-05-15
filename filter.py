import numpy as np
import cv2


def color_filter(img):
    HSV = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
    # For yellow
    lane_yellow = cv2.inRange(HSV, (20, 100, 100), (50, 255, 255))
    # For white
    sensitivity_1 = 68
    lane_white = cv2.inRange(HSV, (0, 0, 255 - sensitivity_1), (255, 20, 255))
    sensitivity_2 = 60
    HSL = cv2.cvtColor(img, cv2.COLOR_RGB2HLS)
    lane_white_1 = cv2.inRange(HSL, (0, 255 - sensitivity_2, 0), (255, 255, sensitivity_2))
    lane_white_2 = cv2.inRange(img, (200, 200, 200), (255, 255, 255))

    return lane_yellow | lane_white | lane_white_2 | lane_white_1


def gradient_filter(img):
    # Grayscale image
    # NOTE: we already saw that standard grayscaling lost color information for the lane lines
    # Explore gradients in other colors spaces / color channels to see what might work better
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

    # Sobel x
    sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0)  # Take the derivative in x
    abs_sobelx = np.absolute(sobelx)  # Absolute x derivative to accentuate lines away from horizontal
    scaled_sobel = np.uint8(255 * abs_sobelx / np.max(abs_sobelx))

    # Threshold x gradient
    thresh_min = 40
    thresh_max = 100
    sxbinary = np.zeros_like(scaled_sobel)
    sxbinary[(scaled_sobel >= thresh_min) & (scaled_sobel <= thresh_max)] = 1

    # Combine the two binary thresholds
    binary = np.zeros_like(sxbinary)
    binary[sxbinary == 1] = 1
    return binary


def filter_img(img):
    gradient_filter(img) | color_filter(img)

