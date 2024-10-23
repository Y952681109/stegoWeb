

def encode_secret(secret):
    # 将字符串转换为字节序列
    secret = secret.encode('utf-8')
    # print(secret)
    # print(len(secret))
    # 将字节序列转换为二进制字符串表示（每个字节转换为8位二进制）  
    binary_string = ''.join(format(b, '08b') for b in secret) 
    # print(binary_string)
    # print(len(binary_string))
    # 将字符串按照每 8 位进行分割
    split_strings = [binary_string[i:i+8] for i in range(0, len(binary_string), 8)]
    # 将每个 8 位字符串转换为字符
    char_list = [chr(int(bit, 2)) for bit in split_strings]
    org_secret = ''.join(char_list)
    return org_secret
    # print(org_secret)
    # print(len(org_secret))

def decode_secret(secret):
    # 将字符串转换为二进制字符串表示（每个字符转换为8位二进制）
    binary_string = ''.join(format(ord(c), '08b') for c in secret)
    # 将二进制字符串转为字节序列
    # 将二进制字符串分割为8位一组  
    groups = [binary_string[i:i+8] for i in range(0, len(binary_string), 8)]  
      
    # 将每组二进制数转换为对应的十进制数，然后转换为字节序列  
    byte_sequence = bytes([int(group, 2) for group in groups])  
    # 解码字节序列并返回原始字符串
    return byte_sequence.decode('utf-8')
    


# secret = encode_secret('1234567hello')
# print(secret)
# secret = encode_secret(secret)
# print(secret)

# decoded_secret = decode_secret(secret)
# print(decoded_secret)