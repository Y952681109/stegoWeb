from embed_img import embed_and_evaluate
from extract_img import extract_img
from code_secret import encode_secret,decode_secret
import os

os.environ["CUDA_VISIBLE_DEVICES"] = "1"

# 嵌入
secret = '编码'
# 中英文统一编码
secret = encode_secret(secret)
cover = 'examples/cover4.jpg'
output = 'steg.jpg'
psnr = embed_and_evaluate(secret, cover, output)
# print(f'PSNR: {psnr}')

# 提取
container_img = 'steg.jpg'
img_secret = extract_img(container_img)
# 中英文统一编码
img_secret = decode_secret(img_secret)
print(f'Recovered secret: {img_secret}')


