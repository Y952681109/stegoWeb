import subprocess
import sys

def call_cpp_program(inputMid_path, outputTxt_path):
    # 定义要传递给C++程序的参数
    iuput_filename = inputMid_path
    output_filename = outputTxt_path

    # 将参数转换为字节串，因为C++程序通过stdin读取输入
    input_data = f"{iuput_filename} {output_filename}\n"

    # 调用C++程序
    process = subprocess.Popen(["./stego/mid/hideme2"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    # 向C++程序发送输入数据
    stdout, stderr = process.communicate(input=input_data)

    # 打印程序的输出和错误信息（如果有）
    if stdout:
        print("C++ Program Output:\n", stdout)
    if stderr:
        print("C++ Program Error:\n", stderr)

if len(sys.argv) != 3:
    print("使用方法: python embed.py <inputMid_path> <outputTxt_path>")
    sys.exit(1)

inputMid_path = sys.argv[1]
outputTxt_path = sys.argv[2]


call_cpp_program(inputMid_path, outputTxt_path)