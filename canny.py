from PIL import Image, ImageFilter
import numpy as np

def main():
    im = Image.open("lenna.png").convert("L")
    w, h = im.size
    #im.show()
    im_gaussian = im.filter(ImageFilter.GaussianBlur(radius=3))
    im_gaussian.show()
    p = np.asarray(im_gaussian)
    dy, dx = np.gradient(p)
    gradient = np.sqrt(dy * dy + dx * dx)
    direction = get_direction(dy,dx)
    g_min, g_max = np.amin(gradient), np.amax(gradient)
    print g_min, g_max
    gradient_norm = np.clip((255.0 * (gradient - g_min ) / (g_max - g_min)),0,255).astype(np.uint8) 
    g_n_clip = np.clip(gradient_norm,200,255)
    im_gradient = Image.fromarray(gradient_norm)
    im_gradient.show()
    #im_clip = Image.fromarray(clip(gradient_norm, 110))
    im_clip = Image.fromarray(clip(gradient, 100))
    im_clip.show()
    threshold = 50
    pre_clip = np.asarray(im_gaussian.filter(ImageFilter.FIND_EDGES))
    im_edge = Image.fromarray(clip(pre_clip,threshold))
    im_edge.show()

def get_direction(dy, dx):
    pass

def clip(gradient_norm, threshold):
    for x in np.nditer(gradient_norm, op_flags=['readwrite']):
        if x >= threshold:
            x[...] = 255
        else:
            x[...] = 0
    return gradient_norm 
def test():
    a = np.array([[1.0, 2.0],[255.5, 256.2]]).astype(np.uint8)
    im = Image.fromarray(a)
    for x in np.nditer(a, op_flags=['readwrite']):
        print x
    #im.show()


if __name__ == "__main__":
    main()
#    test()
