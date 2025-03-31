import threading
import queue
from assistant.core.services.fsm_service.fsm import FSM
from assistant.core.services.audio_service import AudioService


class FSMThreadManager:
    def __init__(self, audio_service: AudioService):
        # Создаем очередь для пользовательского ввода
        self.input_queue = queue.Queue()
        # Создаем FSM
        self.fsm = FSM(audio_service)
        # Флаг остановки потока
        self.running = False
        # Поток для FSM
        self.thread = None

    def start(self):
        """Запускает FSM в отдельном потоке."""
        if not self.running:
            print("Starting FSM thread...")
            self.running = True
            self.thread = threading.Thread(target=self._run_fsm, daemon=True)
            self.thread.start()

    def stop(self):
        """Останавливает поток FSM."""
        if self.running:
            print("Stopping FSM thread...")
            self.running = False
            self.thread.join()  # Ждем завершения потока

    def process_input(self, user_input):
        """Отправляет пользовательский ввод в FSM."""
        if not self.running:
            print("FSM thread is not running. Starting it now...")
            self.start()
        print(f"Adding input to queue: {user_input}")
        self.input_queue.put(user_input)

    def _run_fsm(self):
        """Основной цикл FSM в потоке."""
        print("FSM thread started.")
        while self.running:
            try:
                user_input = self.input_queue.get(timeout=1)
                print(f"Processing input: {user_input}")
                try:
                    response = self.fsm.process(user_input)
                    print(f"FSM Response: {response}")
                except Exception as e:
                    print(f"Error in fsm.process: {e}")
            except queue.Empty:
                continue