from extract_img import extract_img
from PIL import Image
import os
from code_secret import decode_secret
import time  
from datetime import datetime  

def extract_indices(filename):
    parts = filename.split("_")
    i, j = int(parts[1]), int(parts[2][:-4])  # 去除扩展名 ".jpg"
    return i, j

def split_image(image_path, output_folder, size):
    image = Image.open(image_path)
    # 获取原图的宽度和高度
    width, height = image.size
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 计算水平和垂直方向上的分割数量
    num_horizontal = width // size
    num_vertical = height // size

    # 遍历每个小图像的起始位置
    for i in range(num_vertical):
        for j in range(num_horizontal):
            # 计算当前小图像的坐标范围
            left = j * size
            upper = i * size
            right = left + size
            lower = upper + size

            # 裁剪出当前小图像
            tile = image.crop((left, upper, right, lower))

            # 生成保存路径和文件名
            filename = f"tile_{i}_{j}.jpg"
            output_path = os.path.join(output_folder, filename)

            # 保存当前小图像
            tile.save(output_path)


def extract_long_words(input_image_path):
    # 读取图片进行分割
    # 获取当前时间的时间戳  
    timestamp = time.time()  
    # 将时间戳转换为datetime对象  
    dt_object = datetime.fromtimestamp(timestamp)  
    # 将datetime对象格式化为一个字符串，例如 "YYYY-MM-DD_HH-MM-SS"  
    formatted_time = dt_object.strftime("%Y-%m-%d_%H-%M-%S")  
    output_folder = "examples/split/split_secret"
    output_folder = os.path.join(output_folder, formatted_time)
    
    split_size = 256
    split_image(input_image_path, output_folder, split_size)
    # 获取"split_secret"文件夹中的所有图像文件路径
    image_files_org = [f for f in os.listdir(output_folder) if os.path.isfile(os.path.join(output_folder, f))]
    image_files = sorted(image_files_org, key=extract_indices)
    # print(image_files)

    # 提取时提取第一个小块内容转为01比特流，跟图片一块遍历，遍历一个图片字符往后移一位，如果当前为是0就不提取，如果是1就提取

    recovered_secrets = []
    i = 0
    # 循环处理每张图像
    for image_file in image_files:
        # 构建图像文件路径
        image_path = os.path.join(output_folder, image_file)
        # print("图像路径为：")
        # print(image_path)

        # decode secret
        # print('Extracting secret...')
        if(image_file == "tile_0_0.jpg"):
            secret_decoded = extract_img(image_path)
            # 将字符串转为二进制串
            secret_decoded = secret_decoded.rstrip()
            binary_string = ''.join(format(ord(c), '08b') for c in secret_decoded)

        else:
            if(binary_string[i] == '1'):
                secret_decoded = extract_img(image_path)
                print(f'Recovered secret: {secret_decoded}')
                recovered_secrets.append(secret_decoded)
            i=i+1
            if(i==len(binary_string)):
                break
                



    # print("Recovered secrets:")
    # for i, secret in enumerate(recovered_secrets):
    #     print(f"Image {i+1}: {secret}")

    # 将列表中的秘密信息合成一个字符串
    all_recovered_secrets = "".join(recovered_secrets)
    all_recovered_secrets = all_recovered_secrets.rstrip()
    # 中英文编码统一
    all_recovered_secrets = decode_secret(all_recovered_secrets)
    # print("decode secrets:")
    # print(all_recovered_secrets)
    return all_recovered_secrets



input_image_path = "long_embed_image.jpg"
secret = extract_long_words(input_image_path)
print("decode secrets:")
print(secret)
