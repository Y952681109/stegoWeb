import os
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

if len(sys.argv) != 3:
    print("使用方法: python extract.py <stegoJPG_path> <extractTXT_path>")
    sys.exit(1)
    
    # 获取命令行参数
stegoJPG_path = sys.argv[1]
extractTXT_path = sys.argv[2]


result1 = check_file_and_format(stegoJPG_path, "jpg")
if result1:
    result2 = check_format(extractTXT_path, "txt")
    if result2:
        img_secret = extract_img(stegoJPG_path)
        try:
            # 打开文件，如果文件已存在则覆盖，不存在则创建
            with open(extractTXT_path, 'w', encoding='utf-8') as file:
                # 写入字符串内容
                file.write(img_secret)
        except Exception as e:
            print(f"保存文件时发生错误：{e}")
            sys.exit(1)


    else:
        print(extractTXT_path + "文件路径或格式不正确，应为txt格式文件")
        sys.exit(1)


else:
    print(stegoJPG_path + "文件路径或格式不正确，应为jpg格式文件")
    sys.exit(1)


# # 提取
# container_img = 'output.jpg'
# img_secret = extract_img(container_img)
# print(img_secret)

