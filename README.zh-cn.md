<h1 align="center">MSPCManagerHelper</h1>

## 🖹 选择语言

Select your region and language to continue.

选择你的语言地区以继续。

[English (United States)](./README.md) | [繁體中文 (臺灣)](./README.zh-tw.md)

## 👏 简介

这是 **Microsoft 官方**出品的电脑辅助软件“微软电脑管家”的辅助工具“微软电脑管家助手”，本工具旨在帮助用户解决遇到问题时提供快速、便捷的解决方案。欢迎前往 <https://pcmanager.microsoft.com> 下载并体验最新版微软电脑管家！😉

> [!IMPORTANT]
> 这并不是微软及其子公司官方组织编写的辅助工具，辅助工具编写者并非微软及其子公司的员工，本辅助工具中的内容也与微软及其子公司本身无关。

> [!NOTE]
> 请注意，本辅助工具部分内容引用了来自第三方（即非 Microsoft 官方）网页的链接。这些网页似乎提供了准确、安全的信息以帮助你解决问题。但是，请仍然留意网页中推广的通常被归类为 PUP（Potentially Unwanted Products，潜在有害产品）的广告。在您下载及安装文件或应用前，请彻底地研究网页中推广的任何产品。

## 💻 开发

1. 从 [Python](https://www.python.org/downloads) 下载 Python 3.11 版本。

2. 将仓库 Clone 至本地

```
git clone https://github.com/Goo-aw233/MSPCManagerHelper.git
cd MSPCManagerHelper
```

3. 创建并激活虚拟环境

```
python -m venv <path\to\MSPCManagerHelper>
<path\to\MSPCManagerHelper>\Scripts\activate
```

4. 安装依赖包

```
pip install -r requirements.txt
pip install requests
```

5. 构建 EXE

直接运行根目录下的 `build.bat` 或 `build.sh`即可自己构建。