import gc
import cv2
import json
import torch
import random
import imageio
import numpy as np
from model import *
from glob import glob
from tqdm import tqdm
import Embed
import warnings
import sys
import io
import os
import binascii

sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

random.seed(42)
np.random.seed(42)
torch.manual_seed(42)

torch.backends.cudnn.benchmark = False
SEQ_LEN = 3
SEQ_LEN_MIDDLE = SEQ_LEN // 2

bitsList = []
bitsDict = {}

def decode(s):
    return ''.join([chr(i) for i in [int(b, 2) for b in s.split(' ')]]).strip(b'\x00'.decode())

def toBit2Str(model_out):        #每次模型检测输出：将01比特流转化为字符串
    # >0  1
    # <0  0
    bits = ''
    count = 0
    for i in model_out:
        if(i>0):
            bits+='1'
        else:
            bits+='0'
        if(count == 6):
            bits+=' ';
            count=0
        else:
            count+=1
    # print("01_mark :"+bits)
    bitsList.append(bits)

    bits = decode(bits)
    # print(type(bits))
    # print("String  :"+bits)


def Is_Mark(mdir,path_to_data):
    # Generate metrics
    gc.collect()
    path_os = "stego/RivaGAN-neurips/"

    path_to_model = path_os + "results/1557517365/model.pt"
    if not (os.path.exists(path_to_model)):
        path_to_model = mdir+"\\RivaGAN-neurips\\results\\1557517365\\model.pt"

    # data
    # encoder, decoder, _, _ = torch.load(path_to_model)
    encoder, decoder, _, _ = torch.load(path_to_model, map_location=torch.device('cpu'))
    # encoder, decoder = map(lambda x: x.cuda(), (encoder, decoder))
    encoder, decoder = map(lambda x: x, (encoder, decoder))
    encoder.eval()
    decoder.eval()


    with torch.no_grad():
        gc.collect()
        vin = cv2.VideoCapture(path_to_data)
        width = int(vin.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(vin.get(cv2.CAP_PROP_FRAME_HEIGHT))
        height, width = 4 * (height // 8), 4 * (width // 8)
        nb_frames = int(vin.get(cv2.CAP_PROP_FRAME_COUNT)) - 10
        # vin.set(cv2.CAP_PROP_POS_FRAMES, 10)
        frames = []
        # print(nb_frames)
        for _ in tqdm(range(nb_frames)):
            ok, frame = vin.read()
            frames.append(frame[:height,:width])
            if len(frames) < SEQ_LEN:
                continue
            frames = frames[-SEQ_LEN:]
            # print(frames)
            # x = torch.cuda.FloatTensor(frames) / 127.5 - 1.0  # (L, H, W, 3)
            x = torch.FloatTensor(frames) / 127.5 - 1.0  # (L, H, W, 3)
            x = x.permute(3, 0, 1, 2).unsqueeze(0)  # (1, 3, L, H, W)
            # x = x.permute(3, 0, 1, 2).unsqueeze(0).cuda()  # (1, 3, L, H, W)
            y_out = decoder(torch.clamp(x.detach(), min=-1.0, max=1.0))
            # print(y_out[0])
            toBit2Str(y_out[0])

    # for a in bitsList:
    #     int(a)
    for i in bitsList:
        flag = decode(i).isalnum()  # 判断是否为数字和字母的组合 包括纯数字和纯字母
        if flag:
            if i not in bitsDict.keys():
                bitsDict[decode(i)] = bitsList.count(i)
    # it[0] 按key排序   it[1] 按value排序
    # bitsDict_final = sorted(bitsDict.items(), key=lambda it: it[1], reverse=True) # True降序 False升序
    # (bitsDict)

    res = ""

    list_key = find_key(bitsDict)
    if len(list_key) > 1 :
        for i in range(0, len(list_key)):
            print(list_key[i])
            res+=list_key[i]
    elif len(list_key) == 0:
        print("提取失败！")
    else:
        print(list_key[0])
        res+=list_key[0]

    return res
    # print(list(bitsDict_final.keys())[0])

def find_key(dict_input):
    list_keys = []
    for i in range(len(list(dict_input.keys()))):
        if list(dict_input.values())[i] == max(list(dict_input.values())):
            list_keys.append(list(dict_input.keys())[i])
    return list_keys

# if __name__ == "__main__":
#
#     movie_path = sys.argv[1]
#     data = sys.argv[2]
#     dir=sys.argv[3]    #result路径
#
#     os.chdir(dir)
#     data = Embed.str_tensor(data)  # 将字符串转化为张量信息
#     with torch.no_grad():
#         Is_Mark(movie_path, data)