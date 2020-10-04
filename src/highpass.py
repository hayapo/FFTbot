import cv2
import numpy as np
from matplotlib import pyplot as plt
from pylab import rcParams

IMG_PATH = './images/before.png'

def highpass_fft():
    rcParams['figure.figsize'] = 15, 10
    #grayscaleで読み込み
    img = cv2.imread(IMG_PATH,0)
    rows, cols = img.shape
    #画像の中心
    crow,ccol = int(rows/2) , int(cols/2)
    #フィルタする原点付近の幅
    reg = 50
    f = np.fft.fft2(img)
    fshift = np.fft.fftshift(f)
    #フーリエ変換像からフィルタ
    fshift[crow-reg:crow+reg, ccol-reg:ccol+reg] = 0
    #逆フーリエ変換で画像に戻す
    f_ishift = np.fft.ifftshift(fshift)
    img_back = np.fft.ifft2(f_ishift)
    img_back = np.abs(img_back)

    plt.subplot(121),plt.imshow(img, cmap = 'gray')
    plt.title('Input Image'), plt.xticks([]), plt.yticks([])
    plt.subplot(122),plt.imshow(img_back)
    plt.title('Result in JET'), plt.xticks([]), plt.yticks([])
    plt.savefig('./results/figure.png')

if __name__ == '__main__':
    highpass_fft()