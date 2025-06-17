import logging
import random
import asyncio
from datetime import datetime
from telegram import Update
from telegram.ext import (
    ApplicationBuilder, CommandHandler, ContextTypes
)

# إعدادات البوت
BOT_TOKEN = "7778433338:AAH2O3DH0ZfonJ2mKeBXYSOtbjutBWvWlVQ"
CHANNEL_ID = "@dzmmm"  # تأكد أن البوت مشرف بالقناة
QARI_PATH = "misha"  # مجلد القارئ على mp3quran.net
QARI_NAME = "مشاري راشد العفاسي"

# قائمة أسماء السور
SURAH_LIST = [
    "الفاتحة", "البقرة", "آل عمران", "النساء", "المائدة", "الأنعام", "الأعراف", "الأنفال", "التوبة", "يونس",
    "هود", "يوسف", "الرعد", "إبراهيم", "الحجر", "النحل", "الإسراء", "الكهف", "مريم", "طه",
    "الأنبياء", "الحج", "المؤمنون", "النور", "الفرقان", "الشعراء", "النمل", "القصص", "العنكبوت", "الروم",
    "لقمان", "السجدة", "الأحزاب", "سبأ", "فاطر", "يس", "الصافات", "ص", "الزمر", "غافر",
    "فصلت", "الشورى", "الزخرف", "الدخان", "الجاثية", "الأحقاف", "محمد", "الفتح", "الحجرات", "ق",
    "الذاريات", "الطور", "النجم", "القمر", "الرحمن", "الواقعة", "الحديد", "المجادلة", "الحشر", "الممتحنة",
    "الصف", "الجمعة", "المنافقون", "التغابن", "الطلاق", "التحريم", "الملك", "القلم", "الحاقة", "المعارج",
    "نوح", "الجن", "المزمل", "المدثر", "القيامة", "الإنسان", "المرسلات", "النبأ", "النازعات", "عبس",
    "التكوير", "الانفطار", "المطففين", "الانشقاق", "البروج", "الطارق", "الأعلى", "الغاشية", "الفجر", "البلد",
    "الشمس", "الليل", "الضحى", "الشرح", "التين", "العلق", "القدر", "البينة", "الزلزلة", "العاديات",
    "القارعة", "التكاثر", "العصر", "الهمزة", "الفيل", "قريش", "الماعون", "الكوثر", "الكافرون", "النصر",
    "المسد", "الإخلاص", "الفلق", "الناس"
]

# حالة البوت وعدد السور المُرسلة
is_running = True
sent_count = 0

# إعداد اللوق
logging.basicConfig(level=logging.INFO)

async def send_random_surah(app):
    global sent_count, is_running
    while True:
        if is_running:
            index = random.randint(0, 113)
            surah_name = SURAH_LIST[index]
            surah_num = str(index + 1).zfill(3)
            url = f"https://server6.mp3quran.net/{QARI_PATH}/{surah_num}.mp3"
            caption = f"📖 {surah_name}\n🎙️ {QARI_NAME}"
            try:
                await app.bot.send_audio(chat_id=CHANNEL_ID, audio=url, caption=caption)
                sent_count += 1
            except Exception as e:
                logging.error(f"فشل الإرسال: {e}")
        await asyncio.sleep(300)  # كل 5 دقائق

# أوامر التحكم
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 أهلاً بك! هذا بوت نشر القرآن تلقائيًا في القناة.")

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
    surah_num = str(index + 1).zfill(3)
    url = f"https://server6.mp3quran.net/{QARI_PATH}/{surah_num}.mp3"
    caption = f"📖 {surah_name}\n🎙️ {QARI_NAME}"
    await update.message.reply_audio(audio=url, caption=caption)

async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"📊 تم إرسال {sent_count} سورة حتى الآن.")

# التشغيل
async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("status", status))
    app.add_handler(CommandHandler("pause", pause))
    app.add_handler(CommandHandler("resume", resume))
    app.add_handler(CommandHandler("now", now))
    app.add_handler(CommandHandler("stats", stats))
    app.job_queue.run_once(lambda *_: asyncio.create_task(send_random_surah(app)), when=1)
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
