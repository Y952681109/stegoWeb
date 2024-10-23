import os
import sys
import wave
import numpy as np
import soundfile
import torch
import wavmark
import librosa
import resampy
import argparse
from wavmark.utils import *

def extraWav(filename = "output1.wav",output_name="extra_from_output2", split_length = 1):
    # 1.load model
    device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')

    path_join = "stego/wav_deeplearning/src/"

    model = wavmark.load_model(path_join + "step59000_snr39.99_pesq4.35_BERP_none0.30_mean1.81_std1.81.model.pkl").to(device)

    # # 2. take 16,000 samples
    # filename = "output1.wav"
    # split_length = 1 # 分段时长：1s

    # 读取音频文件，转换为单通道16kHz
    data, sr = librosa.load(filename, sr=16000, mono=True)

    # 计算每个分割文件的样本数
    samples_per_split = split_length*sr

    i=0
    start = 0
    # 分割音频数据并保存
    # for start in range(0, len(data), samples_per_split):
    while start < len(data):
        if len(data[start:])<samples_per_split :
            print("提取完毕，有部分不足1s，没有隐写")
            break
        else:
            end = start + samples_per_split
            ori_signal = data[start:end]
            
            # 4.do decode:
            with torch.no_grad():
                signal = torch.Tensor(ori_signal).to(device).unsqueeze(0)
                message_decoded_npy = (model.decode(signal) >= 0.5).int().detach().cpu().numpy().squeeze()

            print(f"decoce message:{message_decoded_npy}")
            if i==0:
                output_npy=message_decoded_npy
            else:
                output_npy = np.concatenate([output_npy, message_decoded_npy])
            
            # print(f"decoce message:{message_decoded_npy}")
            flagArr = np.array([0,0,1,0,0,0,1,1,0,0,1,0,0,0,1,1,0,0,1,0,0,0,1,1,0,0,1,0,0,0,1,1])
            # if np.all(message_decoded_npy[-8:] == [0,0,1,0,0,0,1,1]):
            if np.array_equal(message_decoded_npy, flagArr):
                print("遇到#标记，达到结尾，退出迭代")
                break
            i+=1
            start = end
    # 检查末尾8位是否为#
    while np.all(output_npy[-8:] == [0,0,1,0,0,0,1,1]):
        # 如果是，则删除这最后8位
        output_npy = output_npy[:-8]
    
    
    if len(output_npy)%8!=0:
        print("长度不为8的整数倍，说明存在错误，或者遭到攻击")
        exit(0)
    # 将每8位转换为一个字节
    byte_arr = np.packbits(output_npy)
    byte_data =  byte_arr.tobytes()
    # print(byte_data[-3:].decode('utf-8'))
    file_type = byte_data[:3].decode('utf-8')
    if file_type == 'jpe':
        file_type = 'jpeg'
        byte_data = byte_data[4:]
    elif file_type in ['txt','png','bmp','jpg','wav']:
        byte_data = byte_data[3:]
    else:
        print(f"{file_type}文件类型不在设置的秘密文件类型中")
        exit(0)
    
    output_file = output_name+'.' + file_type
    # output_file = output_name
    # 转换并写入文件
    with open(output_file, 'wb') as f:
        f.write(byte_data)
            


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


if __name__ =="__main__":

    # if len(sys.argv) != 4:
    #     print("使用方法: python extract.py <filename> <split_length> <output_name>")
    #     sys.exit(1)
        
    #     # 获取命令行参数
    # filename = sys.argv[1]
    # split_length = sys.argv[2]
    # output_name = sys.argv[3]

    # try:
    #     int_value = int(split_length)
        
    #     result1 = check_file_and_format(filename, "wav")
    #     if result1:

    #         try:
    #             extraWav(filename, output_name, int_value)

    #         except RuntimeError:
    #             print("split_length分割长度与嵌入不符")


    #     else:
    #         print(filename + "文件路径或格式不正确，应为wav格式文件")
    #         sys.exit(1)



    # except ValueError:
    #     print("split_length不是一个有效的整数")

    if len(sys.argv) != 3:
        print("使用方法: python extract.py <filename> <output_name>")
        sys.exit(1)
        
        # 获取命令行参数
    filename = sys.argv[1]
    output_name = sys.argv[2]


    result1 = check_file_and_format(filename, "wav")
    if result1:

        extraWav(filename, output_name, 1)


    else:
        print(filename + "文件路径或格式不正确，应为wav格式文件")
        sys.exit(1)
        



    # filename = "output_music.wav"
    # split_length = 1 # 分段时长：1s
    # output_name="extra_from_music"
    # extraWav(filename, output_name, split_length)
    




