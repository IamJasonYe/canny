#encoding=utf-8
from PIL import Image, ImageFilter
import matplotlib.pyplot as plt
import numpy as np
def main():
    im = Image.open("lenna.png").convert('L')
    width, height = im.size
    im_gaussian = im.filter(ImageFilter.GaussianBlur)
    im.show(title="Original")
    # Gaussian Filtering
    #im_gaussian.show(title="Gaussian_filtered")
    # Gradient Calculation
    p = np.asarray(im_gaussian.transpose(Image.FLIP_TOP_BOTTOM)).astype('uint8')
    x, y = np.mgrid[0:height, 0:width]
    dy, dx = np.gradient(p)
    skip = (slice(None, None, 3), slice(None, None, 3))
    fig, ax = plt.subplots()
    im = ax.imshow(im,extent=[x.min(), x.max(), y.min(), y.max()])
    plt.colorbar(im)
    ax.quiver(x[skip], y[skip], dx[skip].T, dy[skip].T)
    ax.set(aspect=1, title='Quiver Plot')
    # plt.show()
    gradient =  np.sqrt(dy * dy + dx * dx)
    # print dx[15][15], dy[15][15], gradient[15][15]
    direction = np.arctan2(dy,dx)
    plt.close()
    gradient_norm = np.abs((gradient - np.mean(gradient)) / (1.0*np.std(gradient)))
    im_gradient = Image.fromarray( np.uint8(255-np.clip(gradient_norm * 255,200,255))).transpose(Image.FLIP_TOP_BOTTOM)
    im_gradient.show()
    np.NAN
if __name__ == "__main__":
	main()
