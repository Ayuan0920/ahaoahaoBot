# ahaoahaoBot

阿豪自動GIF機器人，根據關鍵字或指定用戶自動回覆GIF

## Features / 功能

    * **Keyword Trigger 關鍵字觸發**：當訊息含特定關鍵字（如 `阿豪`, `豪`, `喵夢`, `にゃむ` 等）時，自動回傳預設GIF連結。
    * **User Mention Trigger 指定用戶觸發**：標註特定用戶（指定ID）時，自動回傳其專屬GIF。
    * **Auto-delete Reply 自動回覆刪除**：原訊息刪除時，bot的回應也會自動被刪除。
    * 支援 Docker、以 .env 環境變數設定TOKEN。

## Setup / 使用教學

### 1. Clone & 安裝

    git clone [REPO_URL]
    cd ahaoahaoBot
    pip install -r requirements.txt

### 2. 設定 Discord Bot 金鑰

在專案根目錄建立 .env 檔案，內容如下（請將你的TOKEN換成實際Bot Token）：

    AHAOTOKEN=你的TOKEN

### 3. 執行方式

本地執行：

    python botKeyWord.py

或 Docker：

    # build
    docker-compose build
    # run
    docker-compose up -d

--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

## 檔案說明

    * `botKeyWord.py`：核心Bot程式。
    * `requirements.txt`：所需Python套件。
    * `Dockerfile`、`docker-compose.yml`：Docker部署用文件。
    * `restart.bat`：Windows平台重啟腳本。

## 注意事項

    * 請確保機器人有管理訊息等必要權限。
    * 關鍵字與指定用戶皆可於 `botKeyWord.py` 靜態調整。
    * 支援多套語言與自定義GIF（僅需調整程式對應對映表即可）。