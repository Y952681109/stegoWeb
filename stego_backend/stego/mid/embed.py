import subprocess
import sys

def call_cpp_program(coverMid_path, inputTxt_path, stegoMid_path):
    # 定义要传递给C++程序的参数
    iuput_filename = coverMid_path
    output_filename = stegoMid_path
    secret_filename = inputTxt_path

    # 将参数转换为字节串，因为C++程序通过stdin读取输入
    input_data = f"{iuput_filename} {output_filename} {secret_filename}\n"

    # 调用C++程序
    process = subprocess.Popen(["./stego/mid/hideme"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    # 向C++程序发送输入数据
    stdout, stderr = process.communicate(input=input_data)

    # 打印程序的输出和错误信息（如果有）
    if stdout:
        print("C++ Program Output:\n", stdout)
    if stderr:
        print("C++ Program Error:\n", stderr)

if len(sys.argv) != 4:
    print("使用方法: python embed.py <coverMid_path> <inputTxt_path> <stegoMid_path>")
    sys.exit(1)

coverMid_path = sys.argv[1]
inputTxt_path = sys.argv[2]
stegoMid_path = sys.argv[3]


call_cpp_program(coverMid_path, inputTxt_path, stegoMid_path)