import os
import shutil
import wave
import json
from vosk import KaldiRecognizer, SetLogLevel
from pydub import AudioSegment
import librosa
import soundfile as sf
import noisereduce as nr
import numpy as np

from config import input_dir, out_dir
from handlers.model import load_model

model = load_model()


# Цвета для консоли
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    TRANSCRIPTION = '\033[33m'  # Цвет для транскрипции


def rms_normalize(audio):
    """Нормализует аудио по среднеквадратичному (RMS) значению."""
    print(f"{bcolors.OKBLUE}  Нормализация звука...{bcolors.ENDC}")
    rms = np.sqrt(np.mean(np.square(audio)))
    return audio / rms


def transcribe_mp3(name):
    print(f"{bcolors.HEADER}Обработка файла: {name}{bcolors.ENDC}")
    SetLogLevel(0)

    file_path = os.path.join(input_dir, name)
    wav_file = os.path.splitext(file_path)[0] + ".wav"

    print(f"{bcolors.OKCYAN}  Конвертация MP3 в WAV...{bcolors.ENDC}")
    sound = AudioSegment.from_mp3(file_path)
    in_path = os.path.join(input_dir, name[:-4] + ".wav")
    out_path = os.path.join(out_dir, name[:-4] + ".wav")
    sound.export(wav_file, format="wav")
    shutil.move(in_path, out_path)

    print(f"{bcolors.OKGREEN}  Загрузка аудио...{bcolors.ENDC}")
    audio, sr = librosa.load(f"./audio_out/{name[:-4]}.wav")

    print(f"{bcolors.WARNING}  Обрезка тишины...{bcolors.ENDC}")
    trimmed_audio, _ = librosa.effects.trim(audio, top_db=20)

    normalized_audio = rms_normalize(trimmed_audio)

    print(f"{bcolors.FAIL}  Удаление шума...{bcolors.ENDC}")
    reduced_noise = nr.reduce_noise(y=normalized_audio, sr=sr)

    print(f"{bcolors.BOLD}  Сохранение обработанного аудио...{bcolors.ENDC}")
    sf.write(f"./audio_out/{name[:-4]}_processed.wav", reduced_noise, sr)

    print(f"{bcolors.UNDERLINE}  Транскрипция обработанного аудио...{bcolors.ENDC}")
    wf = wave.open(f"./audio_out/{name[:-4]}_processed.wav", "rb")
    if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getcomptype() != "NONE":
        print(f"    {bcolors.FAIL}Ошибка: Audio file must be WAV format mono PCM.{bcolors.ENDC}")
        return ""

    rec = KaldiRecognizer(model, wf.getframerate())

    transcription = ""
    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            result = json.loads(rec.Result())
            transcription += f"{result.get('text', '')} "

    result = json.loads(rec.FinalResult())
    transcription += f"{result.get('text', '')} "

    print(f"{bcolors.OKGREEN}  Транскрипция завершена.{bcolors.ENDC}")
    return transcription


def main():
    fls = []
    for root, dirs, files in os.walk("./audio_input"):
        for filename in files:
            if filename.endswith(".mp3"):  # Проверка расширения файла
                fls.append(filename)

    for i in fls:
        transcription = transcribe_mp3(i)
        print(f"Filename={i} | Transcription = '{bcolors.TRANSCRIPTION}{transcription}{bcolors.ENDC}'")


if __name__ == "__main__":
    main()