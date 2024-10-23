
import os


def find_recordType(num):
    # 定义一个字典，将数字映射到中文汉字
    recordType_dict = {
        1: 'jpgDL嵌入',
        2: 'jpgDL解析',
        3: 'txtDL嵌入',
        4: 'txtDL解析',
        5: 'wavDL嵌入',
        6: 'wavDL解析',
        7: 'aviDL嵌入',
        8: 'aviDL解析',
        9: 'wav嵌入',
        10: 'wav解析',
        11: 'wma嵌入',
        12: 'wma解析',
        13: 'mid嵌入',
        14: 'mid解析',
        15: 'mp4嵌入',
        16: 'mp4解析',
        17: 'bmp嵌入',
        18: 'bmp解析'
    }
    
    # 检查数字是否在字典的键中
    if num in recordType_dict:
        return recordType_dict[num]
    else:
        return "未知任务类型"


def find_recordRes(num):
    # 定义一个字典，将数字映射到中文汉字
    recordType_dict = {
        0: '失败',
        1: '成功',
    }
    
    # 检查数字是否在字典的键中
    if num in recordType_dict:
        return recordType_dict[num]
    else:
        return "未知任务结果"


def find_recordOperation(num):
    # 定义一个字典，将数字映射到中文汉字
    recordType_dict = {
        0: '',
        1: 'download',
    }
    
    # 检查数字是否在字典的键中
    if num in recordType_dict:
        return recordType_dict[num]
    else:
        return "数字必须在0到1之间"


def find_file_with_extension(directory, filename_without_extension):
    """
    在指定目录中查找具有给定文件名（不含后缀）的文件，并返回其完整路径。
    
    :param directory: 文件所在目录
    :param filename_without_extension: 不含后缀的文件名
    :return: 带后缀的文件完整路径，如果未找到则返回None
    """
    # 遍历目录中的所有文件
    for root, dirs, files in os.walk(directory):
        for file in files:
            # 检查文件名是否匹配（不包括后缀）
            if file.startswith(filename_without_extension):
                # 返回匹配的文件完整路径
                return os.path.join(root, file)
    # 如果没有找到文件，返回None
    return None

