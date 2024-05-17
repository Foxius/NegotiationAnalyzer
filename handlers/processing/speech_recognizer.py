import speech_recognition as sr


class SpeechRecognizer:
    def __init__(self, language='en-US'):
        self.recognizer = sr.Recognizer()
        self.language = language

    def recognize_speech(self, wav_path):
        with sr.AudioFile(wav_path) as source:
            audio_data = self.recognizer.record(source)
            try:
                text = self.recognizer.recognize_google(audio_data, language=self.language)
                print(f"Распознанная речь: {text}")
                return text
            except sr.UnknownValueError:
                print("Речь не распознана.")
                return ""
            except sr.RequestError as e:
                print(f"Ошибка запроса к API: {e}")
                return ""
