import logging
import random
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
)

# إعدادات البوت
BOT_TOKEN   = "ضع_رمز_البوت_هنا"
CHANNEL_ID  = "@dzmmm"      # تأكّد أن البوت مشرف بالقناة
QARI_PATH   = "misha"       # مجلد القارئ في mp3quran.net
QARI_NAME   = "مشاري راشد العفاسي"

# قائمة أسماء السور
SURAH_LIST = [
    # ... (نفس القائمة 114 اسماً كما في السكربت الأصلي) ...
]

# متغيرات الحالة
is_running = True
sent_count = 0

# إعداد اللوق
logging.basicConfig(level=logging.INFO)

# دالة تُرسل سورة عشوائية (تُستدعى كل 5 دقائق)
async def send_random_surah(context: ContextTypes.DEFAULT_TYPE):
    global sent_count, is_running
    if not is_running:
        return

    index = random.randint(0, 113)
    surah_name = SURAH_LIST[index]
    surah_num  = str(index + 1).zfill(3)
    url = f"https://server6.mp3quran.net/{QARI_PATH}/{surah_num}.mp3"
    caption = f"📖 {surah_name}\n🎙️ {QARI_NAME}"

    try:
        await context.bot.send_audio(
            chat_id=CHANNEL_ID,
            audio=url,
            caption=caption
        )
        sent_count += 1
    except Exception as e:
        logging.error(f"فشل الإرسال: {e}")

# --- Handlers للأوامر ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 أهلاً! هذا بوت نشر القرآن تلقائيًا في القناة.")

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    state = "✅ يعمل" if is_running else "⏸️ متوقف"
    await update.message.reply_text(f"حالة البوت: {state}")

async def pause(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global is_running
    is_running = False
    await update.message.reply_text("⏸️ تم إيقاف النشر التلقائي.")

async def resume(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global is_running
    is_running = True
    await update.message.reply_text("▶️ تم تشغيل النشر التلقائي.")

async def now(update: Update, context: ContextTypes.DEFAULT_TYPE):
    index = random.randint(0, 113)
    surah_name = SURAH_LIST[index]
    surah_num  = str(index + 1).zfill(3)
    url = f"https://server6.mp3quran.net/{QARI_PATH}/{surah_num}.mp3"
    caption = f"📖 {surah_name}\n🎙️ {QARI_NAME}"
    await update.message.reply_audio(audio=url, caption=caption)

async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"📊 تم إرسال {sent_count} سورة حتى الآن.")

# --- نقطة الانطلاق الرئيسية ---
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # تسجيل الأوامر
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("status", status))
    app.add_handler(CommandHandler("pause", pause))
    app.add_handler(CommandHandler("resume", resume))
    app.add_handler(CommandHandler("now", now))
    app.add_handler(CommandHandler("stats", stats))

    # جدولة المهمة لتشغيل send_random_surah كل 300 ثانية (5 دقائق)
    app.job_queue.run_repeating(send_random_surah, interval=300, first=0)

    # بدء الاستماع للـ updates
    app.run_polling()

if __name__ == "__main__":
    main()

