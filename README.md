# netrunner-cards

*《矩阵潜袭》卡图及处理脚本工具*

## 简介

`netrunner-cards` 是用于存放《矩阵潜袭》卡牌图片资源、处理/转换图片资源脚本及打包/部署卡图资源服务器脚本的仓库。

## 卡图资源

本项目将原有的JPG/PNG格式卡图转换为了体积更小、更便于网络传输的WEBP格式图片文件。

* 中文/英文卡图分别保存在 `webp` 文件夹下 `zh`/`en` 文件夹中；
* 对每张卡图，都生成了以下五种尺寸的文件，分别保存在对应尺寸的文件夹中，方便在不同的场景下选用合适的尺寸：
  * **xlarge**：750x1050
  * **large**：300x420
  * **medium**: 164x230
  * **small**：116x162
  * **tiny**：50x70
* 卡图文件的命名遵循 [NetrunnerDB](https://netrunnerdb.com/) 对卡图的命名规则。

## 部署

使用以下指令生成Docker镜像：

```shell
docker build -t <镜像标签> .
```

或使用项目中的 `docker-compose.yml` 文件运行图片资源服务器：

```shell
docker compose up -d
```

## 版权信息

本项目中的卡图来源：

* 英文卡图
  * FFG：[Netrunner cards @600dpi](https://drive.google.com/drive/folders/1WwMF6danrz8qvY-yZ5R9wSiFVRESZO7a)
  * NSG：[Null Signal Games 官网](https://nullsignal.games/products/) 上的PNP文件
* 中文卡图
  * 深网补给池

本仓库中的所有卡图版权属于Fantasy Flight Games、Wizards of the Coast、Null Signal Games及简体中文版本翻译者等主体所有，本仓库只用于技术开发，并不使用这些卡图进行任何商业用途，也不拥有这些卡图的版权。

本仓库及其开发者与Fantasy Flight Games、Wizards of the Coast、Null Signal Games、NetrunnerDB等主体均无关联。

## 作者

[Eric03742](https://github.com/eric03742)
