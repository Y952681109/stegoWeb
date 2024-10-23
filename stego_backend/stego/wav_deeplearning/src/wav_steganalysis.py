import wave
import numpy as np
import matplotlib.pyplot as plt

def read_audio(file_path):
    with wave.open(file_path, 'rb') as wav:
        params = wav.getparams()
        frames = wav.readframes(params.nframes)
        samples = np.frombuffer(frames, dtype=np.int16)
    return samples, params

def extract_lsb(samples):
    return samples & 1  # 提取LSB位

def plot_histogram(lsb_data):
    plt.hist(lsb_data, bins=2, edgecolor='black')
    plt.title('Histogram of LSB Data')
    plt.xlabel('LSB Value')
    plt.ylabel('Frequency')
    plt.xticks([0, 1])
    plt.show()

def chi_square_test(lsb_data):
    n = len(lsb_data)
    observed_zeros = np.count_nonzero(lsb_data == 0)
    observed_ones = np.count_nonzero(lsb_data == 1)
    expected = n / 2
    chi_square_stat = ((observed_zeros - expected) ** 2 / expected) + ((observed_ones - expected) ** 2 / expected)
    return chi_square_stat

def detect_lsb_steganography(audio_file_path, segment_size=10000):
    samples, params = read_audio(audio_file_path)
    lsb_data = extract_lsb(samples)

    num_segments = len(lsb_data) // segment_size
    chi_square_stats = []

    for i in range(num_segments):
        segment = lsb_data[i * segment_size:(i + 1) * segment_size]
        chi_square_stat = chi_square_test(segment)
        if(chi_square_stat<1000.0):
            chi_square_stats.append(chi_square_stat)
            print(f"Segment {i + 1}: Chi-Square Statistic: {chi_square_stat}")

    avg_chi_square_stat = np.mean(chi_square_stats)
    print(f"Average Chi-Square Statistic: {avg_chi_square_stat}")

    # plot_histogram(lsb_data)

    # 根据平均卡方统计量判断隐写信息的存在
    if avg_chi_square_stat > 3.841:  # 1度自由度下的临界值，显著性水平为0.05
        print("Possible steganography detected!")
    else:
        print("No significant evidence of steganography detected.")

# 使用示例
audio_file_path = 'output.wav'
detect_lsb_steganography(audio_file_path)
