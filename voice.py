import os
from elevenlabs import ElevenLabs, VoiceSettings
import config

# Создаем клиента ElevenLabs с использованием API ключа
client = ElevenLabs(api_key=config.elevenlabs_api_key)


def get_all_voices():
    try:
        # Получаем список голосов и выводим структуру данных для отладки
        voices_response = client.voices.get_all()
        print("Voices response:", voices_response)  # Отладочная информация

        # Проверяем, является ли ответ списком или содержит нужную структуру
        if isinstance(voices_response, list):
            return [{'name': voice['name'], 'id': voice['voice_id']} for voice in voices_response]
        elif hasattr(voices_response, 'voices'):
            # В некоторых API ответ может содержать ключ `voices`, который содержит список голосов
            return [{'name': voice.name, 'id': voice.voice_id} for voice in voices_response.voices]
        else:
            print("Unexpected response format:", voices_response)
            return []
    except Exception as e:
        print(f"Error fetching voices: {e}")
        return []
def generate_audio(text: str, voice_id: str):
    try:
        # Генерация аудио с использованием потоков
        audio_stream = client.text_to_speech.convert_as_stream(
            voice_id=voice_id,
            optimize_streaming_latency="0",
            output_format="mp3_22050_32",
            text=text,
            voice_settings=VoiceSettings(
                stability=0.1,
                similarity_boost=0.3,
                style=0.2
            )
        )

        # Сохранение аудио в файл
        file_name = "audio.mp3"
        with open(file_name, "wb") as audio_file:
            for chunk in audio_stream:
                audio_file.write(chunk)

        # Проверка, был ли файл сохранен
        if os.path.exists(file_name):
            return file_name
        else:
            print("Audio file was not saved correctly.")
            return None
    except Exception as e:
        print(f"Error generating audio: {e}")
        return None

if __name__ == "__main__":
    voices_list = get_all_voices()
    print("Available Voices:", voices_list)

    if voices_list:
        test_voice_id = voices_list[0]['id']
        file = generate_audio("Пример текста для тестирования", test_voice_id)
        print(f"Файл сохранён: {file}")


