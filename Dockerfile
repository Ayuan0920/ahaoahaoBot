# Dockerfile: 建立 Ahaobot 的容器映像
# 使用官方 Python 3.11 精簡版映像作為基底
FROM python:3.11-slim-buster

# 設定容器內的工作目錄為 /app
WORKDIR /app

# 複製 requirements.txt 到工作目錄
COPY requirements.txt .

# 安裝 requirements.txt 中列出的所有 Python 套件
RUN pip install --no-cache-dir -r requirements.txt

# 複製目前目錄所有檔案到容器的工作目錄 (/app)
COPY . .

# 設定 PYTHONUNBUFFERED=1，確保 Python 不使用緩衝，方便 Docker 及時顯示日誌
ENV PYTHONUNBUFFERED=1

# 設定容器啟動時執行的命令：執行 botKeyWord.py（機器人程式）
CMD ["python", "botKeyWord.py"]
