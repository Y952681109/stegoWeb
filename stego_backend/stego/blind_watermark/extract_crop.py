import os
import math
from PIL import Image
from blind_watermark.blind_watermark import WaterMark

def reconstruct_original_image(B_path, crop_ratio):
    # 加载裁剪后的图片B
    image_B = Image.open(B_path)

    # 获取图片B的尺寸
    B_width, B_height = image_B.size

    # 根据裁剪比例计算原始图片A的尺寸
    A_width = math.ceil(B_width / crop_ratio)
    A_height = math.ceil(B_height / crop_ratio)

    # 创建一个新的黑色背景图片，尺寸为原始图片A的尺寸
    background = Image.new('RGB', (A_width, A_height), color='black')

    # 计算图片B在背景图片中的位置（居中）
    B_left = (A_width - B_width) // 2
    B_top = (A_height - B_height) // 2


    # 将图片B粘贴到黑色背景图片的中心位置
    background.paste(image_B, (B_left, B_top))

    # 返回重建后的原始图片A
    return background

# 图片路径
# 获取当前目录的绝对路径
current_directory = os.path.abspath('.')

dir_path = os.path.join(current_directory, 'embedded_crop')

B_path = os.path.join(dir_path, 'embedded_CROP_90.bmp')
C_path = os.path.join(dir_path, 'embedded_CROP_82.bmp')
D_path = os.path.join(dir_path, 'embedded_CROP_75.bmp')

B_crop_ratio = 0.9  
C_crop_ratio = 0.82 
D_crop_ratio = 0.75 

# 重建原始图片A
original_image_A90 = reconstruct_original_image(B_path, B_crop_ratio)
original_image_A80 = reconstruct_original_image(C_path, C_crop_ratio)
original_image_A75 = reconstruct_original_image(D_path, D_crop_ratio)

# 保存重建后的图片A

dir_path = os.path.join(current_directory, 'embedded_crop')

original_image_A90.save(os.path.join(dir_path, 'restoration_90.bmp'))
original_image_A80.save(os.path.join(dir_path, 'restoration_82.bmp'))
original_image_A75.save(os.path.join(dir_path, 'restoration_75.bmp'))

bwm1 = WaterMark(password_img=1, password_wm=1)
wm_extract = bwm1.extract(os.path.join(current_directory, 'embedded_crop', 'restoration_90.bmp'), wm_shape=248, mode='str')
print("提取RESTORE90%信息：", wm_extract)

wm_extract = bwm1.extract(os.path.join(current_directory, 'embedded_crop', 'restoration_82.bmp'), wm_shape=248, mode='str')
print("提取RESTORE82%信息：", wm_extract)

wm_extract = bwm1.extract(os.path.join(current_directory, 'embedded_crop', 'restoration_75.bmp'), wm_shape=248, mode='str')
print("提取RESTORE75%信息：", wm_extract)

