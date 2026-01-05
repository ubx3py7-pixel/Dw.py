#!/bin/bash

echo "=============================="
echo "🤖 YouTube Bot Auto Setup"
echo "=============================="
echo

# -----------------------------
# Check Python (do NOT install)
# -----------------------------
if ! command -v python3 &>/dev/null; then
    echo "❌ Python3 not found"
    echo "Install Python manually first"
    exit 1
fi
echo "✅ Python found: $(python3 --version)"

# -----------------------------
# Update system
# -----------------------------
echo
echo "🔄 Updating system..."
if command -v apt &>/dev/null; then
    sudo apt update -y
elif command -v pkg &>/dev/null; then
    pkg update -y
fi

# -----------------------------
# Install ffmpeg
# -----------------------------
echo
echo "🎬 Installing ffmpeg..."
if command -v apt &>/dev/null; then
    sudo apt install ffmpeg -y
elif command -v pkg &>/dev/null; then
    pkg install ffmpeg -y
fi

# -----------------------------
# Install nodejs (JS runtime)
# -----------------------------
echo
echo "⚙️ Installing nodejs..."
if ! command -v node &>/dev/null; then
    if command -v apt &>/dev/null; then
        sudo apt install nodejs -y
    elif command -v pkg &>/dev/null; then
        pkg install nodejs -y
    fi
else
    echo "✅ Node.js already installed"
fi

# -----------------------------
# Install yt-dlp
# -----------------------------
echo
echo "⬇️ Installing yt-dlp..."
pip install -U yt-dlp

# -----------------------------
# Install Python packages
# -----------------------------
echo
echo "📦 Installing Python dependencies..."
pip install python-telegram-bot==20.7 spleeter

# -----------------------------
# Verify tools
# -----------------------------
echo
echo "🔍 Verifying installation..."

ffmpeg -version >/dev/null 2>&1 && echo "✅ ffmpeg OK" || echo "❌ ffmpeg failed"
yt-dlp --version >/dev/null 2>&1 && echo "✅ yt-dlp OK" || echo "❌ yt-dlp failed"
node -v >/dev/null 2>&1 && echo "✅ nodejs OK" || echo "❌ nodejs missing"

# -----------------------------
# Done
# -----------------------------
echo
echo "=============================="
echo "✅ SETUP COMPLETED"
echo "=============================="
echo
echo "▶️ Run your bot using:"
echo "python3 dw.py"
