#encoding=utf-8
#
# @Author: Jason Ye
#
from PIL import Image, ImageFilter
from constants import *
import matplotlib.pyplot as plt
import numpy as np

def main():
    im = Image.open("lenna.png").convert('L')
    im.show()
    width, height = im.size
    # Gaussian Filtering
    im_gaussian = im.filter(ImageFilter.GaussianBlur(radius=2))
    im_gaussian.show()
    # Gradient Calculation
    p = np.asanyarray(im_gaussian).astype(np.uint8)
    # showImage(p)
    dy,dx =  get_gradient(p)
    direction = get_direction(dy, dx)
    magnitude = get_magnitude(dy, dx)
    showImage(magnitude)
    nms = nonMaximumSuppression(magnitude, direction)
    showImage(nms)
    result = hysteresisThresholding(nms, direction, thLow=THRESHOLD_LOW, thHigh=THRESHOLD_HIGH)
    showImage(result)

def hysteresisThresholding(nms, direction, thLow=5, thHigh=10):
    print("[+] Begin hysteresis thresholding...")
    result = nms.copy()
    w, h = nms.shape
    for i in xrange(1,h-1):
        for j in xrange(1,w-1):
            if nms[i,j] >= thHigh:
                result[i,j] = EDGE
            elif nms[i,j] <= thLow:
                result[i,j] = NOT_EDGE
            else:
                dir00 = direction[i-1][j-1]; dir01 = direction[i-1][j]; dir02 = direction[i-1][j+1]
                dir10 = direction[i][j-1]  ; dir11 = direction[i][j]  ; dir12 = direction[i][j+1]
                dir20 = direction[i+1][j-1]; dir21 = direction[i+1][j]; dir22 = direction[i+1][j+1]
                isEdge = False
                if dir11 == DEGREE_0 and dir10 == DEGREE_0 and dir12 == DEGREE_0:
                    isEdge = nms[i,j-1] >= thHigh or nms[i, j+1] >= thHigh or result[i,j-1] == EDGE
                elif dir11 == DEGREE_45 and dir02 == DEGREE_45 and dir20 == DEGREE_45:
                    isEdge = nms[i-1, j+1] >= thHigh or nms[i+1, j-1] >= thHigh or result[i-1, j+1] == EDGE
                elif dir11 == DEGREE_90 and dir21 == DEGREE_90 and dir01 == DEGREE_90:
                    isEdge = nms[i-1, j] >= thHigh or nms[i+1, j] >= thHigh or result[i-1, j] == EDGE
                elif dir11 == DEGREE_135 and dir22 == DEGREE_135 and dir00 == DEGREE_135:
                    isEdge = nms[i-1, j-1] >= thHigh or nms[i+1, j+1] >= thHigh or result[i-1, j-1] == EDGE
                result[i,j] = EDGE if isEdge else NOT_EDGE
    print("[+] End hysteresis thresholding!")
    return result

def nonMaximumSuppression(magnitude, direction):
    print("[+] Begin nms...")
    mag = magnitude.copy()
    w, h = magnitude.shape
    for i in xrange(1,h-1):
        for j in xrange(1,w-1):
            mag00 = magnitude[i-1][j-1]; mag01 = magnitude[i-1][j]; mag02 = magnitude[i-1][j+1]
            mag10 = magnitude[i][j-1]  ; mag11 = magnitude[i][j]  ; mag12 = magnitude[i][j+1]
            mag20 = magnitude[i+1][j-1]; mag21 = magnitude[i+1][j]; mag22 = magnitude[i+1][j+1]
            
            dir00 = direction[i-1][j-1]; dir01 = direction[i-1][j]; dir02 = direction[i-1][j+1]
            dir10 = direction[i][j-1]  ; dir11 = direction[i][j]  ; dir12 = direction[i][j+1]
            dir20 = direction[i+1][j-1]; dir21 = direction[i+1][j]; dir22 = direction[i+1][j+1]

            a = c = None
            b = mag11
            if dir11 == DEGREE_0 and dir10 == DEGREE_0 and dir12 == DEGREE_0:
                a,c = mag10,mag12
            elif dir11 == DEGREE_45 and dir02 == DEGREE_45 and dir20 == DEGREE_45:
                a,c = mag20,mag02
            elif dir11 == DEGREE_90 and dir21 == DEGREE_90 and dir01 == DEGREE_90:
                a,c = mag21,mag01
            elif dir11 == DEGREE_135 and dir22 == DEGREE_135 and dir00 == DEGREE_135:
                a,c = mag22,mag00

            if a > b or c > b:
                mag[i][j] = 0
            elif a < b and c < b:
                if dir11 == DEGREE_0:
                    mag[i, j-1] = mag[i, j+1] = 0
                elif dir11 == DEGREE_45:
                    mag[i+1,j-1] = mag[i-1,j+1] = 0
                elif dir11 == DEGREE_90:
                    mag[i-1,j] = mag[i+1,j] = 0
                elif dir11 == DEGREE_135:
                    mag[i-1,j-1] = mag[i+1,j+1] = 0
    print("[+] End nms!")
    return mag

def get_direction(dy, dx):
    print("[+] Begin gradient direction...")
    w, h = dy.shape
    d = np.zeros([w,h], dtype=np.uint8)
    for i in xrange(h):
        for j in xrange(w):
            x = dx[i][j]
            y = dy[i][j]
            if y < 0:
                x = -x
                y = -y
            if x >= 0:
                if  y <= 0.5 * x:
                    d[i][j] = 0
                elif y > 0.5*x and y <= 2.5 * x:
                    d[i][j] = 45
                elif y > 2.5*x:
                    d[i][j] = 90
            elif x <0:
                if  y <= -0.5 * x:
                    d[i][j] = 0
                elif y > -0.5*x and y <= -2.5 * x:
                    d[i][j] = 135
                elif y > -2.5*x:
                    d[i][j] = 90
    print("[+] End gradient direction!")
    return d


def get_gradient(p):
    print("[+] Begin gradient...")
    dy = convolution(p, sobel_y)
    dx = convolution(p, sobel_x)
    print("[+] End gradient!")
    return dy, dx

def get_magnitude(dy, dx):
    print("[+] Begin gradient magnitude...")
    tmp = np.abs(dy) + np.abs(dx)
    print("[+] End gradient magnitude!")
    return norm2Image(0.5 * tmp)


def showImage(arr):
    im = Image.fromarray(arr)
    im.show()

def convolution(arr, operator):
    g = arr.copy().astype(np.int16)
    w, h = arr.shape
    radius = (operator.shape[0] - 1) / 2
    for i in xrange(radius,h-radius):
        for j in xrange(radius, w-radius):
            g[i,j] = (arr[(i-radius):(i+radius+1), (j-radius):(j+radius+1)] * operator).sum()
    # g = norm2Image(g)
    return g

def norm2Image(i):
    i = i * (255.0 / i.max())
    i = i.astype(np.uint8)
    return i

if __name__ == "__main__":
    main()
#    test()
