import os

# 方法1：设置环境变量
os.environ['HTTP_PROXY'] = 'http://127.0.0.1:7890'
os.environ['HTTPS_PROXY'] = 'http://127.0.0.1:7890'

# 验证设置
print("当前代理设置：")
print(f"HTTP_PROXY: {os.environ.get('HTTP_PROXY')}")
print(f"HTTPS_PROXY: {os.environ.get('HTTPS_PROXY')}")

# 如果要取消代理，可以：
# os.environ.pop('HTTP_PROXY', None)
# os.environ.pop('HTTPS_PROXY', None)

# 或者设置为空字符串：
# os.environ['HTTP_PROXY'] = ''
# os.environ['HTTPS_PROXY'] = ''
