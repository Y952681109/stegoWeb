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


def embed(context_path, plaintext_path, output_path):
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
    with open(plaintext_path, "r") as file:
            plaintext = file.read()

    if len(plaintext) == 0:
        print("plaintext嵌入字符不能为空！")
        sys.exit(1)
    
    # get steganography encoding context
    with open(context_path, "r") as file:
            context = file.read()

    # start steganography pipeline
    print("Loading large LM to GPU, please wait for a few seconds...")
    enc, model, device = get_model(model_name=lm_model, device_id=device)
    
    # Encryption: encrypt secret plaintext to message bits
    print(f"Plaintext: {plaintext}")
    print(f"Encryption method: {encryption_method}")
    if encryption_method == "utf8":
        ba = bitarray.bitarray()
        ba.frombytes(plaintext.encode('utf-8'))
        message = ba.tolist()
    elif encryption_method == "arithmetic":
        message_ctx = [enc.encoder['<|endoftext|>']]
        plaintext += '<eos>'
        message = decode_arithmetic(model, enc, plaintext, message_ctx, device=device, precision=40, topk=60000)
    print(f"Encrypted message bits: {message}")

    # Steganography Encoding: encode message bits to covertext
    print(f"Steganography encoding method: {steganography_method}")
    context_tokens = encode_context(context, enc)
    if steganography_method == 'bins':
        bin2words, words2bin = get_bins(len(enc.encoder), block_size)
        out, nll, kl, words_per_bit = encode_block(model, enc, message, context_tokens, block_size, bin2words, words2bin, device=device)
    elif steganography_method == 'huffman':
        out, nll, kl, words_per_bit = encode_huffman(model, enc, message, context_tokens, block_size, device=device)
    elif steganography_method == 'arithmetic':
        out, nll, kl, words_per_bit, Hq, kl_list = encode_arithmetic(model, enc, message, context_tokens, device=device, temp=temp, precision=precision, topk=topk)
    elif steganography_method == 'saac':
        out, nll, kl, words_per_bit, Hq, topk_list, case_studies = encode_saac(model, enc, message, context_tokens, device=device, temp=temp, precision=precision, topk=topk, nucleus=nucleus)
    covertext = enc.decode(out)
    print(f"Encoded covertext: {covertext}")
    print(f"kl: {kl}, bits/words: {1.0/words_per_bit}")
    
    with open(output_path, 'w') as file:
        file.write(covertext)


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


def check_char_count(file_path):
    try:
        # 打开文件并读取内容
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        print("len: " + str(len(content)))
        # 检查字符数量是否在1到60个之间
        if 1 <= len(content) <= 60:
            return True
        else:
            return False
    except FileNotFoundError:
        print("文件未找到，请检查路径是否正确。")
        return False
    except Exception as e:
        print(f"读取文件时发生错误：{e}")
        return False
    

if __name__ == '__main__':
    # embed("context.txt", "plaintext.txt", "embed.txt")
    
    # 检查是否提供了三个命令行参数
    if len(sys.argv) != 4:
        print("使用方法: python embed.py <context_path> <plaintext_path> <embed_path>")
        sys.exit(1)
    
    # 获取命令行参数
    context_path = sys.argv[1]
    plaintext_path = sys.argv[2]
    embed_path = sys.argv[3]

    result1 = check_file_and_format(context_path, "txt")
    if result1:
        result2 = check_file_and_format(plaintext_path, "txt")
        if result2:
            result3 = check_format(embed_path, "txt")
            if result3:
                embed(context_path, plaintext_path, embed_path)

            else:
                print(embed_path + "文件路径或格式不正确，应为txt格式文件")
                sys.exit(1)


        else:
            print(plaintext_path + "文件路径或格式不正确，应为txt格式文件")
            sys.exit(1)


    else:
        print(context_path + "文件路径或格式不正确，应为txt格式文件")
        sys.exit(1)
    

    # if os.path.exists(context_path):
    #     if os.path.exists(plaintext_path):
    #         # 调用 embed 函数
    #         embed(context_path, plaintext_path, embed_path)
    #     else:
    #         print(f"文件 {plaintext_path} 不存在。")
    # else:
    #     print(f"文件 {context_path} 不存在。")

