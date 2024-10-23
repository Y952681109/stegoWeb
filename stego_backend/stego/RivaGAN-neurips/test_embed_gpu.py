import os
import sys
import torch
import Embed_gpu
from Extract_gpu import Is_Mark


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


# 检查是否提供了两个命令行参数
if len(sys.argv) != 4:
    print("使用方法: python test.py <ori_path> <data_path> <end_path>")
    sys.exit(1)

# 获取命令行参数
ori_path = sys.argv[1]
data_path = sys.argv[2]
end_path = sys.argv[3]


result1 = check_file_and_format(ori_path, "avi")
if result1:
    result2 = check_file_and_format(data_path, "txt")
    if result2:
        result3 = check_format(end_path, "avi")
        if result3:
            # 读取当前目录下data.txt文件中的数据
            try:
                with open(data_path, 'r', encoding='utf-8') as file:
                    data = file.read()
            except Exception as e:
                print(f"打开文件出错: {e}")
                sys.exit(1)

            if len(data) > 2 and len(data)<=4:
                if data.isalpha():
                    Embed_gpu.Embed_API(dir, data, ori_path, end_path)
                else:
                    print("嵌入文本应均为字母")
            else:
                print("嵌入文本应为3-4字符")
    
        else:
            print(end_path + "文件路径或格式不正确，应为avi格式文件")
            sys.exit(1)
    
    else:
        print(data_path + "文件路径或格式不正确，应为txt格式文件")
        sys.exit(1)

else:
    print(ori_path + "文件路径或格式不正确，应为avi格式文件")
    sys.exit(1)








