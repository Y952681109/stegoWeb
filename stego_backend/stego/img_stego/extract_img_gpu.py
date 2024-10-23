import os, torch 
import numpy as np
from torchvision import transforms
from ldm.util import instantiate_from_config
from omegaconf import OmegaConf
from PIL import Image
from tools.ecc import ECC



def extract_img(container_img):

    path_join = "stego/img_stego/"

    config = OmegaConf.load(path_join + "models/VQ4_mir_inference.yaml").model
    # 获取秘密信息长度
    secret_len = config.params.control_config.params.secret_len
    config.params.decoder_config.params.secret_len = secret_len
    # 创建模型实例
    model = instantiate_from_config(config)
    # 加载模型的参数和权重
    state_dict = torch.load(path_join + "models/RoSteALS/epoch=000017-step=000449999.ckpt", map_location=torch.device('cpu'))
    # 
    # if 'global_step' in state_dict:
    #     print(f'Global step: {state_dict["global_step"]}, epoch: {state_dict["epoch"]}')

    if 'state_dict' in state_dict:
        state_dict = state_dict['state_dict']
    # 返回未匹配的、被忽略的键的列表（misses 和 ignores）。
    misses, ignores = model.load_state_dict(state_dict, strict=False)
    # print(f'Missed keys: {misses}\nIgnore keys: {ignores}')
    # 将模型移动到 GPU

    model = model.cuda()
    
    # 设置模型为评估模式
    model.eval()
    ecc = ECC()
    # 对输入的图像进行预处理
    tform = transforms.Compose([
        transforms.Resize((256, 256)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5]),
    ])
    # 使用 PIL 库打开输入图像，并将其转换为 RGB 格式
    extra_org = Image.open(container_img).convert('RGB')
    # .unsqueeze(0)：在张量的最前面添加一个维度，将其转换为形状为 (1, 3, H, W) 的张量
    stego = tform(extra_org).unsqueeze(0).cuda()  # 1, 3, 256, 256

    # stego = tform(extra_org).unsqueeze(0)  # 1, 3, 256, 256

    # decode secret
    # print('Extracting secret...')
    secret_pred = (model.decoder(stego) > 0).cpu().numpy()  # 1, 100
    secret_decoded = ecc.decode_text(secret_pred)[0]
    # print(f'Recovered secret: {secret_decoded}')

    # binary_sequence = ''.join(format(ord(char), '08b') for char in secret_decoded)
    # return binary_sequence


    return secret_decoded


# os.environ["CUDA_VISIBLE_DEVICES"] = "1"
# container_img = 'steg.jpg'
# img_secret = extract_img(container_img)
# print(img_secret)
# # 去掉img_secret后面的空格
# img_secret = img_secret.rstrip()
# print(len(img_secret))


