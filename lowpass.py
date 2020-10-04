import cv2
import numpy as np
from matplotlib import pyplot as plt
from pylab import rcParams

IMG_PATH = './images/before.png'

def lowpass_fft():
    rcParams['figure.figsize'] = 15, 10
    #grayscaleで読み込み
    img = cv2.imread(IMG_PATH,0)

    dft = cv2.dft(np.float32(img),flags = cv2.DFT_COMPLEX_OUTPUT)
    dft_shift = np.fft.fftshift(dft)
    magnitude_spectrum = 20*np.log(cv2.magnitude(dft_shift[:,:,0],dft_shift[:,:,1]))
    rows, cols = img.shape
    crow,ccol = int(rows/2) , int(cols/2)
    fil2 = 20
    # マスク作成
    mask = np.zeros((rows,cols,2),np.uint8)
    mask[crow-fil2:crow+fil2, ccol-fil2:ccol+fil2] = 1

    # フーリエ変換象にマスク適用
    fshift = dft_shift*mask
    #逆フーリエ変換で画像に戻す
    f_ishift = np.fft.ifftshift(fshift)
    img_back = cv2.idft(f_ishift)
    img_back = cv2.magnitude(img_back[:,:,0],img_back[:,:,1])

    plt.subplot(121),plt.imshow(img, cmap = 'gray')
    plt.title('Input Image'), plt.xticks([]), plt.yticks([])
    plt.subplot(122),plt.imshow(img_back, cmap = 'gray')
    plt.title('Magnitude Spectrum'), plt.xticks([]), plt.yticks([])
    plt.savefig('./results/figure.png')

if __name__ == '__main__':
    lowpass_fft()
