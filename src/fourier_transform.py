import cv2, boto3, os
import numpy as np
from matplotlib import pyplot as plt
from pylab import rcParams


rcParams['figure.figsize'] = 15, 10

IMG_PATH = './tmp/before.png'

def fft():
    #grayscaleで読み込み
    img = cv2.imread(IMG_PATH,0)
    f = np.fft.fft2(img)
    fshift = np.fft.fftshift(f)
    magnitude_spectrum = 20*np.log(np.abs(fshift))
    plt.subplot(121),plt.imshow(img, cmap = 'gray')
    plt.title('Input Image'), plt.xticks([]), plt.yticks([])
    plt.subplot(122),plt.imshow(magnitude_spectrum, cmap = 'gray')
    plt.title('Magnitude Spectrum'), plt.xticks([]), plt.yticks([])
    plt.savefig('./tmp/figure.png')    

if __name__ == '__main__':
    fft()