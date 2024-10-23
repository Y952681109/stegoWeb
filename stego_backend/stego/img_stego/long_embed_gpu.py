from embed_img_gpu import embed_and_evaluate
from extract_img_gpu import extract_img
from PIL import Image
import os
import sys
from code_secret import encode_secret
import shutil  
import time  
from datetime import datetime  

def split_image(image_path, output_folder, size):
    image = Image.open(image_path).convert('RGB')
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

def merge_images(input_folder, output_path):
    # 获取所有小图像的文件名
    filenames = sorted(os.listdir(input_folder))

    # 计算水平和垂直方向上的合并数量
    num_horizontal = len(set([filename.split("_")[2] for filename in filenames]))
    num_vertical = len(set([filename.split("_")[1] for filename in filenames]))

    # 计算合并后的图像的宽度和高度
    width = num_horizontal * 256
    height = num_vertical * 256

    # 创建一个新的图像对象
    merged_image = Image.new("RGB", (width, height))

    # 遍历每个小图像的文件名
    for filename in filenames:
        # 解析小图像的坐标
        # i, j = [int(index) for index in filename.split("_")[1:3]]

        parts = filename.split("_")
        i = int(parts[1])  # 获取第一个零
        j = int(parts[2].split(".")[0])  # 获取第二个零，去除扩展名部分

        # 计算当前小图像在合并图像中的位置
        left = j * 256
        upper = i * 256
        right = left + 256
        lower = upper + 256

        # 打开当前小图像
        tile_path = os.path.join(input_folder, filename)
        tile = Image.open(tile_path)

        # 将当前小图像粘贴到合并图像中的对应位置
        merged_image.paste(tile, (left, upper, right, lower))

    # 保存合并后的图像
    merged_image.save(output_path)

def extract_indices(filename):
    parts = filename.split("_")
    i, j = int(parts[1]), int(parts[2][:-4])  # 去除扩展名 ".jpg"
    return i, j

def embed_long_words(secret_to_encode,input_image_path,output_image_path):
    secret_to_encode = encode_secret(secret_to_encode)

    # 读取图片进行分割
    # 获取当前时间的时间戳  
    timestamp = time.time()  
    # 将时间戳转换为datetime对象  
    dt_object = datetime.fromtimestamp(timestamp)  
    # 将datetime对象格式化为一个字符串，例如 "YYYY-MM-DD_HH-MM-SS"  
    formatted_time = dt_object.strftime("%Y-%m-%d_%H-%M-%S")  

    split_images_path = "examples/split/split_images"
    secret_images_path = "examples/split/secret_image"
    split_images_path = os.path.join(split_images_path, formatted_time)
    secret_images_path = os.path.join(secret_images_path, formatted_time)

    if not os.path.exists(secret_images_path):
        os.makedirs(secret_images_path)
    split_size = 256
    split_image(input_image_path, split_images_path, split_size)

    # 获取"split_images"文件夹中的所有图像文件路径
    image_files_org = [f for f in os.listdir(split_images_path) if os.path.isfile(os.path.join(split_images_path, f))]
    image_files = sorted(image_files_org, key=extract_indices)

    # 将秘密信息按七个字符分段
    split_fragments = [secret_to_encode[i:i+7] for i in range(0, len(secret_to_encode), 7)]
    total_fragments = len(split_fragments)
    i = 0
    # 最多嵌入数目
    # 块数没超过56，最大嵌入数目就是块数*7，如果超过56小块，就嵌前56小块
    max_len = (len(image_files)-1)*7
    max_len = min(max_len,56*7)
    print(f"嵌入长度为 {len(secret_to_encode)},最多嵌入字符数为 {max_len}。")

    if max_len < len(secret_to_encode):
        print(f"秘密信息长度为 {len(secret_to_encode)}，最多嵌入字符数为 {max_len}。")
        sys.exit()


    # 记录第一个小块的路径，先嵌后面的小块，如果能嵌就给字符串拼接1，不能嵌就拼接0，最后将01比特流转为字符串嵌入到第一个小块中
    # 嵌入第一个小块后提取，如果不一致，就需要换图片
    # 提取时提取第一个小块内容转为01比特流，跟图片一块遍历，遍历一个图片字符往后移一位，如果当前为是0就不提取，如果是1就提取

    bit_site = ""
    # 循环处理每个图象
    for image_file in image_files:
        image_path = os.path.join(split_images_path, image_file)
        output_path = os.path.join(secret_images_path, image_file)

        # 第一张图片记录一下单独处理
        if(image_file == "tile_0_0.jpg"):
            first_input_path = image_path
            first_output_path = output_path

        else:
            if i < total_fragments:
                this_secret = split_fragments[i]
                embed_and_evaluate(this_secret, image_path, output_path)
                now_secret = extract_img(output_path)
                # 最后一段秘密信息要去掉右边的空格再比较
                if(i==total_fragments-1):
                    this_secret = this_secret.rstrip()
                    now_secret = now_secret.rstrip()
                if(now_secret == this_secret):
                    bit_site += "1"
                    i = i + 1
                    # print("载体图像路径为：")
                    # # cover
                    # print(image_path)
                else:
                    bit_site += "0"
                    shutil.copy2(image_path, output_path)
            else:
                shutil.copy2(image_path, output_path)

    if i < total_fragments:
        print("信息未能完全嵌入，请更换载体图像重试")
        sys.exit()

    # 处理第一个小块的嵌入内容
    # 需要将字符串补足8的倍数
    padding_length = (8 - (len(bit_site) % 8)) % 8  
    bit_site = bit_site + '0' * padding_length 
    split_strings = [bit_site[i:i+8] for i in range(0, len(bit_site), 8)]
    # 将每个 8 位字符串转换为字符
    char_list = [chr(int(bit, 2)) for bit in split_strings]
    first_secret = ''.join(char_list)

    embed_and_evaluate(first_secret, first_input_path, first_output_path)
    extract_first_secret = extract_img(first_output_path)
    extract_first_secret = extract_first_secret.rstrip()
    # print(len(extract_first_secret))
    if first_secret != extract_first_secret:
        print("无法保证100%准确率，请更换载体图像进行尝试。")
        sys.exit()

    # 合并小图像
    merge_images(secret_images_path, output_image_path)
    print(f'嵌入完成，图像保存在{output_image_path}')



if len(sys.argv) != 4:
    print("使用方法: python long_embed_test.py <coverJPG_path> <inputTxt_path> <stegoJPG_path>")
    sys.exit(1)
    
    # 获取命令行参数
coverJPG_path = sys.argv[1]
inputTxt_path = sys.argv[2]
stegoJPG_path = sys.argv[3]

try:
    with open(inputTxt_path, 'r', encoding='utf-8') as file:
        data = file.read()
except Exception as e:
    print(f"打开文件出错: {e}")
    sys.exit(1)




secret_to_encode = data
input_image_path = coverJPG_path
output_image_path = stegoJPG_path
embed_long_words(secret_to_encode, input_image_path, output_image_path)
