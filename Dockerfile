# syntax=docker/dockerfile:1
# 官方 Dev Container Python 基礎鏡像，原生兼容 VS Code 開發環境
FROM mcr.microsoft.com/devcontainers/python:2-3.12-bookworm

# Python 環境優化配置
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 統一 UID/GID，與 compose.yml 中的用戶配置完全匹配
ARG UID=10001
ARG GID=10001

# 創建非特權用戶 appuser，修復歷史配置問題：
# 1. 創建真實家目錄，解決 VS Code 配置寫入問題
# 2. 使用 /bin/bash 交互式終端，解決 Dev Container 終端無法使用的問題
# 3. 配置免密 sudo 權限，滿足開發場景需求
RUN groupadd --gid "${GID}" appuser \
    && adduser \
        --disabled-password \
        --gecos "" \
        --home "/home/appuser" \
        --shell "/bin/bash" \
        --uid "${UID}" \
        --gid "${GID}" \
        appuser \
    && echo "appuser ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

# 告訴 VS Code Dev Container 使用 appuser 作為默認用戶
ENV VSCODE_USER=appuser
ENV USER=appuser
ENV HOME=/home/appuser

# 工作目錄設定
WORKDIR /app

# 安裝系統依賴
RUN rm -f /etc/apt/sources.list.d/yarn.list \
    && apt update && apt install -y --no-install-recommends \
    sudo \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# 優化：分層安裝 Python 依賴，利用 Docker 緩存加速構建
RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=bind,source=requirements.txt,target=requirements.txt \
    python -m pip install --upgrade pip \
    && python -m pip install -r requirements.txt

# 設置默認文件創建權限，確保新建文件有正確的讀寫權限
RUN umask 002

# 複製項目源碼，並賦予 appuser 完整權限
COPY --chown=appuser:appuser . .
RUN chown -R appuser:appuser /app \
    && chmod -R 775 /app

# 切換到非特權用戶運行
USER appuser

# 暴露服務端口
EXPOSE 8001

# 默認啟動命令（Dev Container 會自動覆蓋此命令，不影響開發）
CMD ["uvicorn", "app:app", "--host=0.0.0.0", "--port=8001", "--reload"]