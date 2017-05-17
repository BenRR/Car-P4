import calibration
import imagefilter
import warp
import drawlane
import sys
from moviepy.editor import VideoFileClip
from line import Line


def process_video(video_file):
    lane_line = Line()
    cali_dict = calibration.cam_cali()
    warp_src, warp_dst = warp.warp_points()
    warp_m, in_m = warp.warp_ms(warp_src,warp_dst)

    def process_full(img):
        cali_img = calibration.cali_img(img, cali_dict)
        warped_img = warp.warp_img(cali_img, warp_m)
        filtered_img = imagefilter.color_gradient_filter(warped_img)
        lane_line.update(filtered_img)
        output = drawlane.lane_image(filtered_img, img,in_m, lane_line.ploty,
                                     lane_line.left_best_fit,lane_line.right_best_fit,
                                     lane_line.left_curve, lane_line.right_curve,
                                     lane_line.center_dist)
        return output

    clip = VideoFileClip(video_file)
    return clip.fl_image(process_full) #NOTE: this function expects color images!!

if __name__ == '__main__':
    assert (len(sys.argv) == 3), 'Need input and output video file names.'
    white_output = sys.argv[2]
    white_clip = process_video(sys.argv[1])
    white_clip.write_videofile(white_output, audio=False)

