import os
from PIL import Image
import csv
from embed_img import embed_and_evaluate
from extract_img import extract_img
from test_tools import calculate_accuracy,generate_random_string

os.environ["CUDA_VISIBLE_DEVICES"] = "1"

# 定义文件夹路径和秘密信息
folder_path = 'examples/images'
# secret = 'testsec'
output_folder = 'examples/stego_images'
csv_file = 'image_psnr_accuracy_report.csv'

# 确保输出文件夹存在
os.makedirs(output_folder, exist_ok=True)

# 初始化总和和计数器
total_psnr = 0
total_accuracy = 0
count = 0

# 准备CSV文件记录数据
with open(csv_file, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Image Name', 'PSNR', 'Accuracy', 'secret', 'ex-secret'])

    # 遍历文件夹中的每个文件
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):  # 检查文件格式
            image_path = os.path.join(folder_path, filename)
            output_image_path = os.path.join(output_folder, filename)

            # 生成随机秘密信息
            secret = generate_random_string(7)

            # 嵌入信息并计算PSNR
            psnr = embed_and_evaluate(secret, image_path, output_image_path)
            # print(type(psnr))
            # print(psnr.shape)
            # print(psnr)

            # 提取信息并计算准确率
            extracted = extract_img(output_image_path)
            accuracy = calculate_accuracy(secret, extracted)

            # 累加PSNR和准确率
            total_psnr += psnr[0]
            total_accuracy += accuracy
            count += 1

            # 将数据写入CSV文件
            writer.writerow([filename, psnr, accuracy,secret,extracted])

# 计算平均PSNR和准确率
average_psnr = total_psnr / count if count > 0 else 0
average_accuracy = total_accuracy / count if count > 0 else 0

print(f"处理完成，所有数据已记录到 {csv_file}")
print(f"Average PSNR: {average_psnr}")
print(f"Average Accuracy: {average_accuracy}")
