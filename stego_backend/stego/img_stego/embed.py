import os
import re
import sys
from embed_img import embed_and_evaluate
from extract_img import extract_img


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


if len(sys.argv) != 4:
    print("使用方法: python embed.py <coverJPG_path> <inputTxt_path> <stegoJPG_path>")
    sys.exit(1)
    
    # 获取命令行参数
coverJPG_path = sys.argv[1]
inputTxt_path = sys.argv[2]
stegoJPG_path = sys.argv[3]

result1 = check_file_and_format(coverJPG_path, "jpg")
if result1:
    result2 = check_file_and_format(inputTxt_path, "txt")
    if result2:
        result3 = check_format(stegoJPG_path, "jpg")
        if result3:
            try:
                # 打开文件
                with open(inputTxt_path, 'r', encoding='utf-8') as file:
                    # 读取文件内容
                    content = file.read()
                    
                    embed_and_evaluate(content, coverJPG_path, stegoJPG_path)


            except FileNotFoundError:
                print(f"错误：文件 {inputTxt_path} 未找到。")
                sys.exit(1)
            except Exception as e:
                print(f"读取文件时发生错误：{e}")
                sys.exit(1)


        else:
            print(stegoJPG_path + "文件路径或格式不正确，应为jpg格式文件")
            sys.exit(1)


    else:
        print(inputTxt_path + "文件路径或格式不正确，应为txt格式文件")
        sys.exit(1)


else:
    print(coverJPG_path + "文件路径或格式不正确，应为jpg格式文件")
    sys.exit(1)

# # 嵌入
# secret = 'Test23A'
# cover = 'input.jpg'
# output = 'steg.jpg'
# embed_and_evaluate(secret, cover, output)