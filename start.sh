#!/bin/bash

# 1. 仮想ディスプレイの起動
Xvfb :0 -screen 0 1280x800x24 &
export DISPLAY=:0

# 2. ウィンドウマネージャーの起動
fluxbox &

# 3. VNCサーバーの起動
# localhostだけでなく0.0.0.0でリッスンさせる設定
x11vnc -display :0 -forever -nopw -rfbport 5900 -shared &

# 4. noVNCの起動
# launch.shが内部でnetstatを使う場合があるため、net-toolsを上記Dockerfileで入れました
/usr/share/novnc/utils/launch.sh --vnc localhost:5900 --listen 8080 &

# 5. Pythonブラウザの起動
# サンドボックスとGPUを無効化することでDocker内でのクラッシュを防ぎます
python3 main.py --no-sandbox --disable-gpu
