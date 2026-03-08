#!/bin/bash

# 仮想ディスプレイの設定
Xvfb :0 -screen 0 1280x800x24 &
export DISPLAY=:0

# ウィンドウマネージャーの起動
fluxbox &

# VNCサーバーの起動
x11vnc -display :0 -forever -nopw -listen localhost -xkb &

# noVNCの起動
/usr/share/novnc/utils/launch.sh --vnc localhost:5900 --listen 8080 &

# Pythonブラウザの起動
# --no-sandbox は Docker環境でWebEngineを動かすために必須
python3 main.py --no-sandbox
