from dotenv import load_dotenv
import os

# Загрузка переменных окружения из файла .env
load_dotenv()
elevenlabs_api_key=os.getenv('elevenlabs_api_key')
bot_token= os.getenv('bot_token')

