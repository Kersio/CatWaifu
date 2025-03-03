from PySide6.QtCore import QThread, Signal
import numpy as np
import sounddevice as sd

from assistant.models.tts_model import TextToSpeechModel
from config import SAMPLE_RATE_AUDIO


class AudioPlayerThread(QThread):
    finished_signal = Signal()
    error_signal = Signal(str)

    def __init__(self, audio_tensor, sample_rate):
        super().__init__()
        self.audio_tensor = audio_tensor
        self.sample_rate = sample_rate

    def run(self):
        try:
            audio_numpy = self.audio_tensor.cpu().numpy()
            audio_numpy = audio_numpy / np.max(np.abs(audio_numpy))
            sd.play(audio_numpy, self.sample_rate)
            sd.wait()
            self.finished_signal.emit()

        except Exception as e:
            self.error_signal.emit(str(e))


class AudioService:
    def __init__(self, sample_rate_audio=SAMPLE_RATE_AUDIO):
        self.tts_model = TextToSpeechModel()
        self.current_thread = None
        self.sample_rate_audio = sample_rate_audio

    def sound_text(self, text: str):
        audio_tensor = self.tts_model.generate_speech(text)
        self._play_audio(audio_tensor)

    def play_audio_tensor(self, audio_tensor):
        self._play_audio(audio_tensor)

    def _play_audio(self, audio_tensor):
        if self.current_thread and self.current_thread.isRunning():
            self.current_thread.wait()
        self.current_thread = AudioPlayerThread(audio_tensor, self.sample_rate_audio)
        self.current_thread.start()
