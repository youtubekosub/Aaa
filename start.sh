#!/bin/bash

# 1. 仮想ディスプレイの起動
Xvfb :0 -screen 0 1280x800x24 &
export DISPLAY=:0

# 2. ウィンドウマネージャーの起動（軽量なfluxbox）
fluxbox &

# 3. VNCサーバーの起動
x11vnc -display :0 -forever -nopw -listen localhost -xkb &

# 4. noVNC（ブラウザでVNCを見るためのプロキシ）の起動
/usr/share/novnc/utils/launch.sh --vnc localhost:5900 --listen 8080 &

# 5. Pythonブラウザアプリの起動
python3 main.py
