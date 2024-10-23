#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# embed string
import numpy as np
from blind_watermark import WaterMark
import cv2
import os

# os.chdir(os.path.dirname(__file__))
file_path = "plaintext.txt"
extract_txt = "extract.txt"

bwm = WaterMark(password_img=1, password_wm=1)
bwm.read_img('lena.bmp')

with open(file_path, 'r', encoding='utf-8') as file:
        wm = file.read()
        
bwm.read_wm(wm, mode='str')
bwm.embed('embedded.bmp')

len_wm = len(bwm.wm_bit)  # 解水印需要用到长度
print('Put down the length of wm_bit {len_wm}'.format(len_wm=len_wm))

ori_img_shape = cv2.imread('lena.bmp').shape[:2]  # 抗攻击有时需要知道原图的shape
h, w = ori_img_shape

bwm1 = WaterMark(password_img=1, password_wm=1)
wm_extract = bwm1.extract('embedded.bmp', wm_shape=len_wm, mode='str')

print(wm_extract)

with open(extract_txt, 'w', encoding='utf-8') as file:
        file.write(wm_extract)


