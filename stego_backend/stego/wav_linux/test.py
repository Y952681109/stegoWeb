import ctypes

# 确定动态链接库的路径
lib = ctypes.CDLL("./libaudio.so")
decrypt_func = ctypes.c_char_p(b"sm4")
key = ctypes.c_char_p(b"1234567890123456")
cover_type = ctypes.c_char_p(b"audio")


#embed(char* stega_name, char* cover_path, char* secret_path, char* output_path, char* encrypt_func, char* key);
#stega_name: 嵌入—提取算法名称
#cover_path: 载体路径
#secret_path: 秘密信息路径
#output_path: 输出载秘文件路径
#encrypt_func: 加密方法
#key: 秘钥

cover_path = ctypes.c_char_p(b"input.wav")
secret_path = ctypes.c_char_p(b"secret.txt")
output_path = ctypes.c_char_p(b"output.wav")

lib.embed(cover_type,cover_path, secret_path,output_path,decrypt_func,key)



# extract(char* cover_type, char* cover_path, char* output_path, char* decrypt_func, char* key);
# cover_type:载体类型 {picture audio vedio text}
# cover_path: 载秘文件路径
# output_path: 输出秘密信息路径
# decrypt_func: 解密方法
# key: 秘钥

cover_path = ctypes.c_char_p(b"output.wav")
output_sec = ctypes.c_char_p(b"output_secret")

lib.extract(cover_type,cover_path, output_sec, decrypt_func,key)

