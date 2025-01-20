import os
import requests
import socket


def make_request_with_proxy():
    # 设置代理
    proxies = {
        "http": "http://127.0.0.1:7890",
        "https": "http://127.0.0.1:7890",
    }

    try:
        # 尝试发送请求
        response = requests.get(
            "http://example.com", proxies=proxies, timeout=5
        )
        return response.text
    except requests.exceptions.ProxyError as e:
        print(f"代理服务器连接错误: {e}")
        # 尝试不使用代理
        try:
            print("尝试不使用代理直接连接...")
            os.environ.pop("HTTP_PROXY", None)
            os.environ.pop("HTTPS_PROXY", None)
            response = requests.get("http://example.com", timeout=5)
            return response.text
        except Exception as e:
            print(f"直接连接也失败: {e}")
    except requests.exceptions.ConnectTimeout:
        print("连接超时")
    except requests.exceptions.ConnectionError as e:
        print(f"连接错误: {e}")
    except Exception as e:
        print(f"其他错误: {e}")
    return None


def check_proxy_connection(host="127.0.0.1", port=7890):
    try:
        # 创建socket连接来测试代理是否可用
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)  # 设置超时时间
        result = sock.connect_ex((host, port))
        if result == 0:
            print(f"代理服务器 {host}:{port} 可以连接")
            return True
        else:
            print(f"代理服务器 {host}:{port} 无法连接")
            return False
    except Exception as e:
        print(f"检查代理时发生错误: {e}")
        return False
    finally:
        sock.close()


if __name__ == "__main__":
    # 首先检查代理是否可用
    if check_proxy_connection():
        print("代理服务器正常，尝试发送请求")
        response = make_request_with_proxy()
        if response:
            print("请求成功")
    else:
        print("代理服务器不可用，请检查代理设置或尝试直接连接")
