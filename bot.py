import random
import os
from typing import Final
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from elevenlabs.client import ElevenLabs

TOKEN = os.getenv("8749430751:AAF4XLqfGX9SJhxUFe0DVs3yYElzJKK1-90")
ELEVEN_API_KEY = os.getenv("sk_cba090791cf6a99c680b5cbdb13067ce72b8c66c4674fcd")
eleven_client = ElevenLabs(api_key=ELEVEN_API_KEY)

qorxu = ['Qorxu hekayə 1: Bir gün bir uşaq evdə anası və atası ilə birlikdə oturmuşdu...', "Qorxu hekayə 2: Telefonuna gecə yarısı naməlum mesaj gəldi...", "Qorxu hekayə 3: Balkondan qəribə səs gəldi...", "Qorxu hekayə 4: Pəncərədə kölgə göründü...", "Qorxu hekayə 5: Gecə saat 3-də addım səsləri eşidildi..."]
fantastik = ["Fantastik hekayə 1: Göydə böyük portal açıldı...", "Fantastik hekayə 2: Robotlar insanlarla yaşamağa başladı...", "Fantastik hekayə 3: Bir uşaq zaman maşını tapdı...", "Fantastik hekayə 4: Marsdan siqnal gəldi...", "Fantastik hekayə 5: Görünməzlik paltosu icad edildi..."]
romantik = ["Romantik hekayə 1: Onlar yağışlı gündə tanış oldular...", "Romantik hekayə 2: Köhnə məktub onları yenidən birləşdirdi...", "Romantik hekayə 3: Bir baxış hər şeyi dəyişdi...", "Romantik hekayə 4: Parkda başlayan dostluq sevgiyə çevrildi...", "Romantik hekayə 5: İllər sonra yenidən görüşdülər..."]
maraqli = ["Maraqlı hekayə 1: Bir uşaq köhnə sandıq tapdı...", "Maraqlı hekayə 2: Sandıqdan xəritə çıxdı...", "Maraqlı hekayə 3: Tərk edilmiş adada sirli qapı tapıldı...", "Maraqlı hekayə 4: Kitabın içində gizli mesaj vardı...", "Maraqlı hekayə 5: Köhnə saat zaman səyahəti edə bilirdi..."]

STORIES = {"qorxu": qorxu, "fantastik": fantastik, "romantik": romantik, "maraqli": maraqli}

def menu():
    keyboard = [[InlineKeyboardButton("😱 Qorxu", callback_data="qorxu")], [InlineKeyboardButton("🚀 Fantastik", callback_data="fantastik")], [InlineKeyboardButton("❤️ Romantik", callback_data="romantik")], [InlineKeyboardButton("🤔 Maraqlı", callback_data="maraqli")], [InlineKeyboardButton("🎲 Random hekayə", callback_data="random")]]
    return InlineKeyboardMarkup(keyboard)

def back_button():
    keyboard = [[InlineKeyboardButton("⬅️ Geri menyu", callback_data="menu")]]
    return InlineKeyboardMarkup(keyboard)

def story_menu(category):
    keyboard = [[InlineKeyboardButton(f"Hekayə {i+1}", callback_data=f"{category}_{i}")] for i in range(5)]
    keyboard.append([InlineKeyboardButton("⬅️ Geri menyu", callback_data="menu")])
    return InlineKeyboardMarkup(keyboard)

async def send_voice(text: str, query):
    file_path = "story.mp3"
    audio = eleven_client.text_to_speech.convert(text=text, voice_id="21m00Tcm4TlvDq8ikWAM", model_id="eleven_multilingual_v2", output_format="mp3_44100_128")
    with open(file_path, "wb") as f:
        for chunk in audio:
            if chunk: f.write(chunk)
    with open(file_path, "rb") as audio_file:
        await query.message.reply_voice(audio_file)
    if os.path.exists(file_path): os.remove(file_path)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📚 Hekayə botuna xoş gəldin!\nKateqoriya seç:", reply_markup=menu())

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    if data == "menu": await query.message.reply_text("Kateqoriya seç:", reply_markup=menu())
    elif data in STORIES:
        label = {"qorxu": "Qorxu", "fantastik": "Fantastik", "romantik": "Romantik", "maraqli": "Maraqlı"}[data]
        await query.message.reply_text(f"{label} hekayələrindən birini seç:", reply_markup=story_menu(data))
    elif data == "random":
        all_stories = [s for stories in STORIES.values() for s in stories]
        story = random.choice(all_stories)
        await query.message.reply_text(story, reply_markup=back_button())
        await send_voice(story, query)
    else:
        parts = data.rsplit("_", 1)
        if len(parts) == 2:
            category, index_str = parts
            if category in STORIES and index_str.isdigit():
                index = int(index_str)
                story = STORIES[category][index]
                await query.message.reply_text(story, reply_markup=back_button())
                await send_voice(story, query)

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))
    print("Bot işləyir...")
    app.run_polling()

if __name__ == "__main__":
    main()
