import os
import re
import requests
from urllib.parse import urlparse

def download_and_replace_md_images(md_file, output_base_dir):
    # 提取 md 文件名（不含扩展名）
    md_name = os.path.splitext(os.path.basename(md_file))[0]
    # 创建该 md 文件的专属图片目录
    output_dir = os.path.join(output_base_dir, md_name)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 读取 Markdown 文件内容
    with open(md_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # 正则匹配 <img> 标签中的 src 链接
    img_pattern = r'<img [^>]*src="(http[s]?://[^\s"]+\.(?:png|jpg|jpeg|gif|bmp))"[^>]*>'
    matches = re.findall(img_pattern, content)

    for img_url in matches:
        try:
            # 提取原始文件名
            parsed_url = urlparse(img_url)
            original_filename = os.path.basename(parsed_url.path)  # 提取文件名
            local_filepath = os.path.join(output_dir, original_filename)

            # 下载图片到本地
            if not os.path.exists(local_filepath):  # 避免重复下载
                response = requests.get(img_url, stream=True)
                response.raise_for_status()

                with open(local_filepath, 'wb') as img_file:
                    for chunk in response.iter_content(1024):
                        img_file.write(chunk)
                print(f"Downloaded: {img_url} -> {local_filepath}")
            else:
                print(f"Already exists: {local_filepath}, skipping download.")

            # 替换 Markdown 文件中的 <img> 标签为本地图片路径
            relative_path = os.path.relpath(local_filepath, os.path.dirname(md_file))
            content = content.replace(img_url, relative_path)
        except Exception as e:
            print(f"Failed to download {img_url}: {e}")

    # 将修改后的内容写回 Markdown 文件
    with open(md_file, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Processed: {md_file}, images saved in {output_dir}")

def process_all_md_files(base_dir):
    # 遍历当前目录及子目录中所有 Markdown 文件
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file.endswith(".md"):
                md_file_path = os.path.join(root, file)
                download_and_replace_md_images(md_file_path, os.path.join(base_dir, "images"))

# 示例用法
base_directory = "."  # 当前目录
process_all_md_files(base_directory)
