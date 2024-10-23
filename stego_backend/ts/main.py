import os
import argparse
import torch
from transformers import BertModel, BertTokenizer
import Network

parser = argparse.ArgumentParser(description='MyBert')
data_name = "../Dataset/2_steganalysis/"   # Steganalysis
parser.add_argument('-device', type=str, default='cuda', help='device to use for training [default:cuda]')
parser.add_argument('-idx-gpu', type=str, default='0', help='the number of gpu for training [default:0]')
parser.add_argument('-dropout', type=float, default=0.05, help='the probability for dropout [default:0.5]')
parser.add_argument('-load_dir', type=str, default='snapshot/best.pt', help='where to loading the trained model')
args = parser.parse_args()
os.environ['CUDA_VISIBLE_DEVICES'] = args.idx_gpu

args.model = BertModel.from_pretrained('./bert-base-uncased')
args.tokenizer = BertTokenizer.from_pretrained('./bert-base-uncased')

text = input("Input the text: ")
model = Network.MyBert(args)    # Bert
model.load_state_dict(torch.load(args.load_dir), strict=False)
encoded_input = args.tokenizer(text, return_tensors='pt')
encoded_input = encoded_input.data
output = model(encoded_input)
if output[0, 0] > output[0, 1]:
	print('This text is "cover".')
else:
	print('This text is "stego".')
