#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# embed string
import sys
import numpy as np
from blind_watermark import WaterMark
import cv2
import os


def check_file_and_format(file_path, expected_format):
    """
    检查指定路径的文件是否存在，并且是否为指定格式。
    
    :param file_path: 文件的路径
    :param expected_format: 期望的文件格式，例如 'txt', 'jpg' 等
    :return: 如果文件存在并且格式正确，返回 True，否则返回 False
    """
    # 检查文件是否存在
    if os.path.exists(file_path):
        # 获取文件扩展名
        _, file_extension = os.path.splitext(file_path)
        # 检查文件扩展名是否与期望的格式匹配
        if file_extension.lower() == '.' + expected_format.lower():
            return True
    return False

def check_format(file_path, expected_format):
    """
    检查指定路径的文件是否存在，并且是否为指定格式。
    
    :param file_path: 文件的路径
    :param expected_format: 期望的文件格式，例如 'txt', 'jpg' 等
    :return: 如果文件存在并且格式正确，返回 True，否则返回 False
    """
    # 获取文件扩展名
    _, file_extension = os.path.splitext(file_path)
    # 检查文件扩展名是否与期望的格式匹配
    if file_extension.lower() == '.' + expected_format.lower():
        return True

    return False



if len(sys.argv) != 4:
    print("使用方法: python embed.py <image_path> <plaintext_path> <output_path>")
    sys.exit(1)
        
# 获取命令行参数
image_path = sys.argv[1]
plaintext_path = sys.argv[2]
output_path = sys.argv[3]


result1 = check_file_and_format(image_path, "bmp")
if result1:
    result2 = check_file_and_format(plaintext_path, "txt")
    if result2:
        result3 = check_format(output_path, "bmp")
        if result3:

            try:
                bwm = WaterMark(password_img=1, password_wm=1)
                bwm.read_img(image_path)

                with open(plaintext_path, 'r', encoding='utf-8') as file:
                        wm = file.read()
                        
                bwm.read_wm(wm, mode='str')
                bwm.embed(output_path)

                print("嵌入成功，嵌入长度为" + str(len(bwm.wm_bit)))

            except AssertionError as error:
                # 捕获 AssertionError 并打印错误信息
                print(f"发生断言错误: {error}")

        else:
            print(output_path + "文件路径或格式不正确，应为bmp格式文件")
            sys.exit(1)


    else:
        print(plaintext_path + "文件路径或格式不正确，应为txt格式文件")
        sys.exit(1)


else:
    print(image_path + "文件路径或格式不正确，应为bmp格式文件")
    sys.exit(1)



# # os.chdir(os.path.dirname(__file__))
# file_path = "plaintext.txt"
# # extract_txt = "extract.txt"

# bwm = WaterMark(password_img=1, password_wm=1)
# bwm.read_img('lena.bmp')

# with open(file_path, 'r', encoding='utf-8') as file:
#         wm = file.read()
        
# bwm.read_wm(wm, mode='str')
# bwm.embed('embedded.bmp')

# len_wm = len(bwm.wm_bit)  # 解水印需要用到长度
# print('Put down the length of wm_bit {len_wm}'.format(len_wm=len_wm))

# ori_img_shape = cv2.imread('lena.bmp').shape[:2]  # 抗攻击有时需要知道原图的shape
# h, w = ori_img_shape

# bwm1 = WaterMark(password_img=1, password_wm=1)
# wm_extract = bwm1.extract('embedded.bmp', wm_shape=len_wm, mode='str')

# print(wm_extract)

# with open(extract_txt, 'w', encoding='utf-8') as file:
#         file.write(wm_extract)


