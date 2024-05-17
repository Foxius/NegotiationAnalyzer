import os
from pydub import AudioSegment
import speech_recognition as sr

source_folder = 'samples'
output_folder = 'wav_samples'

os.makedirs(output_folder, exist_ok=True)

recognizer = sr.Recognizer()

def convert_and_recognize(file_path):
    ogg_audio = AudioSegment.from_ogg(file_path)
    wav_path = os.path.join(output_folder, os.path.splitext(os.path.basename(file_path))[0] + '.wav')
    ogg_audio.export(wav_path, format='wav')

    with sr.AudioFile(wav_path) as source:
        audio_data = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio_data, language='ru-RU')
            print(f"Распознанная речь в файле {os.path.basename(wav_path)}: {text}")
        except sr.UnknownValueError:
            print(f"Речь в файле {os.path.basename(wav_path)} не распознана.")
        except sr.RequestError as e:
            print(f"Ошибка запроса к API: {e}")

for file_name in os.listdir(source_folder):
    if file_name.endswith('.ogg'):
        file_path = os.path.join(source_folder, file_name)
        convert_and_recognize(file_path)
