from PIL import Image
import os

# 图像文件路径
image_path1 = './embedded_rotate/embedded_ROT_10.bmp'
image_path2 = './embedded_rotate/embedded_ROT_25.bmp'
image_path3 = './embedded_rotate/embedded_ROT_45.bmp'
# 输出文件夹
output_folder = 'embedded_rotate'

# 确保输出目录存在
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# 加载图像
original_image1 = Image.open(image_path1)
original_image2 = Image.open(image_path2)
original_image3 = Image.open(image_path3)
# 旋转5度
#rotated_image = original_image.rotate(-5, resample=Image.BICUBIC, expand=True)

# 保存旋转后的图像
#rotated_path = os.path.join(output_folder, 'rotated_5_degrees.bmp')
#rotated_image.save(rotated_path)

# 尝试还原图像，通过相反的旋转
restored_image1 = original_image1.rotate(-10, resample=Image.BICUBIC, expand=True)
restored_image2 = original_image2.rotate(-25, resample=Image.BICUBIC, expand=True)
restored_image3 = original_image3.rotate(-45, resample=Image.BICUBIC, expand=True)
# 保存还原后的图像
restored_path = os.path.join(output_folder, 'restored_image_10.bmp')
restored_image1.save(restored_path)
restored_path = os.path.join(output_folder, 'restored_image_25.bmp')
restored_image2.save(restored_path)
restored_path = os.path.join(output_folder, 'restored_image_45.bmp')
restored_image3.save(restored_path)

import cv2

# 读取图像
img1 = cv2.imread('./embedded_rotate/restored_image_10.bmp')
img2 = cv2.imread('./embedded_rotate/restored_image_25.bmp')
img3 = cv2.imread('./embedded_rotate/restored_image_45.bmp')
# 计算中心裁剪的坐标
center_x, center_y = img1.shape[1] // 2, img1.shape[0] // 2
half_width, half_height = 512 // 2, 512 // 2
top = center_y - half_height
bottom = center_y + half_height
left = center_x - half_width
right = center_x + half_width

# 裁剪图像
cropped_img = img1[top:bottom, left:right]

# 保存裁剪后的图像
cv2.imwrite('./embedded_rotate/center_cropped_10.bmp', cropped_img)


# 计算中心裁剪的坐标
center_x, center_y = img2.shape[1] // 2, img2.shape[0] // 2
half_width, half_height = 512 // 2, 512 // 2
top = center_y - half_height
bottom = center_y + half_height
left = center_x - half_width
right = center_x + half_width

# 裁剪图像
cropped_img = img2[top:bottom, left:right]

# 保存裁剪后的图像
cv2.imwrite('./embedded_rotate/center_cropped_25.bmp', cropped_img)

# 计算中心裁剪的坐标
center_x, center_y = img3.shape[1] // 2, img3.shape[0] // 2
half_width, half_height = 512 // 2, 512 // 2
top = center_y - half_height
bottom = center_y + half_height
left = center_x - half_width
right = center_x + half_width

# 裁剪图像
cropped_img = img3[top:bottom, left:right]

# 保存裁剪后的图像
cv2.imwrite('./embedded_rotate/center_cropped_45.bmp', cropped_img)

from blind_watermark.blind_watermark import WaterMark

# 获取当前目录的绝对路径
current_directory = os.path.abspath('.')


bwm1 = WaterMark(password_img=1, password_wm=1)

wm_extract = bwm1.extract(os.path.join(current_directory, 'embedded_rotate', 'center_cropped_10.bmp'), wm_shape=248, mode='str')
print("提取rotate10°的信息：", wm_extract)

wm_extract = bwm1.extract(os.path.join(current_directory, 'embedded_rotate', 'center_cropped_25.bmp'), wm_shape=248, mode='str')
print("提取rotate25°的信息：", wm_extract)

wm_extract = bwm1.extract(os.path.join(current_directory, 'embedded_rotate', 'center_cropped_45.bmp'), wm_shape=248, mode='str')
print("提取rotate45°的信息：", wm_extract)
