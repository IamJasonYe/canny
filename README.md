# Canny_edgeDetector
## About the project 

This is a project based on the lecture, *Digital System and Design* , by Prof. Wang. It aims at implementing a hardware architecture to boost the speed of computation by parallel design and some tricks of optimization to achieve the real-time video analysis goal. 

## TODO List

- [x] Analyze the needs and the features of the project.
- [ ] Devide the module and interfaces based on above.
- [ ]  Write the documentations. 
- [ ] Implement the code

## Needs and features
### Needs

1. A basic one: given a static picture or a frame of video, it can detect the edge of the picture.
2. A tough one (Performance requirement): given a video, it can detect the edge in real time, which means it can handle at least 25 frames per second.
3. Image size or resolution: 200x200 pixels for pictures.  1280x720@25fps for videos.

### Features

1. It runs on FPGA for evaluating, thus it should be controllable for playing and pausing the video.
2. It could see the difference between original source and the output source.

## Modules and Interfaces

<img src="/img">