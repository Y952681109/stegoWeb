import os
import numpy as np
import bitarray
import sys
import re
import math
import argparse

from utils import get_model, encode_context
from block_baseline import get_bins, encode_block, decode_block
from huffman_baseline import encode_huffman, decode_huffman
from arithmetic_baseline import encode_arithmetic, decode_arithmetic
from saac import encode_saac, decode_saac


def extract(context_path, embeded_path, output_path):
    # get model hyperparameters
    lm_model = "gpt2"
    device = "0"
    encryption_method = "utf8"
    steganography_method = "arithmetic"
    precision = 26
    temp = 1.0
    topk = 50
    block_size = 4
    nucleus = 0.95   
    delta = 0.01
    if delta:
        nucleus = 2**(-1.0*delta)

    # get plaintext
    with open(embeded_path, "r") as file:
            embededtext = file.read()

    # get steganography encoding context
    with open(context_path, "r") as file:
            context = file.read()

    # start steganography pipeline
    print("Loading large LM to GPU, please wait for a few seconds...")
    enc, model, device = get_model(model_name=lm_model, device_id=device)
    
    # Encryption: encrypt secret plaintext to message bits
    print(f"Embededtext: {embededtext}")
    print(f"Encryption method: {encryption_method}")

    message_ctx = [enc.encoder['<|endoftext|>']]
    
    context_tokens = encode_context(context, enc)
    
    # Steganography Decoding: decode covertext to message bits
    if steganography_method == 'bins':
        message_rec = decode_block(model, enc, covertext, context_tokens, block_size, bin2words, words2bin)
    elif steganography_method == 'huffman':
        message_rec = decode_huffman(model, enc, covertext, context_tokens, block_size)
    elif steganography_method == 'arithmetic':
        message_rec = decode_arithmetic(model, enc, embededtext, context_tokens, device=device, temp=temp, precision=precision, topk=topk)
    elif steganography_method == 'saac':
        message_rec = decode_saac(model, enc, covertext, context_tokens, device=device, temp=temp, precision=precision, topk=topk, nucleus=nucleus)
    print(f"Decoded message bits: {message_rec}")

    # Decryption: map message bits back to original text
    if encryption_method == "utf8":
        message_rec = [bool(item) for item in message_rec]
        ba = bitarray.bitarray(message_rec)
        reconst = ba.tobytes().decode('utf-8', 'ignore')
    elif encryption_method == "arithmetic":
        reconst = encode_arithmetic(model, enc, message_rec, message_ctx, device=device, precision=40, topk=60000)
        reconst = enc.decode(reconst[0])
    print("Recovered plaintext:", reconst)
    
    with open(output_path, "w") as file:
      file.write(reconst)

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




if __name__ == '__main__':
    # extract("context.txt", "embed.txt", "extract.txt")
    
    # 检查是否提供了三个命令行参数
    if len(sys.argv) != 4:
        print("使用方法: python extract.py <context_path> <embed_path> <extract_path>")
        sys.exit(1)
    
    # 获取命令行参数
    context_path = sys.argv[1]
    embed_path = sys.argv[2]
    extract_path = sys.argv[3]



    result1 = check_file_and_format(context_path, "txt")
    if result1:
        result2 = check_file_and_format(embed_path, "txt")
        if result2:
            result3 = check_format(extract_path, "txt")
            if result3:
                extract(context_path, embed_path, extract_path)

            else:
                print(extract_path + "文件路径或格式不正确，应为txt格式文件")
                sys.exit(1)


        else:
            print(embed_path + "文件路径或格式不正确，应为txt格式文件")
            sys.exit(1)


    else:
        print(context_path + "文件路径或格式不正确，应为txt格式文件")
        sys.exit(1)
    

    # if os.path.exists(context_path):
    #     if os.path.exists(embed_path):
    #         # 调用 embed 函数
    #         extract(context_path, embed_path, extract_path)
    #     else:
    #         print(f"文件 {embed_path} 不存在。")
    # else:
    #     print(f"文件 {context_path} 不存在。")
