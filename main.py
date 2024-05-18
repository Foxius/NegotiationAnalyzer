import os
import wave
import json
from vosk import Model, KaldiRecognizer, SetLogLevel
from pydub import AudioSegment

def transcribe_mp3(mp3_file, model_path="model"):
    """
    Транскрибирует MP3 файл с помощью Vosk.

    Args:
        mp3_file: Путь к MP3 файлу.
        model_path: Путь к папке с моделью Vosk.
    Returns:
        Строка, содержащая транскрибированный текст.
    """

    SetLogLevel(0)

    # Проверка наличия модели
    if not os.path.exists(model_path):
        print(
            f"Пожалуйста, скачайте модель Vosk с https://alphacephei.com/vosk/models и распакуйте ее в '{model_path}'"
        )
        return ""

    # Конвертация MP3 в WAV
    wav_file = os.path.splitext(mp3_file)[0] + ".wav"
    sound = AudioSegment.from_mp3(mp3_file)
    sound.export(wav_file, format="wav")

    # Транскрипция WAV файла
    wf = wave.open(wav_file, "rb")
    if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getcomptype() != "NONE":
        print("Audio file must be WAV format mono PCM.")
        return ""

    model = Model(model_path)
    rec = KaldiRecognizer(model, wf.getframerate())

    transcription = ""
    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            result = json.loads(rec.Result())  # Преобразуем JSON строку в словарь
            transcription += f"{result.get('text', '')} "

    result = json.loads(rec.FinalResult()) # Преобразуем JSON строку в словарь
    transcription += f"{result.get('text', '')} "

    return transcription

# Пример использования
mp3_file = input("Укажите путь до файла: ")  # Путь к вашему MP3 файлу
transcription = transcribe_mp3(mp3_file)
print(f"Транскрипция: {transcription}")
