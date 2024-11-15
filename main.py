import telebot
import config
import voice

API_TOKEN = config.bot_token

bot = telebot.TeleBot(API_TOKEN)

# Fetch available voices and prepare keyboard
try:
    voices = voice.get_all_voices()
    voice_buttons = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    for v in voices:
        button = telebot.types.KeyboardButton(v['name'])
        voice_buttons.add(button)
except Exception as e:
    print(f"Ошибка загрузки голосов: {e}")
    voices = []

# User-selected voice tracker
selected_voice = {}


@bot.message_handler(commands=['start'])
def send_welcome(message):
    if voices:
        bot.reply_to(
            message,
            "Привет! Я бот для создания озвучки! Выбери голос, который будет использоваться при создании озвучки:",
            reply_markup=voice_buttons
        )
    else:
        bot.reply_to(
            message,
            "К сожалению, сейчас список голосов недоступен. Попробуйте позже."
        )


@bot.message_handler(commands=['voices'])
def list_voices(message):
    """List available voices."""
    if not voices:
        bot.reply_to(
            message,
            "Не удалось загрузить список голосов. Попробуйте позже."
        )
        return

    text = "Список доступных голосов:\n"
    for i, voice_data in enumerate(voices):
        text += f"{i + 1}. {voice_data['name']} (ID: {voice_data['id']})\n"

    bot.reply_to(message, text)


@bot.message_handler(func=lambda message: message.text in [v['name'] for v in voices])
def voice_selected(message):
    """Handle voice selection."""
    user_id = message.from_user.id
    selected_voice[user_id] = message.text
    bot.reply_to(
        message,
        f"Вы выбрали голос: {message.text}. Теперь введите текст для озвучки:"
    )


@bot.message_handler(func=lambda message: True)
def generate_voice(message):
    """Generate audio for the input text."""
    user_id = message.from_user.id
    if user_id in selected_voice:
        voice_name = selected_voice[user_id]
        try:
            voice_id = next(v['id'] for v in voices if v['name'] == voice_name)
            audio_file = voice.generate_audio(message.text, voice_id)
            if audio_file:
                with open(audio_file, 'rb') as audio:
                    bot.send_voice(user_id, audio)
            else:
                bot.reply_to(
                    message,
                    "Произошла ошибка при создании аудио. Попробуйте снова."
                )
        except Exception as e:
            bot.reply_to(
                message,
                f"Ошибка при создании аудио: {e}. Пожалуйста, попробуйте снова."
            )
    else:
        bot.reply_to(
            message,
            "Сначала выберите голос командой /start или из доступных голосов."
        )


if __name__ == "__main__":
    bot.polling(none_stop=True)
