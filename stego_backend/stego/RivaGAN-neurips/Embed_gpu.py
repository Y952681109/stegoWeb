#coding=utf-8
import gc
import cv2
import torch
from tqdm import tqdm
from moviepy.editor import *
import os

def Add_Audio(Ori_video,Obj_video,End_video):           #视频轨  音轨
    video1 = VideoFileClip(Ori_video)  # 视频所在路径
    audio1 = video1.audio
    video2 =VideoFileClip(Obj_video)
    video3=video2.set_audio(audio1)
    video3.write_videofile(End_video, codec='libx264')
    video2.close()

    path = Obj_video  # 文件路径
    if os.path.exists(path):  # 如果文件存在
        os.remove(path)
    else:
        print('no such file:%s' % path)  # 则返回文件不存在


def encode(s):
    return ''.join([bin(ord(c)).replace('0b', '') for c in s])

def decode(s):
    return ''.join([chr(i) for i in [int(b, 2) for b in s.split(' ')]])

def str_tensor(str):
    msg = encode(str)
    # data = torch.zeros([1,32])
    data = torch.zeros([1,32]).cuda()
    for i in range(len(msg)-1):
        if (msg[i] == '0'):
            data[0][i] = 0.0
        else:
            data[0][i] = 1.0
    return data


def EmbedMark(mdir,path_to_data,data,path_embed=None):

    torch.backends.cudnn.benchmark = True
    SEQ_LEN = 3
    SEQ_LEN_MIDDLE = SEQ_LEN // 2
    gc.collect()
    path_os = "stego/RivaGAN-neurips/"

    path_to_model = path_os +  "results/1557517365/model.pt"
    if not (os.path.exists(path_to_model)):
        path_to_model = mdir + "\\RivaGAN-neurips\\results\\1557517365\\model.pt"

    print('模型加载开始')
    encoder, decoder, _, _ = torch.load(path_to_model, map_location=torch.device('cpu'))
    print('模型加载成功')
    encoder, decoder = map(lambda x: x.cuda(), (encoder, decoder))
    # encoder, decoder = map(lambda x: x, (encoder, decoder))
    encoder.eval()
    decoder.eval()


    if (path_embed==None):                       #没有输入文件的生成路径，使用源视频的路径，并且岸源视频的格式存储
        path_embed = path_to_data * 1
        path_embed = path_embed.replace('/', '//')
        path_prefix =path_embed.split('.',1)[0]
        path_suffix =path_embed.split('.',1)[1]
        path_embed=path_prefix+'temp.'+path_suffix


    if (path_suffix=='mp4'):
        videocode='mp4v'
    else:
        videocode='XVID'

    with torch.no_grad():
        frames = []
        vin = cv2.VideoCapture(path_to_data)
        width = int(vin.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(vin.get(cv2.CAP_PROP_FRAME_HEIGHT))
        nb_frames = int(vin.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = int(vin.get(cv2.CAP_PROP_FPS))
        vout2 = cv2.VideoWriter(path_embed , cv2.VideoWriter_fourcc(*videocode), fps, (width, height))

        for _ in tqdm(range(nb_frames)):
            try:
                ok, frame = vin.read()
                frames.append(frame)
                if len(frames) < SEQ_LEN:
                    continue
                frames = frames[-SEQ_LEN:]
                # x = torch.FloatTensor(frames) / 127.5 - 1.0  # (L, H, W, 3)         归一化处理
                x = torch.cuda.FloatTensor(frames) / 127.5 - 1.0  # (L, H, W, 3)         归一化处理
                x = x.permute(3, 0, 1, 2).unsqueeze(0).cuda()  # (1, 3, L, H, W)
                # x = x.permute(3, 0, 1, 2).unsqueeze(0)  # (1, 3, L, H, W)
                y = encoder(x, data)  # (1, 3, L, H, W)
                image = torch.clamp(y[0, :, SEQ_LEN_MIDDLE, :, :].permute(1, 2, 0), min=-1.0, max=1.0)
                vout2.write(((image + 1.0) * 127.5).detach().cpu().numpy().astype("uint8"))
            except:
                pass
    return path_embed



def Embed_API(mdir,str,path_to_data,path_end):


    try:
        # print(str)
        data=str_tensor(str)          #将字符串转化为张量信息
        # print(data)
    except IOError:
        print("将字符串转化为张量信息失败")

    with torch.no_grad():
        path_embed=EmbedMark(mdir,path_to_data, data)

    try:
        Add_Audio(path_to_data,path_embed,path_end)
    except IOError:
        print("视频加音轨失败")


# if __name__=="__main__":
#     print('开始')
#     data=sys.argv[1]
#     ori_path=sys.argv[2]
#     end_path=sys.argv[3]
#     dir = sys.argv[4]
#     os.chdir(dir)
#     Embed_API(data,ori_path,end_path)


