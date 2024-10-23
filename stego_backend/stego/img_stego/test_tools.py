import cv2
import random  
import string  
import numpy as np
from PIL import Image 
  
def generate_random_string(length):  
    letters_and_digits = string.ascii_letters + string.digits  
    return ''.join(random.choice(letters_and_digits) for i in range(length))

# random_string = generate_random_string(7)  
# print(random_string)

def compute_psnr(input,output):
    # 读取图像
    img1 = cv2.imread(input)
    img2 = cv2.imread(output)

    # 计算PSNR
    psnr_value = cv2.PSNR(img1, img2)
    return psnr_value

def string_to_bits(s):
    """将字符串转换为比特流。"""
    return ''.join(f'{ord(i):08b}' for i in s)

def calculate_accuracy(original, extracted):
    """计算两个比特流的匹配准确率。"""
    original_bits = string_to_bits(original)
    extracted_bits = string_to_bits(extracted)
    
    # 确保比特流长度一致
    max_len = min(len(original_bits), len(extracted_bits))
    original_bits = original_bits[:max_len]
    extracted_bits = extracted_bits[:max_len]
    
    # 计算匹配的位数
    matches = sum(1 for o, e in zip(original_bits, extracted_bits) if o == e)
    accuracy = matches / max_len * 100  # 计算准确率
    return accuracy


def add_gaussian_noise(image, mean=0, stddev=25):  
    """  
    给图像添加高斯噪声。  
  
    参数:  
    image -- 输入的图像（numpy数组）  
    mean -- 高斯噪声的均值（默认为0）  
    stddev -- 高斯噪声的标准差（默认为25）  
  
    返回:  
    noisy_image -- 添加噪声后的图像（numpy数组）  
    """  
    # 确保图像数据类型为浮点型以进行噪声添加  
    image = image.astype(np.float32)  
  
    # 获取图像的高、宽和通道数  
    h, w, c = image.shape  
  
    # 生成与图像相同形状的高斯噪声  
    noise = np.zeros((h, w, c), np.float32)  
    noise = np.random.normal(mean, stddev, (h, w, c))  
  
    # 将噪声添加到图像上  
    noisy_image = image + noise  
  
    # 确保像素值在0-255范围内  
    noisy_image = np.clip(noisy_image, 0, 255).astype(np.uint8)  
  
    return noisy_image


def add_img_compression(image_path, compressed_img_path, quality):
    # 打开图像  
    img = Image.open(image_path)  
    
    # 保存图像，设置压缩质量（0-100）  
    img.save(compressed_img_path, 'JPEG', quality=quality)


# add_img_compression("steg.jpg", "compressed_steg.jpg", 10)

# image = cv2.imread("steg.jpg")

# # 添加高斯噪声
# noisy_image = add_gaussian_noise(image, mean=0, stddev=2)
# cv2.imwrite("noisy_img1.jpg",noisy_image)

# # 计算PSNR
# psnr1 = compute_psnr("examples/cover.jpg", "steg.jpg")
# psnr2 = compute_psnr("examples/cover.jpg", "noisy_img.jpg")
# print(f"PSNR with original image: {psnr1:.2f}")
# print(f"PSNR with noisy image: {psnr2:.2f}")


# # 示例使用
# original = "testsec"
# extracted = "testsec"
# accuracy = calculate_accuracy(original, extracted)
# print(f"Accuracy: {accuracy:.2f}%")

# psnr = compute_psnr("examples/images2/n0153282900000083.jpg", "steg.jpg")
# print(f"PSNR: {psnr:.2f}")

