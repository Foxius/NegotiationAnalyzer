import os
import shutil
import wave
import json
from vosk import KaldiRecognizer, SetLogLevel
from pydub import AudioSegment
import librosa
import soundfile as sf

from config import input_dir, out_dir
from handlers.model import load_model

model = load_model()


def transcribe_mp3(name):
    SetLogLevel(0)

    file_path = os.path.join(input_dir, name)
    wav_file = os.path.splitext(file_path)[0] + ".wav"
    sound = AudioSegment.from_mp3(file_path)
    in_path = os.path.join(input_dir, name[:-4] + ".wav")
    out_path = os.path.join(out_dir, name[:-4] + ".wav")
    sound.export(wav_file, format="wav")
    shutil.move(in_path, out_path)
    audio, sr = librosa.load(f"./audio_out/{name[:-4]}.wav")
    audio *= 1
    sf.write(f"./audio_out/{name[:-4]}_louder.wav", audio, sr, )

    wf = wave.open(f"./audio_out/{name[:-4]}_louder.wav", "rb")
    if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getcomptype() != "NONE":
        print("Audio file must be WAV format mono PCM.")
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

    return transcription


def main():
    fls = []
    for root, dirs, files in os.walk("./audio_input"):
        for filename in files:
            fls.append(filename)

    for i in fls:
        transcription = transcribe_mp3(i)
        print(f"Filename={i} | Transcription = '{transcription}'")

if __name__ == "__main__":
    main()