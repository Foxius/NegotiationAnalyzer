import os

from vosk import Model


def load_model(model_path="model"):
    if not os.path.exists(model_path):
        print(
            f"Пожалуйста, скачайте модель Vosk с https://alphacephei.com/vosk/models и распакуйте ее в '{model_path}'"
        )
        return ""
    model = Model(model_path)
    return model