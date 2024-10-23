import ctypes 

lib = ctypes.CDLL("./lib/libmp4stego.so")


cover_mp4 = ctypes.c_char_p(b"./mp4/sample_2.mp4") #载体mp4视频
intput_txt = ctypes.c_char_p(b"./intput.txt") #待嵌入文本信息
stego_mp4 = ctypes.c_char_p(b"./mp4/output_sample_2.mp4") #隐写mp4视频

lib.embed_secret(cover_mp4,intput_txt,stego_mp4)

# stego_mp4 = ctypes.c_char_p(b"./mp4/output_sample_2.mp4") #隐写mp4视频
# output_txt = ctypes.c_char_p(b"./output.txt") #提取文本信息
# lib.extract_func(stego_mp4,output_txt)
