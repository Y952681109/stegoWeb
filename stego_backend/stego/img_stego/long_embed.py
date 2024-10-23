from embed_img import embed_and_evaluate
from extract_img import extract_img
from PIL import Image
import os
import sys
from code_secret import encode_secret

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
    print("原始文件名列表:", filenames)
    
    # 使用列表推导式过滤出格式正确的文件名
    # 只保留能够成功分割出三个部分的文件名
    filenames = [
        filename for filename in filenames
        if "_" in filename and len(filename.split("_")) > 2
    ]
    print("过滤后的文件名列表:", filenames)
    
    # 重新计算水平和垂直方向上的合并数量
    num_horizontal = len(set(filename.split("_")[2] for filename in filenames))
    num_vertical = len(set(filename.split("_")[1] for filename in filenames))

    # 下面是合并图像的其他逻辑...
    # ...

# 调用函数的示例
# merge_images('path_to_input_folder', 'path_to_output_image')

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


secret_to_encode = "hello this is 1a秘密信息, 这是一个长文本测试"
secret_to_encode = encode_secret(secret_to_encode)

# 读取图片进行分割
input_image_path = "examples/wallhave2.jpg"
split_images_path = "examples/split/split_images"
secret_images_path = "examples/split/secret_image"
if not os.path.exists(secret_images_path):
    os.makedirs(secret_images_path)
split_size = 256
split_images = split_image(input_image_path, split_images_path, split_size)

# 获取"split_images"文件夹中的所有图像文件路径
image_files_org = [f for f in os.listdir(split_images_path) if os.path.isfile(os.path.join(split_images_path, f))]
image_files = sorted(image_files_org, key=extract_indices)

# 将秘密信息按七个字符分段
split_fragments = [secret_to_encode[i:i+7] for i in range(0, len(secret_to_encode), 7)]
total_fragments = len(split_fragments)
i = 0
# 最多嵌入数目
max_len = (len(image_files)-1)*7
print(f"嵌入长度为 {len(secret_to_encode)},最多嵌入字符数为 {max_len}。")
if len(image_files) * 7 < len(secret_to_encode):
    print(f"秘密信息长度为 {len(secret_to_encode)}，最多嵌入字符数为 {max_len}。")
    sys.exit()


# 用第一个小块来存放含有秘密信息小块的个数
# 判断：如果是第一个图片，就嵌入total_fragments，i不++；ifnot就嵌入秘密信息，i++



# 循环处理每个图象
for image_file in image_files:
    image_path = os.path.join(split_images_path, image_file)
    output_path = os.path.join(secret_images_path, image_file)
    print("载体图像路径为：")
    # cover
    print(image_path)

    # 如果是第一张图片，就嵌入需要的小块数目
    if(image_file == "tile_0_0.jpg"):
        this_secret = str(total_fragments)
        print(f'第一张图片嵌入的内容为：{this_secret}')
        embed_and_evaluate(this_secret, image_path, output_path)

        #验证第一个小块嵌入和提取的是否一样
        first_secret = extract_img(output_path)
        secret_num = first_secret[0]
        # print(f'提取的第一个小块内容为：{first_secret}')
        # print(f'嵌入的第一个小块的长度为：{len(first_secret)}')
        if secret_num != this_secret:
            print("无法保证100%准确率，请更换载体图像进行尝试。")
            sys.exit()

    else:
        if i < total_fragments:
            this_secret = split_fragments[i]
            i = i + 1
            embed_and_evaluate(this_secret, image_path, output_path)
        else:
            with open(image_path, 'rb') as source_file:
                # 读取原始文件内容
                file_content = source_file.read()

                # 打开目标文件以供写入
                with open(output_path, 'wb') as destination_file:
                    # 将原始文件内容写入目标文件
                    destination_file.write(file_content)

                    
# 合并小图像
merged_image_path = "merged_image.jpg"
merge_images(secret_images_path, merged_image_path)



