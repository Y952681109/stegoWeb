import os
import argparse
import torch
from transformers import BertModel, BertTokenizer
from ts import Network

def textJudge(text):
    parser = argparse.ArgumentParser(description='MyBert')
    data_name = "../Dataset/2_steganalysis/"   # Steganalysis
    parser.add_argument('-device', type=str, default='cuda', help='device to use for training [default:cuda]')
    parser.add_argument('-idx-gpu', type=str, default='0', help='the number of gpu for training [default:0]')
    parser.add_argument('-dropout', type=float, default=0.05, help='the probability for dropout [default:0.5]')
    parser.add_argument('-load_dir', type=str, default='ts/snapshot/best.pt', help='where to loading the trained model')
    args = parser.parse_args()
    os.environ['CUDA_VISIBLE_DEVICES'] = args.idx_gpu

    args.model = BertModel.from_pretrained('ts/bert-base-uncased')
    args.tokenizer = BertTokenizer.from_pretrained('ts/bert-base-uncased')

    # text = input("Input the text: ")
    model = Network.MyBert(args)    # Bert
    model.load_state_dict(torch.load(args.load_dir), strict=False)
    encoded_input = args.tokenizer(text, return_tensors='pt')
    encoded_input = encoded_input.data
    output = model(encoded_input)
    if output[0, 0] > output[0, 1]:
        return '这段文本是原文  This text is "cover".'
    else:
        return '这段文本是隐写文本  This text is "stego".'
