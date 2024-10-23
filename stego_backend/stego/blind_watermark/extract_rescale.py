from PIL import Image  
  
def resize_image(input_image_path, output_image_path, size):  
    """  
    按比例缩放图像  
  
    参数:  
    input_image_path (str): 输入图像的路径  
    output_image_path (str): 输出图像的路径  
    size (tuple): (宽度, 高度) 的元组，新的图像尺寸  
  
    返回:  
    None  
    """  
    original_image = Image.open(input_image_path)  
    width, height = original_image.size  
    print(f"原始图像尺寸: {width} 宽 x {height} 高")  
  
    # 保持图像的比例  
    max_size = (size[0], size[1])  
    original_image.thumbnail(max_size)  
    original_image.save(output_image_path)  
  
    # 注意：thumbnail 方法会原地修改图像对象，并且如果新的尺寸大于原始尺寸，则不会进行任何操作  
    # 如果你需要确保图像被缩放到指定的大小（即使这意味着图像可能会失真），你应该使用 resize 方法  
  
    # 使用 resize 方法确保图像被缩放到指定的大小  
    resized_image = original_image.resize(size)  
    resized_image.save(output_image_path)  
  
# 使用示例  
resize_image('./embedded_rescale/embedded_RESC_75.bmp', './embedded_rescale/output_embedded_RESC_75.bmp', (512, 512))
resize_image('./embedded_rescale/embedded_RESC_90.bmp', './embedded_rescale/output_embedded_RESC_90.bmp', (512, 512))
resize_image('./embedded_rescale/embedded_RESC_110.bmp', './embedded_rescale/output_embedded_RESC_110.bmp', (512, 512))
resize_image('./embedded_rescale/embedded_RESC_125.bmp', './embedded_rescale/output_embedded_RESC_125.bmp', (512, 512))

from blind_watermark.blind_watermark import WaterMark
import os
# 获取当前目录的绝对路径
current_directory = os.path.abspath('.')


bwm1 = WaterMark(password_img=1, password_wm=1)

wm_extract = bwm1.extract(os.path.join(current_directory, 'embedded_rescale', 'output_embedded_RESC_75.bmp'), wm_shape=248, mode='str')
print("提取rescale75°的信息：", wm_extract)

wm_extract = bwm1.extract(os.path.join(current_directory, 'embedded_rescale', 'output_embedded_RESC_90.bmp'), wm_shape=248, mode='str')
print("提取rescale90°的信息：", wm_extract)

wm_extract = bwm1.extract(os.path.join(current_directory, 'embedded_rescale', 'output_embedded_RESC_110.bmp'), wm_shape=248, mode='str')
print("提取rescale110°的信息：", wm_extract)

wm_extract = bwm1.extract(os.path.join(current_directory, 'embedded_rescale', 'output_embedded_RESC_125.bmp'), wm_shape=248, mode='str')
print("提取rescale125°的信息：", wm_extract)