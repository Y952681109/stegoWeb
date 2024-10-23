import sys

def check_string_length(s):
    if len(s) > 7:
        print("错误：字符串长度大于7")
        sys.exit(1)  # 使用非零的退出状态码表示异常情况
    else:
        print("字符串长度在允许范围内")

    print("hello world")

# 测试示例
test_string = "OpenA123"
check_string_length(test_string)

# 其他代码（只有在字符串长度不大于7时才会执行）
print("程序继续运行")
