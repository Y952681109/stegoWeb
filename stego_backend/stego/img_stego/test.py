# # test chinese string
# chinaStr = "你好"
# changeStr = chinaStr.encode('utf-8')
# print(changeStr)
# print(len(changeStr))
# # 将字节序列转换为二进制字符串表示（每个字节转换为8位二进制）  
# binary_string = ''.join(format(b, '08b') for b in changeStr) 
# print(binary_string)
# print(len(binary_string))
# # 将 56 位字符串按照每 8 位进行分割
# split_strings = [binary_string[i:i+8] for i in range(0, len(binary_string), 8)]
# # 将每个 8 位字符串转换为字符
# char_list = [chr(int(bit, 2)) for bit in split_strings]
# org_secret = ''.join(char_list)
# print(org_secret)
# print(len(org_secret))
# # print(org_secret)
# # test_str = "hello"
# # encode_str = test_str.encode('utf-8')
# # print(encode_str)
# # print(len(encode_str))


# # secret_to_encode = "hello this is a secret, test the long secret"
# secret_to_encode = "你好世界"
# from code_secret import encode_secret
# secret_to_encode = encode_secret(secret_to_encode)
# print(secret_to_encode)
# print(len(secret_to_encode))
# split_fragments = [secret_to_encode[i:i+7] for i in range(0, len(secret_to_encode), 7)]
# print(split_fragments)
# print(len(split_fragments[0]))
# print(len(split_fragments[1]))


# binary_string = "11010010011000010000000000000000"
# split_strings = [binary_string[i:i+8] for i in range(0, len(binary_string), 8)]
# # 将每个 8 位字符串转换为字符
# char_list = [chr(int(bit, 2)) for bit in split_strings]
# org_secret = ''.join(char_list)
# print(org_secret)
# print(len(org_secret))
# print(org_secret[:3])

# # 看看转为比特流是否还有前面的8个0
# binary_bits = ''  
# for char in org_secret:  
#     # 获取字符的ASCII值的二进制表示  
#     ascii_binary = bin(ord(char))[2:].zfill(8)  # 使用zfill确保每个ASCII值都是8位  
#     binary_bits += ascii_binary  

# print(binary_bits)

# for i in range(10):
#     if i == 1:
#         a = i
#     if i==2:
#         print(a)

# print(a)


# import shutil  
  
# # 源文件路径  
# source_file = 'examples/cover3.jpg'  
  
# # 目标文件路径  
# destination_folder = 'examples/split/933.jpg'  
  
# # 使用shutil.copy2函数复制文件，保留元数据（如时间戳）  
# shutil.copy2(source_file, destination_folder)
# max_len = 1113
# max_len = min(max_len,56*7)
# print(max_len)

bit_site = '1111111101'
# 计算需要添加的'0'的数量  
padding_length = (8 - (len(bit_site) % 8)) % 8  
# 使用字符串乘法添加足够的'0'  
bit_site = bit_site + '0' * padding_length 
# 处理第一个小块的嵌入内容
split_strings = [bit_site[i:i+8] for i in range(0, len(bit_site), 8)]
print(split_strings)
# 将每个 8 位字符串转换为字符
char_list = [chr(int(bit, 2)) for bit in split_strings]
first_secret = ''.join(char_list)
print(first_secret)
print(len(first_secret))
