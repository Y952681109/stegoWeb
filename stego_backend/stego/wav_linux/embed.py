import ctypes
import os
import sys

# 确定动态链接库的路径
lib = ctypes.CDLL("./stego/wav_linux/libaudio.so")
decrypt_func = ctypes.c_char_p(b"sm4")
key = ctypes.c_char_p(b"1234567890123456")
cover_type = ctypes.c_char_p(b"audio")


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


#embed(char* stega_name, char* cover_path, char* secret_path, char* output_path, char* encrypt_func, char* key);
#stega_name: 嵌入—提取算法名称
#cover_path: 载体路径
#secret_path: 秘密信息路径
#output_path: 输出载秘文件路径
#encrypt_func: 加密方法
#key: 秘钥

# cover_path = ctypes.c_char_p(b"input.wav")
# secret_path = ctypes.c_char_p(b"secret.txt")
# output_path = ctypes.c_char_p(b"output.wav")

if len(sys.argv) != 4:
    print("使用方法: python embed.py <cover_path> <secret_path> <output_path>")
    sys.exit(1)
    
    # 获取命令行参数
cover_path = sys.argv[1]
secret_path = sys.argv[2]
output_path = sys.argv[3]


result1 = check_file_and_format(cover_path, "wav")
if result1:
    result3 = check_format(output_path, "wav")
    if result3:

        cover_path = ctypes.c_char_p(cover_path.encode('utf-8'))
        secret_path = ctypes.c_char_p(secret_path.encode('utf-8'))
        output_path = ctypes.c_char_p(output_path.encode('utf-8'))

        lib.embed(cover_type,cover_path, secret_path,output_path,decrypt_func,key)


    else:
        print(output_path + "文件路径或格式不正确，应为wav格式文件")
        sys.exit(1)


else:
    print(cover_path + "文件路径或格式不正确，应为wav格式文件")
    sys.exit(1)




