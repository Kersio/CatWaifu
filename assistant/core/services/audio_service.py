import torch
from PySide6.QtCore import QThread, Signal
import numpy as np
import sounddevice as sd
import queue
import librosa
from assistant.models.tts_model import TextToSpeechModel
from config import SAMPLE_RATE_AUDIO


class AudioQueueThread(QThread):
    finished_signal = Signal()
    error_signal = Signal(str)

    def __init__(self, task_queue: queue.Queue, sample_rate: int):
        super().__init__()
        self.task_queue = task_queue
        self.sample_rate = sample_rate

    def run(self):
        while True:
            task = self.task_queue.get()
            if task is None:
                break  # Условие выхода, если нужно
            try:
                self._process_task(task)
            except Exception as e:
                self.error_signal.emit(str(e))
            finally:
                self.task_queue.task_done()

    def _process_task(self, task):
        # Обработка задачи
        if task['type'] == 'tensor':
            audio_numpy = task['data'].cpu().numpy()
        elif task['type'] == 'file':
            audio, sr = librosa.load(task['path'], sr=self.sample_rate, mono=True)
            audio_numpy = audio
        else:
            return

        # Нормализация аудио
        max_val = np.max(np.abs(audio_numpy))
        if max_val > 0:
            audio_numpy /= max_val

        # Воспроизведение
        sd.play(audio_numpy, self.sample_rate)
        sd.wait()  # Блокируем поток до завершения воспроизведения

        # Уведомление о завершении
        self.finished_signal.emit()


class AudioService:
    def __init__(self, sample_rate_audio: int = SAMPLE_RATE_AUDIO) -> None:
        self.tts_model = TextToSpeechModel()
        self.sample_rate_audio = sample_rate_audio
        self.task_queue = queue.Queue()
        self.audio_thread = AudioQueueThread(self.task_queue, self.sample_rate_audio)
        self.audio_thread.finished.connect(self._on_task_finished)
        self.audio_thread.start()

    def sound_text(self, text: str) -> None:
        audio_tensor = self.tts_model.generate_speech(text)
        self.play_audio_tensor(audio_tensor)

    def play_audio_tensor(self, audio_tensor: torch.Tensor) -> None:
        self.task_queue.put({'type': 'tensor', 'data': audio_tensor})

    def play_mp3(self, file_path: str) -> None:
        self.task_queue.put({'type': 'file', 'path': file_path})

    def _on_task_finished(self):
        # Вызывается при завершении текущей задачи
        pass  # Можно добавить логику, если нужно

    def stop(self):
        """Останавливает текущее воспроизведение и очищает очередь."""
        sd.stop()  # Прерывает текущее воспроизведение
        with self.task_queue.mutex:
            self.task_queue.queue.clear()  # Очищаем очередь

    def wait_for_all_tasks(self):
        """Ждёт завершения всех задач в очереди."""
        self.task_queue.join()  # Блокирует до тех пор, пока не будут обработаны все задачи

    def __del__(self):
        # Убедимся, что поток завершился при удалении объекта
        self.task_queue.put(None)
        self.audio_thread.wait()