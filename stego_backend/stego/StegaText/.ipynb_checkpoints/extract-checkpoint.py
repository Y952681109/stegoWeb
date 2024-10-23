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


if __name__ == '__main__':
    extract("context.txt", "embed.txt", "extract.txt")
   
