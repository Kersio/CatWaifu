import json
from vosk import Model, KaldiRecognizer
import pyaudio

from config import (
    SAMPLE_RATE_STT,
    MODEL_PATH_STT
)


class SpeechToTextModel:

    def __init__(self, model_path: str = MODEL_PATH_STT, sample_rate: int = SAMPLE_RATE_STT) -> None:
        self.model = Model(model_path)
        self.recognizer = KaldiRecognizer(self.model, sample_rate)
        self.sample_rate = sample_rate

        # Инициализация PyAudio
        self.audio = pyaudio.PyAudio()
        self.stream = self.audio.open(
            format=pyaudio.paInt16,  # Формат аудио (16-bit PCM)
            channels=1,  # Моно
            rate=self.sample_rate,  # Частота дискретизации
            input=True,  # Входной поток (микрофон)
            frames_per_buffer=4000  # Размер буфера
        )

    def listen(self):
        while True:
            data = self.stream.read(4000, exception_on_overflow=False)

            if len(data) == 0:
                break

            if self.recognizer.AcceptWaveform(data):
                result = json.loads(self.recognizer.Result())
                text = result.get("text", "").strip()
                if text:
                    return text
            else:
                partial_result = json.loads(self.recognizer.PartialResult())
                partial_text = partial_result.get("partial", "").strip()

        # Получение финального результата
        final_result = json.loads(self.recognizer.FinalResult())
        final_text = final_result.get("text", "").strip()
        if final_text:
            return final_text

        return ""

    def close(self):
        """
        Освобождение ресурсов.
        """
        self.stream.stop_stream()
        self.stream.close()
        self.audio.terminate()
