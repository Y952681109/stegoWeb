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

def check_file_length(file_path):
    try:
        # 打开文件并读取内容
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            # 计算字符数量
            char_count = len(content)
            
            # 判断字符数量是否小于8187
            if char_count < 8187:
                
                return True
            else:
                print(f"文件 '{file_path}' 的字符数量为 {char_count}，大于或等于8187个字符。")
                return False
    except FileNotFoundError:
        print(f"错误：文件 '{file_path}' 未找到。")
        return False
    except IOError:
        print(f"错误：读取文件 '{file_path}' 时发生IO错误。")
        return False
    except Exception as e:
        print(f"未知错误：{e}")
        return False


if len(sys.argv) != 4:
    print("使用方法: python embed.py <coverMp4_path> <inputTxt_path> <stegoMp4_path>")
    sys.exit(1)
    
    # 获取命令行参数
context_path = sys.argv[1]
embed_path = sys.argv[2]
extract_path = sys.argv[3]

# cover_mp4 = ctypes.c_char_p(b"mp4/sample_2.mp4") #载体mp4视频
# intput_txt = ctypes.c_char_p(b"input.txt") #待嵌入文本信息
# stego_mp4 = ctypes.c_char_p(b"mp4/output_sample_2.mp4") #隐写mp4视频


cover_mp4 = ctypes.c_char_p(context_path.encode()) #载体mp4视频
intput_txt = ctypes.c_char_p(embed_path.encode()) #待嵌入文本信息
stego_mp4 = ctypes.c_char_p(extract_path.encode()) #隐写mp4视频

lib.embed_secret(cover_mp4,intput_txt,stego_mp4)


# if os.path.exists(context_path):
#     if os.path.exists(embed_path):
#         # 调用 embed 函数
#         cover_mp4 = ctypes.c_char_p(context_path.encode()) #载体mp4视频
#         intput_txt = ctypes.c_char_p(embed_path.encode()) #待嵌入文本信息
#         stego_mp4 = ctypes.c_char_p(extract_path.encode()) #隐写mp4视频

#         lib.embed_secret(cover_mp4,intput_txt,stego_mp4)
#     else:
#         print(f"文件 {embed_path} 不存在。")
# else:
#     print(f"文件 {context_path} 不存在。")


