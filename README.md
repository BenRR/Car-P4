## Advanced Lane Finding Project

[//]: # (Image References)

[image2]: output_images/image2.png "undistort frame from origin"
[image3]: output_images/image3.png "binary filter Example from origin"
[image4]: output_images/image4.png "Warp frame from origin"
[image5]: output_images/image5.png "detect lane from the binary warped frame"
[image51]: output_images/image51.png "detect lane from the binary warped frame"
[image6]: output_images/image6.png "draw lane back to the original frame"
[image7]: output_images/image7.png "full process pipeline"

### Here I will consider the rubric points individually and describe how I addressed each point in my implementation.  

### Files

* calibration.py    - calculate and persist camera matrix and distortion coefficients
* warp.py           - calculate and persist warp matrix and invert matrix
* imagefilter.py    - color and gradient transforms to filter a image to binary
* findlane.py       - find lanes from a warped binary image and other helper functions to calculate distance and curves
* line.py           - class to cache frames to make video more smooth
* drawlane.py       - plot road lanes on image
* processvideo.py   - main entry to process a video
* output.mp4   - the result video file generated from project_video.mp4

To run the program `python processvideo.py project_video.mp4 output1.mp4` (carnd-term1 minicondo profile required)

### 1. Camera Calibration

Following the lecture I use the provided images from camera_cal folder and `cv2.findChessboardCorners` with size `(9,6)` to collect image points then use `cv2.calibrateCamera` to calculate matrix and coefficients and use pickle to save them into `cam_cali.p` file so the values will be loaded from pickle after creation.
Detailed code is available in `calibration.py`

### Pipeline

#### 1. Distortion-correction.

After calibration matrix and coefficients are persist `cv2.undistort` method can be used to undistort any given image. I have created function `cali_img` in `calibration.py` and later the function is used in `processvideo.py`. Here is result to undistort one example frame.
![alt text][image2]

#### 2. Image Filtering

I used a combination of color and gradient thresholds to generate a binary image (thresholding steps at in `imagefilter.py`). I used codes provided from the lecture which has HLS color space and horizontal gradient filtering then I added HSV color space to filter out lane colors in videos mostly white and yellow. In the end I tune all parameters to get the best result as I can.
Here's an example of my output for this step.

![alt text][image3]

#### 3. Perspective Transformation

The code for my perspective transform includes two functions in `warp.py`. `warp_ms` uses source and destination points that I manually chose to calculate warp matrix and inverse matrix then save them into pickle file. The other function `warp_img` can transform perspective for given image and warp matrix. These methods are used in `processvideo.py` as part of the pipeline.

These are the source and destination points which are return value of `warp_points` function in `warp.py`:

| Source        | Destination   |
|:-------------:|:-------------:|
| 585, 455      | 300, 100        |
| 705, 455      | 1000, 100      |
| 1130, 720     | 1000, 720      |
| 190, 720      | 300, 100        |

I verified that my perspective transform was working as expected by verifying that the lines appear almost parallel in the warped image.

![alt text][image4]

#### 4. Lane Detection

The code for lane detection I used is mostly from the lecture. Function `find_lane` in `findlane.py` can generate lane polynomial fits(left and right) also pixels of left and right lane.
It uses the sliding window search from bottom the picture. In the same file function `find_lane_continue` can skip the window search but find pixels around given previous lane fits.

Here is a plot of polynomial fits from binary warped frame.

![alt text][image5]
![alt text][image51]

#### 5. Curvature Radius and Center Distance

Curvature radius and distance calculation codes are in `findlane.py` by function `alculate_curve_radius` and `center_dist` which are used in `Line.py` later as part of the pipeline. The curvature radius and distance are plotted in the frame as well.

#### 6. Plot Lanes

In file `drawlane.py` function `lane_image` can plot the detected lane polynomial fits with other information like radius and distance. The function is used in `processvideo.py` as part of the pipeline.

![alt text][image6]

#### 7. Pipeline

The main logic is in `processvideo.py` with function `process_video`. It firstly initialises a Line instance which will cache detected lanes. Then loads required configurations like undistort matrixes, coefficients, warp matrixes etc. Then the `process_full` method put all processes together and `clip.fl_image` uses this method to process each frame and generate the output video.

![alt text][image7]

---

### Project Video Result
To get the result video file, just run the program `python processvideo.py project_video.mp4 output1.mp4` (carnd-term1 minicondo profile required)

Here's my result

[![IMAGE ALT TEXT HERE](https://img.youtube.com/vi/9M7rShHZ7Tw/0.jpg)](https://www.youtube.com/watch?v=9M7rShHZ7Tw)

[youtube link](https://youtu.be/9M7rShHZ7Tw)

---

### Discussion

* I found that warp the image then apply binary filtering can give me better result
* Maybe apply region of interesting filter will help
* My current binary filter is not working well with other challenge videos. More tuning should be done if I have more time.
* Better lane acceptance checking and caching needed for challenge videos.
