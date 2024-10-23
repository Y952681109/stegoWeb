import cv2

def main():
    # 读取图像
    img1 = cv2.imread('bmp/1.bmp')
    img2 = cv2.imread('out.bmp')

    # 计算PSNR
    psnr_value = cv2.PSNR(img1, img2)
    print("PSNR value:", psnr_value)

if __name__ == "__main__":
    main()
