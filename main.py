import os
from handlers.processing.audio_processor import AudioProcessor
from handlers.processing.speech_recognizer import SpeechRecognizer
from handlers.utils.regulation_checker import RegulationChecker

source_folder = 'samples'
output_folder = 'wav_samples'

if not os.path.exists(output_folder):
    os.makedirs(output_folder)


def main():
    recognizer = SpeechRecognizer(language='ru-RU')
    checker = RegulationChecker('regulations.json')
    processor = AudioProcessor(input_folder=source_folder, output_folder=output_folder)
    for file_name in os.listdir(source_folder):
        if file_name.endswith('.ogg'):
            file_path = os.path.join(source_folder, file_name)

            wav_path = processor.convert_to_wav(file_path)
            text = recognizer.recognize_speech(wav_path)
            compliance_results = checker.check_compliance(text)
            for result in compliance_results:
                print(f"{file_name} - {result[1]}: {'Соответствует' if result[0] else 'Нарушение'}")

if __name__ == "__main__":
    main()
