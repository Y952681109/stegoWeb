import ctypes
import os
import sys 

lib = ctypes.CDLL("./stego/mp4/lib/libmp4stego.so")

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


if len(sys.argv) != 3:
    print("使用方法: python extract.py <stegoMp4_path> <outputTxt_path>")
    sys.exit(1)
    
    # 获取命令行参数
stegoMp4_path = sys.argv[1]
outputTxt_path = sys.argv[2]

# stego_mp4 = ctypes.c_char_p(b"./mp4/output_sample_2.mp4") #隐写mp4视频
# output_txt = ctypes.c_char_p(b"./output.txt") #提取文本信息

stego_mp4 = ctypes.c_char_p(stegoMp4_path.encode()) #隐写mp4视频
output_txt = ctypes.c_char_p(outputTxt_path.encode()) #提取文本信息

lib.extract_func(stego_mp4,output_txt)

# if os.path.exists(stegoMp4_path):
#     stego_mp4 = ctypes.c_char_p(stegoMp4_path.encode()) #隐写mp4视频
#     output_txt = ctypes.c_char_p(outputTxt_path.encode()) #提取文本信息
    
#     lib.extract_func(stego_mp4,output_txt)
# else:
#     print(f"文件 {stegoMp4_path} 不存在。")


