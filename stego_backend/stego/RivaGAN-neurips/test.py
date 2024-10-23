import torch
import Embed
from Extract import Is_Mark


dir = ''
data ='BUPT';

if torch.cuda.device_count() > 0:
    # # todo--嵌入秘密信息示例
    # ori_path = 'test_v/1.avi'
    # end_path = 'test_v/1wmm.avi'
    # Embed.Embed_API(dir, data, ori_path, end_path)

    # todo----提取秘密信息示例
    movie_path = 'test_v/1wmm.avi'

    Is_Mark(dir, movie_path);
else:
    print("未找到独立显卡，程序无法运行！")