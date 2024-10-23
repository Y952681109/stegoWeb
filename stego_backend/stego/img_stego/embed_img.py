
import os, torch 
import numpy as np
from torchvision import transforms
from ldm.util import instantiate_from_config
from omegaconf import OmegaConf
from PIL import Image
from tools.ecc import ECC
from tools.eval_metrics import compute_psnr




def embed_and_evaluate(img_secret, cover, output):


    # # 将 56 位字符串按照每 8 位进行分割
    # split_strings = [img_secret[i:i+8] for i in range(0, len(img_secret), 8)]

    # # 将每个 8 位字符串转换为字符
    # char_list = [chr(int(bit, 2)) for bit in split_strings]
    # org_secret = ''.join(char_list)
    # # print(org_secret)

    # secret是字符串不用转，如果是比特流则转为字符串，自动截取前七位字符串作为秘密信息



    image_size = 256
    # Load model

    path_join = "stego/img_stego/"

    config = path_join + 'models/VQ4_mir_inference.yaml'
    weight = path_join + 'models/RoSteALS/epoch=000017-step=000449999.ckpt'

    config = OmegaConf.load(config).model
    secret_len = config.params.control_config.params.secret_len
    config.params.decoder_config.params.secret_len = secret_len
    model = instantiate_from_config(config)
    state_dict = torch.load(weight, map_location=torch.device('cpu'))

    if 'state_dict' in state_dict:
        state_dict = state_dict['state_dict']
    misses, ignores = model.load_state_dict(state_dict, strict=False)
    # print(f'Missed keys: {misses}\nIgnore keys: {ignores}')

    # model = model.cuda()

    model.eval()

    # cover
    tform = transforms.Compose([
        transforms.Resize((image_size, image_size)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5]),
    ])
    cover_org = Image.open(cover).convert('RGB')
    w,h = cover_org.size
    # cover = tform(cover_org).unsqueeze(0).cuda()  # 1, 3, 256, 256

    cover = tform(cover_org).unsqueeze(0)  # 1, 3, 256, 256

    # secret
    ecc = ECC()
    secret = ecc.encode_text([img_secret])  # 1, 100
    # secret = torch.from_numpy(secret).cuda().float()  # 1, 100

    secret = torch.from_numpy(secret).float()  # 1, 100

    # inference
    with torch.no_grad():
        z = model.encode_first_stage(cover)
        z_embed, _ = model(z, None, secret)
        stego = model.decode_first_stage(z_embed)  # 1, 3, 256, 256
        res = stego.clamp(-1,1) - cover  # (1,3,256,256) residual
        res = torch.nn.functional.interpolate(res, (h,w), mode='bilinear')
        res = res.permute(0,2,3,1).cpu().numpy()  # (1,h,w,3)
        stego_uint8 = np.clip(res[0] + np.array(cover_org)/127.5-1., -1,1)*127.5+127.5  
        stego_uint8 = stego_uint8.astype(np.uint8)  # (h,w, 3), ndarray, uint8

        psnr = compute_psnr(np.array(cover_org)[None,...], stego_uint8[None,...])
        # print(type(psnr))

        # save stego
        Image.fromarray(stego_uint8).save(output)
        print(f'Stego saved to {output}')
        return psnr

        # # decode secret
        # print('Extracting secret...')
        # extra_org = Image.open(output).convert('RGB')
        # stego = tform(extra_org).unsqueeze(0).cuda()  # 1, 3, 256, 256
        # secret_pred = (model.decoder(stego) > 0).cpu().numpy()  # 1, 100

        # # print(f'Bit acc: {np.mean(secret_pred == secret.cpu().numpy())}')
        # # print(f'secret_pred: {np.array(secret_pred, dtype=float)}')
        # # print(f'secret_real: {secret.cpu().numpy()}')

        # secret_decoded = ecc.decode_text(secret_pred)[0]

        # print(f'original secret : {org_secret}')
        # print(f'Recovered secret: {secret_decoded}')


        # binary_sequence = ''.join(format(ord(char), '08b') for char in secret_decoded)

        # # 比较恢复的01序列和原01序列的准确率
        # total_bits = len(img_secret)
        # matched_bits = sum(bit1 == bit2 for bit1, bit2 in zip(img_secret, binary_sequence))
        # accuracy = (matched_bits / total_bits) * 100
        # print(f'Bit Accuracy: {accuracy}%')

        # return binary_sequence
        # return secret_decoded


# os.environ["CUDA_VISIBLE_DEVICES"] = "1"


# config = 'models/VQ4_mir_inference.yaml'
# weight = 'models/RoSteALS/epoch=000017-step=000449999.ckpt'

# img_secret = embed_and_evaluate(secret, cover, output, config, weight)
# # secret = embed_and_evaluate('ÿØÿàJ', 'examples/split_images/tile_2_3.jpg', 'steg1.jpg')

# print(img_secret)


# secret = '7'
# cover = 'examples/split/split_images/tile_0_0.jpg'
# output = 'steg.jpg'
# embed_and_evaluate(secret, cover, output)






