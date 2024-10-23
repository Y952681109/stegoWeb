import ctypes
import os
import sys

# from wma import embed_text_in_wma 

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


import wave
import numpy as np
import os
import subprocess


def em_audio(af, string, output):
    print("Please wait...")
    waveaudio = wave.open(af, mode='rb')
    frame_bytes = bytearray(list(waveaudio.readframes(waveaudio.getnframes())))
    string = string.encode('utf-8')  # Encode string to bytes using UTF-8
    string = string + (len(frame_bytes) - len(string) * 8 * 8) // 8 * b'#'
    bits = list(map(int, ''.join([bin(byte).lstrip('0b').rjust(8, '0') for byte in string])))
    for i, bit in enumerate(bits):
        frame_bytes[i] = (frame_bytes[i] & 254) | bit
    frame_modified = bytes(frame_bytes)
    with wave.open(output, 'wb') as fd:
        fd.setparams(waveaudio.getparams())
        fd.writeframes(frame_modified)
    waveaudio.close()
    print("File Has Been Saved...")


def ex_msg(af, output_file):
    print("Please wait...")
    with wave.open(af, mode='rb') as waveaudio:
        frame_bytes = bytearray(list(waveaudio.readframes(waveaudio.getnframes())))
        extracted = [frame_bytes[i] & 1 for i in range(len(frame_bytes))]
        string = "".join(chr(int("".join(map(str, extracted[i:i + 8])), 2)) for i in range(0, len(extracted), 8))
        string = string.split("###")[0]
        msg = string.encode('latin-1').decode('utf-8')

    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(msg)
    print("Your Secret Message is get out success")
    waveaudio.close()


def convert_wma_to_wav(input_wma, output_wav):
    command = ['ffmpeg', '-i', input_wma, output_wav]
    subprocess.run(command, check=True)


def convert_wav_to_wma(input_wav, output_wma):
    command = ['ffmpeg', '-i', input_wav, '-codec:a', 'wmav2', output_wma]
    subprocess.run(command, check=True)


def embed_text_in_wma(input_wma, output_wma, text_file):

    base, ext = os.path.splitext(output_wma)

    temp_wav = base + '.wav'

    with open(text_file, 'r', encoding='utf-8') as file:
        string = file.read()
    convert_wma_to_wav(input_wma, temp_wav)
    em_audio(temp_wav, string, temp_wav)
    convert_wav_to_wma(temp_wav, output_wma)




if len(sys.argv) != 4:
    print("使用方法: python embed.py <coverWMA_path> <inputTxt_path> <stegoWMA_path>")
    sys.exit(1)
    
    # 获取命令行参数
input_wma = sys.argv[1]
text_file = sys.argv[2]
output_wma = sys.argv[3]


embed_text_in_wma(input_wma, output_wma, text_file)