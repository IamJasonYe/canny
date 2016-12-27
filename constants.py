import numpy as np
DEGREE_0 = 0
DEGREE_45 = 45
DEGREE_90 = 90
DEGREE_135 = 135

THRESHOLD_LOW = 12
THRESHOLD_HIGH = 30

EDGE = 255
NOT_EDGE = 0

sobel_x = np.array([[-1, 0, 1],
                    [-2, 0, 2],
                    [-1, 0, 1]])

sobel_y = np.array([[1, 2, 1],
                    [0, 0, 0],
                    [-1, -2, -1]])
