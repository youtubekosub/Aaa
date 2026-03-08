FROM debian:bullseye

# タイムゾーン等の対話型プロンプトを無効化
ENV DEBIAN_FRONTEND=noninteractive

# 依存ライブラリのインストール
# python3-pyqt6.qtwebengine の代わりに必要なシステムライブラリを網羅
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3-pip \
    python3-dev \
    xvfb \
    fluxbox \
    x11vnc \
    novnc \
    websockify \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libnss3 \
    libxcb-icccm4 \
    libxcb-image0 \
    libxcb-keysyms1 \
    libxcb-randr0 \
    libxcb-render-util0 \
    libxcb-xinerama0 \
    libxcb-xinput0 \
    libxkbcommon-x11-0 \
    fonts-noto-cjk \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . .

# PyQt6 と WebEngine を pip で確実にインストール
RUN pip3 install --no-cache-dir PyQt6 PyQt6-WebEngine

RUN chmod +x start.sh

EXPOSE 8080
CMD ["./start.sh"]
