from PySide6.QtCore import QThread, Signal, QObject
from assistant.models.stt_model import SpeechToTextModel


class STTProcessingThread(QThread):
    text_recognized_signal = Signal(str)
    error_signal = Signal(str)

    def __init__(self) -> None:
        super().__init__()
        self.stt_model = SpeechToTextModel()
        self.is_running = True

    def run(self) -> None:
        print(1)
        try:
            while self.is_running:
                recognized_text = self.stt_model.listen()
                if recognized_text:

                    self.text_recognized_signal.emit(recognized_text)

        except Exception as e:
            self.error_signal.emit(f"Ошибка в потоке STT: {str(e)}")

    def stop(self) -> None:
        self.is_running = False
        self.stt_model.close()
        self.quit()


class STTService(QObject):  # Наследуем от QObject для работы с сигналами
    text_recognized_signal = Signal(str)

    def __init__(self) -> None:
        super().__init__()
        self.stt_thread = None

    def start_listening(self) -> None:
        if self.stt_thread and self.stt_thread.isRunning():
            print("Поток уже запущен.")
            return

        self.stt_thread = STTProcessingThread()

        # Подключаем сигналы
        self.stt_thread.error_signal.connect(self._on_error)
        self.stt_thread.text_recognized_signal.connect(self._on_text_recognized)

        self.stt_thread.start()

    def stop_listening(self) -> None:
        if self.stt_thread and self.stt_thread.isRunning():
            self.stt_thread.stop()
            self.stt_thread.wait()  # Дожидаемся завершения потока

    def _on_text_recognized(self, text: str) -> None:
        print(f"Распознанный текст: {text}")

        self.text_recognized_signal.emit(text)

    @staticmethod
    def _on_error(error_message: str) -> None:
        print(f"Ошибка: {error_message}")
