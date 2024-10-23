import os
import openpyxl
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
import numpy as np
import bitarray

# context_path: 上下文路径
# plaintext_path: 秘密信息路径
# output_path: 输出载密文件路径
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
    print(f"kl: {kl}, bits/words: {1.0/words_per_bit}")
    
    with open(output_path, 'w') as file:
        file.write(covertext)
    return kl, 1.0/words_per_bit

def calculate_embedding_rate():
    secret_file = "plaintext.txt"
    sample_dir = "datasets/covid_19"
    embed_file = "embed.txt"
    extract_file = "extract.txt"
    secret_size = os.path.getsize(secret_file)
    total_sample_size = 0
    embedded_size = 0

    # 创建一个 Excel 工作簿
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = "Test Results"
    sheet['A1'] = "Sample File"
    sheet['B1'] = "BitPerWords"
    sheet['C1'] = "KL散度"

    for i in range(1, 101):
        filename = f"plaintext{i}.txt"  # 构造文件名
        sample_file = os.path.join(sample_dir, filename)  # 拼接路径
        sample_size = os.path.getsize(sample_file)
        total_sample_size += sample_size

        # 调用嵌入接口进行秘密信息嵌入
        kl, bpw = embed(sample_file, secret_file, embed_file)

        row = (sample_file, bpw, kl)
        sheet.append(row)

    # 保存 Excel 文件
    workbook.save("test.xlsx")
    # 删除提取后的秘密信息文件
    os.remove(extract_file)
    os.remove(embed_file)

# 调用 calculate_embedding_rate 函数并传入相关参数
calculate_embedding_rate()