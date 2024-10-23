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

if __name__ == '__main__':
    embed("context.txt", "plaintext.txt", "embed.txt")
    
