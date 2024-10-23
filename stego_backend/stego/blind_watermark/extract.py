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
    print("使用方法: python extract.py <embedimage_path> <embed_len> <extract_txt>")
    sys.exit(1)
        
# 获取命令行参数
embedimage_path = sys.argv[1]
embed_len = sys.argv[2]
extract_txt = sys.argv[3]


try:
    int_value = int(embed_len)
    
    result1 = check_file_and_format(embedimage_path, "bmp")
    if result1:
        result2 = check_format(extract_txt, "txt")
        if result2:
            len_wm = int_value  

            bwm1 = WaterMark(password_img=1, password_wm=1)
            wm_extract = bwm1.extract(embedimage_path, wm_shape=len_wm, mode='str')

            print(wm_extract)

            with open(extract_txt, 'w', encoding='utf-8') as file:
                    file.write(wm_extract)

        else:
            print(extract_txt + "文件路径或格式不正确，应为txt格式文件")
            sys.exit(1)


    else:
        print(embedimage_path + "文件路径或格式不正确，应为bmp格式文件")
        sys.exit(1)



except ValueError:
    print("embed_len " + embed_len + " 不是一个有效的整数")







