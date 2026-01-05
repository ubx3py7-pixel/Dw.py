import os
import subprocess
import shutil
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from telegram.request import HTTPXRequest

BOT_TOKEN = "8136444382:AAG6BqQuyhTTC0FYReL4_VgDF7Nbfx4W1b4"

BASE_DIR = "downloads"
os.makedirs(BASE_DIR, exist_ok=True)

def run(cmd):
    result = subprocess.run(cmd, shell=True)
    if result.returncode != 0:
        raise RuntimeError(f"Command failed: {cmd}")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 YouTube Auto Downloader Bot (Windows)\n\n"
        "📌 Command:\n"
        "/download <youtube_link>\n\n"
        "Features:\n"
        "🎬 1080p video\n"
        "🎧 MP3 audio\n"
        "🎤 Vocal separation"
    )

async def download_all(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        return await update.message.reply_text("❌ Please provide a YouTube link")

    url = context.args[0]
    chat_id = update.message.chat_id
    work_dir = os.path.join(BASE_DIR, str(chat_id))
    os.makedirs(work_dir, exist_ok=True)

    await update.message.reply_text("⏳ Processing started, please wait...")

    try:
        # ---------------- VIDEO ----------------
        video_path = os.path.join(work_dir, "video.mp4")

        if os.path.exists(video_path):
            await update.message.reply_text("♻️ Video already exists, resending…")
        else:
            await update.message.reply_text("⬇️ Downloading 1080p video…")
            run(
                'yt-dlp '
                '-f "bv*[height<=1080]+ba/best[height<=1080]" '
                '--merge-output-format mp4 '
                f'-o "{os.path.join(work_dir, "video.%(ext)s")}" {url}'
            )

        await update.message.reply_document(
            open(video_path, "rb"),
            filename="video.mp4",
            caption="🎬 1080p Video"
        )

        # ---------------- MP3 ----------------
        mp3_path = os.path.join(work_dir, "audio.mp3")

        if not os.path.exists(mp3_path):
            run(f'ffmpeg -y -i "{video_path}" "{mp3_path}"')

        await update.message.reply_audio(
            open(mp3_path, "rb"),
            caption="🎧 MP3 Audio"
        )

        # ---------------- VOCALS ----------------
        wav_path = os.path.join(work_dir, "song.wav")

        if not os.path.exists(wav_path):
            run(f'ffmpeg -y -i "{video_path}" "{wav_path}"')

        spleeter_out = os.path.join(work_dir, "song")

        if not os.path.exists(spleeter_out):
            run(f'spleeter separate -p spleeter:2stems -o "{work_dir}" "{wav_path}"')

        vocals = os.path.join(spleeter_out, "vocals.wav")
        music = os.path.join(spleeter_out, "accompaniment.wav")

        await update.message.reply_audio(open(vocals, "rb"), caption="🎤 Vocals")
        await update.message.reply_audio(open(music, "rb"), caption="🎵 Music")

        await update.message.reply_text("✅ Completed successfully")

    except Exception as e:
        await update.message.reply_text(f"❌ Error:\n{e}")

    finally:
        # Windows-safe cleanup
        shutil.rmtree(work_dir, ignore_errors=True)

# ⏱️ Telegram timeout fix
request = HTTPXRequest(
    connect_timeout=60,
    read_timeout=600,
    write_timeout=600,
    pool_timeout=60
)

app = ApplicationBuilder().token(BOT_TOKEN).request(request).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("download", download_all))

print("🤖 Bot running on Windows...")
app.run_polling()
