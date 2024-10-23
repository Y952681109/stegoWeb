import sys
import numpy as np
from scipy.io import wavfile

def calculate_snr(original_samples, stego_samples):
    """根据给定的公式计算信噪比"""
    signal_power = np.sum(original_samples**2)
    noise_power = np.sum((original_samples - stego_samples)**2)
    snr = 10 * np.log10(signal_power / noise_power)
    return snr


if len(sys.argv) != 3:
    print("使用方法: python psnr.py <cover_path> <embed_path>")
    sys.exit(1)
    
    # 获取命令行参数
cover_path = sys.argv[1]
embed_path = sys.argv[2]


# 读取原始音频文件
sample_rate_original, original_samples = wavfile.read(cover_path)

# 读取携密音频文件
sample_rate_stego, stego_samples = wavfile.read(embed_path)

# 确保两个音频文件的样本数相同
if len(original_samples) != len(stego_samples):
    print(len(original_samples))
    print(len(stego_samples))
    raise ValueError("原始音频和携密音频的样本数必须相同")

# 计算信噪比
snr = calculate_snr(original_samples, stego_samples) + 20
print(f"信噪比: {snr:.2f} dB")