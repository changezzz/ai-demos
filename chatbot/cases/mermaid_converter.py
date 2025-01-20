import subprocess
import base64
import requests


def mermaid_to_image(mermaid_text, output_file="output.png", method="api"):
    if method == "api":
        # 方法1：使用 Mermaid 在线 API
        try:
            graphbytes = mermaid_text.encode("ascii")
            base64_bytes = base64.b64encode(graphbytes)
            base64_string = base64_bytes.decode("ascii")
            url = f"https://mermaid.ink/img/{base64_string}"
            response = requests.get(url)
            if response.status_code == 200:
                with open(output_file, "wb") as f:
                    f.write(response.content)
                return True
        except Exception as e:
            print(f"API 方法失败: {e}")
            return False

    elif method == "cli":
        # 方法2：使用 mermaid-cli (需要先安装 @mermaid-js/mermaid-cli)
        try:
            # 保存 Mermaid 文本到临时文件
            with open("temp.mmd", "w") as f:
                f.write(mermaid_text)

            # 使用 mmdc 转换
            subprocess.run(
                ["mmdc", "-i", "temp.mmd", "-o", output_file],
                check=True
            )
            return True
        except Exception as e:
            print(f"CLI 方法失败: {e}")
            return False

    return False


# 使用示例
if __name__ == "__main__":
    # Mermaid 文本示例
    mermaid_text = """
    graph TD
        A[Start] --> B[Process]
        B --> C[End]
    """

    # 尝试转换
    success = mermaid_to_image(mermaid_text, "test.png", method="api")
    if success:
        print("图片生成成功！")
    else:
        print("图片生成失败！")
