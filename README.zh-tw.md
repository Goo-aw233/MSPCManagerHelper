<h1 align="center">MSPCManagerHelper</h1>

## 🖹 選擇語言

Select your region and language to continue.

選擇你的語言地區以繼續。

[English (United States)](./README.md) | [簡體中文 (中國)](./README.zh-cn.md)

## 👏 簡介

這是 **Microsoft 官方**出品的電腦輔助軟體“Microsoft 電腦管家”的輔助工具“Microsoft 電腦管家助手”，本工具旨在幫助使用者解決遇到問題時提供快速、便捷的解決方案。歡迎前往 <https://pcmanager.microsoft.com> 下載並體驗最新版 Microsoft 電腦管家！😉

> [!IMPORTANT]
> 這並不是微軟及其子公司官方組織編寫的輔助工具，輔助工具編寫者並非微軟及其子公司的員工，本輔助工具中的內容也與微軟及其子公司本身無關。

> [!NOTE]
> 請注意，本輔助工具部分內容引用了來自第三方（即非 Microsoft 官方）網頁的連結。這些網頁似乎提供了準確、安全的資訊以幫助你解決問題。但是，請仍然留意網頁中推廣的通常被歸類為 PUP（Potentially Unwanted Products，潛在有害產品）的廣告。在您下載及安裝文件或應用前，請徹底地研究網頁中推廣的任何產品。

## 💻 開發

1. 從 [Python](https://www.python.org/downloads) 下載 Python 3.11 版本。

2. 將倉庫 Clone 至本地

```
git clone https://github.com/Goo-aw233/MSPCManagerHelper.git
cd MSPCManagerHelper
```

3. 創建並啟用虛擬環境

```
python -m venv <path\to\MSPCManagerHelper>
<path\to\MSPCManagerHelper>\Scripts\activate
```

4. 安裝依賴包

```
pip install -r requirements.txt
pip install requests
```

5. 構建 EXE

直接運行根目錄下的 `build.bat` 即可自己構建。
