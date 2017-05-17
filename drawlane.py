import numpy as np
import cv2


def lane_image(warped, origin, in_m, ploty, left_fit, right_fit, left_curve, right_curve, distance):
    # Create an image to draw the lines on
    warp_zero = np.zeros_like(warped).astype(np.uint8)
    color_warp = np.dstack((warp_zero, warp_zero, warp_zero))

    left_fitx = left_fit[0] * ploty ** 2 + left_fit[1] * ploty + left_fit[2]
    right_fitx = right_fit[0] * ploty ** 2 + right_fit[1] * ploty + right_fit[2]

    # Recast the x and y points into usable format for cv2.fillPoly()
    pts_left = np.array([np.transpose(np.vstack([left_fitx, ploty]))])
    pts_right = np.array([np.flipud(np.transpose(np.vstack([right_fitx, ploty])))])
    pts = np.hstack((pts_left, pts_right))

    # Draw the lane onto the warped blank image
    cv2.fillPoly(color_warp, np.int_([pts]), (0,255, 0))

    # Warp the blank back to original image space using inverse perspective matrix (Minv)
    newwarp = cv2.warpPerspective(color_warp, in_m, (warped.shape[1], warped.shape[0]))
    # Combine the result with the original image
    output = cv2.addWeighted(origin, 1, newwarp, 0.3, 0)
    cv2.putText(output, 'left_curve: ' + str(left_curve), (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255,0), 2, cv2.LINE_AA)
    cv2.putText(output, 'right_curve: ' + str(right_curve), (50, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2,
                cv2.LINE_AA)
    return cv2.putText(output, 'distance: ' + str(distance), (50, 130), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2,
                cv2.LINE_AA)

