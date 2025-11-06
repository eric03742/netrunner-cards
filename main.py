"""
这个脚本用于将 .png 或 .jpg 格式的高清卡图
转换为各个尺寸的 .webp 格式图片文件
用于服务器网络传输
"""


import os
import requests
import shutil
from PIL import Image


def collect(folder: str, collector: list[str]) -> None:
    """
    遍历文件夹，提取文件夹中所有图片文件的路径
    """

    files = os.listdir(folder)
    for file in files:
        # 名为 Others 的文件夹用于存放非卡图的图片文件
        # 在生成 .webp 格式的卡图文件时会被忽略
        if file == "Others":
            continue

        route = os.path.join(folder, file)
        _, ext = os.path.splitext(file)
        if os.path.isdir(route):
            collect(route, collector)
        elif ext.lower() == ".png" or ext.lower() == ".jpg":
            collector.append(route)


def verify(collector: list[str]) -> None:
    """
    获取 NetrunnerDB 卡牌数据
    并验证本地是否有缺失的卡图
    """

    filenames: set[str] = set()
    for route in collector:
        # 对于双面卡牌或有多个卡图的卡牌
        # 其文件名会在卡牌编号之后添加 -xxxx 后缀以区分卡面
        # 在验证完整性时只保留编号，后缀会被忽略
        filename, ext = os.path.splitext(os.path.basename(route))
        filenames.add(filename.split("-")[0])

    # 有关 NetrunnerDB API 的文档
    # 可参阅 https://netrunnerdb.com/api/2.0/doc
    link = "https://netrunnerdb.com/api/2.0/public/cards"
    result = requests.get(link)
    if result.status_code != 200:
        raise Exception("无法获取NRDB卡牌数据!")

    content = result.json()
    if (content is None) or (content["data"] is None):
        raise Exception("获取的NRDB卡牌数据为空!")

    items = content["data"]
    for item in items:
        # Terminal Directive Campaign/终极指令战役 扩展包
        # 没有中/英文卡图，因此在检查时会被直接忽略
        if item["pack_code"] == "tdc":
            continue

        if item["code"] not in filenames:
            print(f"> 缺失：{item["code"]} {item["title"]}")


def convert(collector: list[str], dest: str) -> None:
    """
    将 collector 中的图片文件转换为各个尺寸的 .webp 格式
    并保存至 dest 所指定的文件夹中
    """

    if os.path.exists(dest):
        shutil.rmtree(dest)

    os.mkdir(dest)
    convert2webp(collector, dest, "xlarge", 750, 1050)  # xlarge 尺寸为 750*1050
    convert2webp(collector, dest, "large", 300, 420)  # large 尺寸为 300*420
    convert2webp(collector, dest, "medium", 164, 230)  # medium 尺寸为 164*230
    convert2webp(collector, dest, "small", 116, 162)  # small 尺寸为 116*162
    convert2webp(collector, dest, "tiny", 50, 70)  # tiny 尺寸为 50*70


def convert2webp(collector: list[str], dest: str, label: str, width: int, height: int) -> None:
    """
    将 collector 中的图片文件转换为指定尺寸的 .webp 格式
    并保存至 dest 文件夹下以尺寸 label 为名的文件夹中
    """

    folder = os.path.join(dest, label)
    os.mkdir(folder)
    for file in collector:
        filename, ext = os.path.splitext(os.path.basename(file))
        destination = os.path.join(folder, filename + ".webp")
        source = Image.open(file).convert("RGBA")
        result = source.resize((width, height))
        result.save(destination, "webp")
        print(f"> 生成：{destination}")


def process(root: str, dest: str) -> None:
    """
    将位于 root 文件夹下的所有图片文件
    转换格式并保存至 dest 所指定的文件夹中
    """

    print(f">>> 处理目录：{root}")
    collector: list[str] = []
    collect(root, collector)
    verify(collector)
    convert(collector, dest)


def main() -> None:
    """
    脚本的主入口
    """

    process("./source/zh", "./webp/zh")  # 处理中文卡图
    process("./source/en", "./webp/en")  # 处理英文卡图


if __name__ == "__main__":
    main()
