FROM debian:bullseye

ENV DEBIAN_FRONTEND=noninteractive

# 依存関係を網羅的にインストール
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3-pip \
    python3-dev \
    xvfb \
    fluxbox \
    x11vnc \
    novnc \
    websockify \
    net-tools \
    # ここから下がGUI/WebEngineに必須のライブラリ
    libgl1-mesa-glx \
    libegl1-mesa \
    libdbus-1-3 \
    libxkbcommon-x11-0 \
    libi2c-dev \
    libpci3 \
    libnss3 \
    libasound2 \
    libxtst6 \
    libxrandr2 \
    libgbm1 \
    fonts-noto-cjk \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . .

# PyQt6のインストール
RUN pip3 install --no-cache-dir PyQt6 PyQt6-WebEngine

RUN chmod +x start.sh

EXPOSE 8080
CMD ["./start.sh"]
