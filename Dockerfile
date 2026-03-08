FROM debian:bullseye-slim

# OSの依存関係をインストール
RUN apt-get update && apt-get install -y \
    python3-pip python3-pyqt6 python3-pyqt6.qtwebengine \
    xvfb fluxbox x11vnc novnc websockify \
    libgl1-mesa-glx \
    && apt-get clean

WORKDIR /app
COPY . .

# Pythonライブラリのインストール
RUN pip3 install PyQt6 PyQt6-WebEngine

# 実行権限の付与
RUN chmod +x start.sh

EXPOSE 8080
CMD ["./start.sh"]
