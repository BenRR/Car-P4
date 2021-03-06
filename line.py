import numpy as np
import findlane


# Define a class to receive the characteristics of each line detection
class Line:
    def __init__(self):
        # cache frame numbers
        self.frame_n = 15 
        # was the line detected in the last iteration?
        self.detected = False
        self.leftfit = None
        self.leftx = None
        self.lefty = None
        self.recent_leftfit = []
        self.recent_leftx = []
        self.recent_lefty = []
        self.rightfit = None
        self.rightx = None
        self.righty = None
        self.recent_rightfit = []
        self.recent_rightx = []
        self.recent_righty = []
        self.left_best_fit = None
        self.right_best_fit = None
        self.left_curve = None
        self.right_curve = None
        self.left_curve_m = None
        self.right_curve_m = None
        self.center_dist = None
        self.ploty = findlane.get_ploty()

    def update(self, image):
        if self.detected:
            leftfit, rightfit, leftx, rightx, lefty, righty = \
                findlane.find_lane_continue(image, self.leftfit, self.rightfit)
        else:
            leftfit, rightfit, leftx, rightx, lefty, righty =\
                findlane.find_lane(image)

        left_accept =  accept(leftfit, self.leftfit)
        right_accept = accept(rightfit, self.rightfit)

        if left_accept and right_accept:
            self.leftfit = leftfit
            self.leftx = leftx
            self.lefty = lefty
            self.recent_leftfit.append(leftfit)
            self.recent_leftx.append(leftx)
            self.recent_lefty.append(lefty)

            self.rightfit = rightfit
            self.rightx = rightx
            self.righty = righty
            self.recent_rightfit.append(rightfit)
            self.recent_rightx.append(rightx)
            self.recent_righty.append(righty)
            # self.detected = True
        else:
            self.detected = False

        if left_accept or right_accept:
            if len(self.recent_leftfit) > self.frame_n:
                self.recent_leftfit.pop(0)
                self.recent_leftx.pop(0)
                self.recent_lefty.pop(0)
                # re-detect if cache is full
                self.detected = False
            if len(self.recent_rightfit) > self.frame_n:
                self.recent_rightfit.pop(0)
                self.recent_rightx.pop(0)
                self.recent_righty.pop(0)
                # re-detect if cache is full
                self.detected = False

            self.left_best_fit = np.average(self.recent_leftfit, axis=0)
            self.right_best_fit = np.average(self.recent_rightfit, axis=0)
            self.left_curve, self.right_curve = \
                findlane.calculate_curve(self.left_best_fit, self.right_best_fit)
            self.center_dist = findlane.center_dist(self.left_best_fit, self.right_best_fit)

        if not(self.leftx is None) and not(self.rightx is None) and not(self.righty is None) and not(self.lefty is None):
            self.left_curve_m, self.right_curve_m = \
                findlane.calculate_curve_radius(leftx, rightx, lefty, righty)


def accept(current_fit, previous_fit):
    if previous_fit is None:
        return True
    else:
        y = findlane.get_maxy()
        previous_base = previous_fit[0] * (y ** 2) + previous_fit[1] * y + previous_fit[2]
        current_base = current_fit[0] * (y ** 2) + current_fit[1] * y + current_fit[2]
        if abs(previous_base - current_base) > 500:
            return False
        previous_curve = findlane.calculate_single_curve(previous_fit)
        current_curve = findlane.calculate_single_curve(current_fit)
        if abs(previous_curve - current_curve) > 4000:
            return False
        return True

