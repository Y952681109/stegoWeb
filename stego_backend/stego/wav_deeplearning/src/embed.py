import sys
import wave
import os
import numpy as np
import soundfile
import torch
import wavmark
import librosa
import resampy
import argparse
from wavmark.utils import *

def embedWav(filename = "example.wav", secret_path = "1.txt",split_length = 1, outputFile="output1.wav"):
    # 1.load model
    device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')

    path_join = "stego/wav_deeplearning/src/"

    model = wavmark.load_model(path_join + "step59000_snr39.99_pesq4.35_BERP_none0.30_mean1.81_std1.81.model.pkl").to(device)

    # secret_path = "1.txt"
    if '.' in secret_path:
        file_type = secret_path.split('.')[-1]
    else:
        print(f"{secret_path}没有扩展名")
        exit(0)
    extension_bits = ''.join(format(ord(char), '08b') for char in file_type)
    if file_type not in ['txt','png','bmp','jpg','jpeg','wav']:
        print(f"类型{file_type}不支持")
        exit(0)
    
    # 读取音频文件，转换为单通道16kHz
    data, sr = librosa.load(filename, sr=16000, mono=True)
    # 计算每个分割文件的样本数
    samples_per_split = split_length*sr
    capacity = len(data)//samples_per_split
    
    # 以二进制模式读取文件内容
    with open(secret_path, "rb") as file:
        file_content = file.read()
    # 将文件内容转换为二进制字符串
    bit_string = ''.join(format(byte, '08b') for byte in file_content)
    # 将文件扩展名追加到文件末尾
    bit_string = extension_bits + bit_string
    # 计算需要填充的零的数量以使长度成为32的倍数
    padding_length = ((32 - len(bit_string) % 32) % 32)//8
    # 添加填充# 23
    # if padding_length ==0:
    #     padded_bit_string = bit_string+'00100011001000110010001100100011'
    # else:
    padded_bit_string = bit_string + '00100011'*padding_length
    padded_bit_string = padded_bit_string+'00100011001000110010001100100011'
    
    lenSecret = len(padded_bit_string)//32
    # print(f"padded :{len(padded_bit_string)//32}")
    if capacity < lenSecret:
        print(f"超出载体容量，至少需要{lenSecret*split_length}s的wav音频")
        exit(0)
    # # 如果当前容量大于秘密信息长度，填充4个#作为结束标记
    # if lenSecret < capacity:
    #     lenSecret +=1
    #     padded_bit_string = padded_bit_string+'00100011001000110010001100100011'
    
    # 将填充后的二进制字符串转换为NumPy数组
    bit_array = np.array([int(bit) for bit in padded_bit_string], dtype=np.uint8)
    
    # 重新调整数组形状，确保每32位一组（如果需要）
    # 注意：这一步可能不是必需的，取决于你如何使用这个数组
    # 如果你需要按32位（4字节）操作或处理数组，可以考虑保留这一步
    # 如果不需要特定的形状，可以注释掉下面这行代码
    bit_array = bit_array.reshape(-1, 32)
    # print(bit_array.shape[0])
    # print(bit_array)
    # exit(0)

    # # 2. take 16,000 samples
    # filename = "example.wav"
    # split_length = 1 # 分段时长：1s

    
    
    # print(f"capacity:{capacity}")
    # exit(0)
    
    # lenSecret = bit_array.shape[0]
    # if capacity < lenSecret:
    #     print(f"超出载体容量，至少需要{lenSecret*split_length}s的wav音频")
    #     exit(0)


    # 分割音频数据并保存
    # for start in range(0, len(data), samples_per_split):
    start = 0
    i=0
    while i<lenSecret:
        # print(f"{i}")
        end = start + samples_per_split
        ori_signal = data[start:end]
        # split_filename = f"{filename[:-4]}_part{start//samples_per_split}.wav"
        
        # # 保存分割后的文件
        # sf.write(split_filename, split_audio, sr)
        trunck = ori_signal[0:16000]
        
        # message_npy = np.random.choice([0, 1], size=32)
        message_npy = bit_array[i]
        print(f"origin message:{message_npy}")
        
        # 3. do encode:
        with torch.no_grad():
            signal = torch.Tensor(trunck).to(device)[None]
            message_tensor = torch.Tensor(message_npy).to(device)[None]
            signal_wmd_tensor = model.encode(signal, message_tensor)
            signal_wmd_npy = signal_wmd_tensor.detach().cpu().numpy().squeeze()
        if start==0:
            output_data = signal_wmd_npy
        else:
            output_data = np.concatenate([output_data, signal_wmd_npy])
        start = end
        i+=1
    output_data = np.concatenate([output_data, data[start:]])
    soundfile.write(outputFile, output_data, 16000)



# # # signal, sample_rate = soundfile.read("example.wav")
# # # print(f"sample_rate:{sample_rate}")
# # signal = file_reader.read_as_single_channel('example_part0.wav', aim_sr=16000)
# # trunck = signal[0:16000]
# trunck = data[0:16000]

# message_npy = np.random.choice([0, 1], size=32)
# print(f"origin message:{message_npy}")
# # 3. do encode:
# with torch.no_grad():
#     signal = torch.FloatTensor(trunck).to(device)[None]
#     message_tensor = torch.FloatTensor(message_npy).to(device)[None]
#     signal_wmd_tensor = model.encode(signal, message_tensor)
#     signal_wmd_npy = signal_wmd_tensor.detach().cpu().numpy().squeeze()
# soundfile.write("output1.wav", signal_wmd_npy, 16000)

# # # 4.do decode:
# # with torch.no_grad():
# #     signal = torch.FloatTensor(signal_wmd_npy).to(device).unsqueeze(0)
# #     message_decoded_npy = (model.decode(signal) >= 0.5).int().detach().cpu().numpy().squeeze()

# # print(f"decoce message:{message_decoded_npy}")
# # BER = (message_npy != message_decoded_npy).mean() * 100
# # print("BER:", BER)

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

    if len(sys.argv) != 4:
        print("使用方法: python embed.py <filename> <secret_path> <outputFile>")
        sys.exit(1)
        
        # 获取命令行参数
    filename = sys.argv[1]
    secret_path = sys.argv[2]
    split_length = 1
    outputFile = sys.argv[3]

    try:
        int_value = int(split_length)
        
        result1 = check_file_and_format(filename, "wav")
        if result1:
            result2 = check_file_and_format(secret_path, "txt")
            if result2:
                result3 = check_format(outputFile, "wav")
                if result3:
                    embedWav(filename, secret_path, int_value, outputFile)

                else:
                    print(outputFile + "文件路径或格式不正确，应为wav格式文件")
                    sys.exit(1)


            else:
                print(secret_path + "文件路径或格式不正确，应为txt格式文件")
                sys.exit(1)


        else:
            print(filename + "文件路径或格式不正确，应为wav格式文件")
            sys.exit(1)



    except ValueError:
        print("split_length不是一个有效的整数")






    # filename = "music.wav"
    # split_length = 1 # 1
    # outputFile="output_music.wav"
    # secret_path = "1.txt"
    # embedWav(filename, secret_path, split_length, outputFile)

    # parser = argparse.ArgumentParser(description="Embed file into a WAV file.")

    # parser.add_argument("-f","--filename",default="longmusic.wav",  help="The WAV file to embed file into.")
    # parser.add_argument("-s","--secret_path",default="1.txt", help="The path of the file to embed.")
    # parser.add_argument("-l","--split_length", type=int,default = 1, help="The split length for embedding.")
    # parser.add_argument("-o","--outputFile",default="output_music.wav", help="The output WAV file.")

    # args = parser.parse_args()
    # embedWav(args.filename, args.secret_path, args.split_length, args.outputFile)

# python embedWav.py -f longmusic.wav -s 1.txt -o output_music.wav
# python extraWav.py -f output_music.wav -o extra_music
