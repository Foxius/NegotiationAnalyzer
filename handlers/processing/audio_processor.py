import os
from pydub import AudioSegment


class AudioProcessor:
    def __init__(self, input_folder, output_folder):
        self.input_folder = input_folder
        self.output_folder = output_folder

    def convert_to_wav(self, file_path):
        ogg_audio = AudioSegment.from_ogg(file_path)
        wav_path = os.path.join(self.output_folder, os.path.splitext(os.path.basename(file_path))[0] + '.wav')
        ogg_audio.export(wav_path, format='wav')
        return wav_path
