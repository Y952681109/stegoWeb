import os
import sys
import torch
import Embed
from Extract import Is_Mark

dir = ''

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


# 检查是否提供了两个命令行参数
if len(sys.argv) != 3:
    print("使用方法: python test_extract.py <movie_path> <outputTxt_path>")
    sys.exit(1)

# 获取命令行参数
movie_path = sys.argv[1]
outputTxt_path = sys.argv[2]

result1 = check_file_and_format(movie_path, "avi")
if result1:
    res = Is_Mark(dir, movie_path)

    with open(outputTxt_path, 'w', encoding='utf-8') as file:
        file.write(res)
else:
    print(movie_path + "文件路径或格式不正确，应为avi格式文件")
    sys.exit(1)




